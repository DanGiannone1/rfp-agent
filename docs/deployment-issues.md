# Deployment Issues: Root Causes and Fixes

Investigation conducted 2026-03-07. Documents why Azure deployments keep breaking and what needs to change.

---

## What's Broken Right Now

Three specific things block a successful deploy:

### 1. ADLS network access is not set in `deploy.sh`

`deploy.sh` calls `az storage account create` but never sets `--public-network-access Enabled`. The `create` call is a no-op for existing accounts, so re-running the script after a nightly Azure Policy disables public access does nothing. Container Apps is not in Azure's "trusted services" bypass list, so every upload from the orchestrator hits a 403 `AuthorizationFailure`.

**Symptom:** PDF uploads fail with `Content Understanding failed to produce markdown` — the real error is ADLS returning 403 before CU is even attempted.

**Fix:** Add to deploy.sh after the storage account create block:
```bash
az storage account update \
    --name "$ADLS_ACCOUNT_NAME" \
    --resource-group "$RG" \
    --public-network-access Enabled \
    -o none
```

This must be an `update`, not part of `create`, so it runs on every deploy and overrides policy drift.

**Longer-term:** Request a policy exemption for `rfpagentadls`, or set up VNet integration with a storage service endpoint so public access isn't needed at all.

---

### 2. Cognitive Services role assignment silently skips

`deploy.sh` lines 98–103 extract the Cognitive Services resource name from `AZURE_ENDPOINT` using a regex. If the format doesn't match, `AOAI_RESOURCE_NAME` is empty and the entire role assignment block is skipped — no error, no warning, the script continues normally.

The managed identity ends up with `Cognitive Services OpenAI User` (granted at resource group scope) but not `Cognitive Services User` (which covers Content Understanding). CU calls return `PermissionDenied`.

**Fix:** Add an explicit failure if the resource name can't be parsed:
```bash
if [ -z "$AOAI_RESOURCE_NAME" ]; then
    echo "ERROR: Could not parse Cognitive Services resource name from AZURE_ENDPOINT=$AZURE_ENDPOINT"
    exit 1
fi
```

---

### 3. RBAC propagation lag after fresh deploy

Azure takes 5–10 minutes to propagate role assignments after `az role assignment create`. The script doesn't wait. Containers that start up during this window can't authenticate to CU or ADLS and fail. The deploy script exits 0, everything looks healthy, but the first uploads fail.

**Fix:** Add a wait after role assignments, or add a post-deploy smoke test (see below) with enough retries to cover the propagation window.

---

## Broader Findings

### The test suite doesn't test Azure

Every production bug was in the Azure infrastructure layer. The test suite doesn't touch it.

- **All file uploads in the test suite used `.txt` files** (Journeys 1, 2, 4, 6, visual suite). Text files bypass Content Understanding entirely — decoded as UTF-8 directly, no CU API call. Content Understanding was completely broken and all tests passed.
- **Zero tests verify RBAC permissions.** No test checks whether the managed identity can reach ADLS, CU, or AI Search.
- **`/health` returns a hardcoded `{"status": "ok"}`** — it doesn't probe any downstream service. A test asserting the service is healthy asserts nothing meaningful.
- **Journey 4 isolation test can't fail in practice** — asserts `reply.length > 5` instead of asserting the reply does not contain the leaked value.
- **Journey 5 concurrent send test accepts any response** — success or error both pass.

### `deploy.sh` has no pre- or post-deploy validation

- No `npm run build` or `uv run pytest` before images are pushed
- No health check after containers deploy — script exits 0 even if containers are crash-looping
- `2>/dev/null` on `az containerapp create` and `az containerapp sessionpool create` swallows real errors (quota failures, permission errors) not just "already exists"
- No CI/CD pipeline exists — every deploy is manual from a developer's machine

### All images are tagged `:latest`

No git SHA tags, no semantic versioning. No way to correlate a running container to a git commit, no rollback path without rebuilding from a previous commit, no way to detect version skew between services.

