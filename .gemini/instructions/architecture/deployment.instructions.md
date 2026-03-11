---
name: architecture:deployment
description: Azure deployment resources and commands for the RFP Agent — ACR builds, container updates, session pool config.
---

# Deployment

## Azure Resources

| Resource | Name |
|---|---|
| Resource Group | `rfpagent-rg` |
| Container Registry | `rfpagentacr.azurecr.io` |
| Orchestrator (ACA) | `rfpagent-app` |
| Frontend (ACA) | `rfpagent-frontend` |
| Session Pool (ACA) | `rfpagent-sessions` (max=20, ready=5, cooldown=300s) |

Easy Auth is disabled; IP restriction is used instead.

## CRITICAL: Never Use :latest for ACA Deployments

`az containerapp update --image repo:latest` is **silently broken** for all ACA services — not just session pools. ACA resolves the tag to a digest at revision creation time and caches it. If the image string in the command hasn't changed since the last revision, ACA no-ops: no new revision, no image pull, old code keeps running. This is a [known unfixed ACA bug since 2022](https://github.com/microsoft/azure-container-apps/issues/311).

**Fix: always use git SHA tags.** A changed image string forces a new revision.

## Build + Deploy (use git SHA)

```bash
SHA=$(git rev-parse --short HEAD)

# Build all three in parallel (cloud-side builds)
az acr build --registry rfpagentacr \
  --image rfp-session:$SHA --image rfp-session:latest \
  --file session-container/Dockerfile session-container/

az acr build --registry rfpagentacr \
  --image rfp-orchestrator:$SHA --image rfp-orchestrator:latest \
  --file Dockerfile .

az acr build --registry rfpagentacr \
  --image rfp-frontend:$SHA --image rfp-frontend:latest \
  --build-arg "NEXT_PUBLIC_API_URL=https://rfpagent-app.kindground-24020708.eastus2.azurecontainerapps.io" \
  --file frontend/Dockerfile frontend/

# Deploy using SHA tag — ACA sees a changed string, creates a new revision
az containerapp sessionpool update \
  --name rfpagent-sessions --resource-group rfpagent-rg \
  --image rfpagentacr.azurecr.io/rfp-session:$SHA \
  --cooldown-period 300 --max-sessions 20 --ready-sessions 5

az containerapp update \
  --name rfpagent-app --resource-group rfpagent-rg \
  --image rfpagentacr.azurecr.io/rfp-orchestrator:$SHA

az containerapp update \
  --name rfpagent-frontend --resource-group rfpagent-rg \
  --image rfpagentacr.azurecr.io/rfp-frontend:$SHA
```

Session pool update takes ~2-3 minutes (InProgress → Succeeded) while it reprovisions containers. Orchestrator and frontend update in ~30s.

## Full Deployment Script

`infra/deploy.sh` — provisions ACA, ACR, ADLS Gen2, Azure AI Search, and all required Azure resources from scratch. Entra ID app registration is a **manual prerequisite** — pass `ENTRA_TENANT_ID`, `ENTRA_CLIENT_ID`, and `ENTRA_CLIENT_SECRET` to the script to configure Easy Auth using an existing registration.

## Public URLs

- Frontend: `https://rfpagent-frontend.kindground-24020708.eastus2.azurecontainerapps.io`
- Orchestrator: `https://rfpagent-app.kindground-24020708.eastus2.azurecontainerapps.io`