### Version skew during deployment

The deploy order is: session container image → session pool update → orchestrator image → orchestrator deploy → frontend image → frontend deploy. The session pool gets new containers immediately while the orchestrator is still running old code. Pre-warmed sessions run new code against an old orchestrator for several minutes during every deploy.

### Dockerfile COPY lists are fragile

The orchestrator Dockerfile copies only `app.py session_manager.py content_processing.py`. Any new Python module that `app.py` imports will be silently absent from the built image — the build succeeds, the container crashes at runtime. The session container has the same problem.

### Gaps in `deploy.sh`

| Gap | Impact |
|-----|--------|
| No `az storage account update --public-network-access Enabled` | ADLS blocked by nightly policy |
| `AZURE_CLIENT_ID` not set on session pool env vars | Unreliable managed identity in session containers |
| Search service managed identity roles not assigned | Knowledge base indexer fails silently |
| Fragile `AOAI_RESOURCE_NAME` parsing silently skips CU role assignments | Managed identity lacks CU permission after fresh deploy |
| No post-deploy smoke test | No way to know the deploy worked until a user hits an error |

---

## Recommended Fixes

### Immediate (1–2 lines each in `deploy.sh`)

1. Add `az storage account update --public-network-access Enabled` after the storage account create block
2. Add `exit 1` if `AOAI_RESOURCE_NAME` is empty instead of silently skipping
3. Add `AZURE_CLIENT_ID=$IDENTITY_CLIENT_ID` to the session pool `--env-vars` list
4. Add search service MI role assignments: `Storage Blob Data Reader` on ADLS and `Cognitive Services User` on the Foundry resource

### Short-term

**Deep health endpoint** — extend `/health` to probe real dependencies:

```json
GET /health/deep
{
  "status": "ok|degraded|error",
  "content_processing": {
    "enabled": true,
    "adls": "ok|error|disabled",
    "cu": "ok|error|disabled"
  },
  "session_pool": "ok|error",
  "version": "abc1234"
}
```

`adls` and `cu` must make actual lightweight API calls — a constructed SDK client with wrong permissions is indistinguishable from a working one until you make a real call.

**Post-deploy smoke test** — a script or Playwright test that runs against the deployed Azure URLs immediately after deploy:

1. Create a session
2. Upload `sample_data/MD_RFP_SUBSET.pdf`
3. Assert `markdown_ready: true` within 3 minutes
4. Delete the session

This single test would have caught all three production bugs (init deadlock, missing CU role, ADLS network blocked).

**Git SHA image tags** — tag images with `git rev-parse --short HEAD` in addition to `:latest`. Enables rollback and correlates running containers to commits.

### Longer-term

**CI/CD pipeline** (GitHub Actions or Azure DevOps):
1. On PR: lint, build
2. On merge to main: build images with SHA tag, push to ACR, deploy to staging, run post-deploy smoke test

**VNet integration for ADLS** — put Container Apps on a VNet with a `Microsoft.Storage` service endpoint. Configure ADLS to allow traffic from that subnet. Removes the dependency on `publicNetworkAccess: Enabled` entirely, making the nightly policy irrelevant.

**`COPY . .` in Dockerfiles with `.dockerignore`** — replace fragile explicit COPY lists with `COPY . .` and a `.dockerignore` that excludes dev artifacts. New Python files are automatically included.

---

## Files That Need Changes

| File | Change needed |
|------|---------------|
| `infra/deploy.sh` | ADLS network update, RBAC guard, session pool `AZURE_CLIENT_ID`, search MI roles |
| `app.py` | Add `/health/deep` endpoint that probes real dependencies |
| `content_processing.py` | Already fixed (init deadlock, managed identity client ID) |
| `tests/comprehensive.spec.ts` | Journey 3 already fixed (PDF); Journey 4 isolation assertion needs strengthening |
| `Dockerfile` (orchestrator) | Consider `COPY . .` with `.dockerignore` |
| `session-container/Dockerfile` | Same |
