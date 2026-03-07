# Review 5: Infrastructure & Config

## Observations

- [OBSERVATION] `SEARCH_KEY` (the Azure AI Search admin key) is retrieved at line 164-167 and passed in plaintext as an env var value in the `--env-vars` list at line 230 and line 247. Because `az containerapp sessionpool create/update` logs command arguments, this key will appear in shell history, CI logs, and Azure Activity Log. | severity: high | infra/deploy.sh:164-167,230,247

- [OBSERVATION] `ENTRA_CLIENT_SECRET` is accepted as an environment variable (line 47) and passed directly to `az containerapp auth microsoft update --client-secret` at line 339. The value will be visible in the shell's process list (`ps aux`) and shell history during deployment. A Key Vault reference should be used instead. | severity: high | infra/deploy.sh:339

- [OBSERVATION] When `AOAI_RESOURCE_NAME` cannot be parsed from `AZURE_ENDPOINT` (both regex branches fail), the block at lines 103-122 is silently skipped — no role is assigned and no error or warning is printed. The container will fail at runtime when it tries to authenticate to Azure OpenAI, with no indication during deployment that the role assignment was omitted. | severity: high | infra/deploy.sh:103-122

- [OBSERVATION] When `AOAI_RESOURCE_NAME` is parsed but the Cognitive Services resource is not found in `$RG`, the script falls back to assigning "Cognitive Services User" at the entire subscription scope (line 112). This grants the managed identity access to every Cognitive Services resource across the subscription, violating least-privilege. | severity: high | infra/deploy.sh:107-113

- [OBSERVATION] `AZURE_SEARCH_KEY` is stored in the `SEARCH_KEY` shell variable and injected into session pool env vars as a plaintext string (lines 229-230 and 246-247). The session container environment in ACA will hold a static admin key. The CLAUDE.md and agent.py already support managed identity auth for search roles; using a key here bypasses that entirely and creates a long-lived secret that is not rotated. | severity: high | infra/deploy.sh:164-167,229-230,246-247

- [OBSERVATION] `AZURE_SEARCH_KEY` is exposed in `.env.example` as a required field (line 22) with no note that managed identity is a viable alternative for production, encouraging developers to copy a static key into their `.env` and commit-adjacent files. | severity: medium | .env.example:22

- [OBSERVATION] The `mcp.json` file documents the MCP server configuration with a literal `"api-key"` header field (line 7). Although the comment in `agent.py` (line: "not loaded by code") says this file is not used at runtime, the file is checked into the repository. If a developer were to replace the placeholder with a real key during testing and commit it, or if tooling auto-loads `mcp.json`, the key would leak. The field name `api-key` is not redacted or templated in a way that makes the risk obvious. | severity: medium | mcp.json:7

- [OBSERVATION] Section "12" is used twice as the step label — lines 352 and 371 both read `# ── 12. ...`. The second block (Deploy Frontend) should be step 13, and the existing step 13 (CORS) should be 14, etc. This numbering collision makes the script harder to follow and audit. | severity: low | infra/deploy.sh:352,371

- [OBSERVATION] `AZURE_DEPLOYMENT` defaults to `"gpt-5-codex"` (line 33). This is not a real Azure OpenAI deployment name and is almost certainly a placeholder that was never updated. A deployment named `gpt-5-codex` does not exist in standard Azure OpenAI; any deployment using this default will silently fail at runtime. | severity: high | infra/deploy.sh:33

- [OBSERVATION] `AZURE_SEARCH_KB_NAME` is hardcoded to `"rfp-knowledge"` in both `--env-vars` blocks (lines 231 and 249) rather than derived from the `AZURE_SEARCH_KB_NAME` variable used in `.env.example` (line 23) and referenced in `agent.py` (line 34). If an operator changes the KB name, the deploy script will not pick it up. | severity: medium | infra/deploy.sh:231,249

- [OBSERVATION] The `az storage fs create` command (line 136-140) suppresses all errors with `2>/dev/null || true`. If the failure is something other than "already exists" (e.g., auth failure, invalid account name), the error is silently swallowed and the filesystem is never created, but the script proceeds as if it succeeded. | severity: medium | infra/deploy.sh:136-140

- [OBSERVATION] The `az containerapp sessionpool create` and `az containerapp create` commands (lines 211-234 and 288-307) suppress stderr with `2>/dev/null` as a way to detect "already exists." This also suppresses genuine errors (auth failure, quota exceeded, malformed arguments). A more precise check — e.g., inspecting the exit code or using `az containerapp show` first — would not swallow real failures. | severity: medium | infra/deploy.sh:211-234,288-307

- [OBSERVATION] The CORS configuration at line 415 unconditionally includes `"http://localhost:3000"` as an allowed origin in the production ingress CORS rule. This allows requests from any local development server to the production orchestrator, potentially bypassing intended access controls. | severity: medium | infra/deploy.sh:415

- [OBSERVATION] `ALLOWED_IP` applies IP restrictions to both the orchestrator and frontend (lines 424-435) but does not restrict the Container Apps Environment's internal network or the session pool management endpoint. An attacker on the same ACA environment could reach the pool endpoint even when IP restrictions are enabled. | severity: medium | infra/deploy.sh:422-439

- [OBSERVATION] The `dev.py` script hardcodes `POOL_MANAGEMENT_ENDPOINT` to `"http://localhost:8080"` (line 22), overriding any value from `.env`. This is intentional for local dev but means that if `POOL_MANAGEMENT_ENDPOINT` is set in `.env` with a real value (e.g., a staging pool), `dev.py` will silently ignore it and use localhost instead. There is no warning emitted. | severity: low | dev.py:22

- [OBSERVATION] `dev.py` deletes and recreates the entire workspace directory on every startup (lines 27-29) with no confirmation prompt and no check for whether files in the workspace are important. If a developer restarts `dev.py` mid-session, all uploaded and generated files are permanently deleted without warning. | severity: medium | dev.py:27-29

- [OBSERVATION] `dev.py` does not validate that any required environment variables are present after loading `.env`. It only checks for the existence of the `.env` file (line 17). If `AZURE_ENDPOINT` or `AZURE_DEPLOYMENT` are missing or still set to placeholder values, all three services will start without error and only fail at the point of first API call. | severity: medium | dev.py:17-21

- [OBSERVATION] `dev.py` starts all three subprocesses with `subprocess.Popen` but does not monitor them for unexpected exits. If the session container crashes on startup (e.g., missing dependency), `dev.py` continues running with the orchestrator and frontend active, giving no indication that the backend is down. | severity: low | dev.py:47-62,70-71

- [OBSERVATION] `.env.example` marks `AZURE_SEARCH_ENDPOINT` and `AZURE_SEARCH_KEY` as "required" in a comment (line 17: `# Knowledge base (required)`), but `agent.py` treats `AZURE_SEARCH_ENDPOINT` as optional (line 235: `kb_enabled = bool(SEARCH_ENDPOINT)`). The mismatch will confuse developers who read `.env.example` and believe search must be configured before the app will work. | severity: low | .env.example:17-23

- [OBSERVATION] `.env.example` does not document `AZURE_CLIENT_ID`, which is set as an env var on the orchestrator container app at line 306 of `deploy.sh` and is used by `DefaultAzureCredential` to select the user-assigned managed identity. Without this variable documented, local developers or operators running the app outside the deploy script will not know to set it. | severity: medium | .env.example (entire file), infra/deploy.sh:306

- [OBSERVATION] `.env.example` does not document `CHAT_TIMEOUT_SECONDS` as actually required or defaulted — it is shown as a comment (line 46) with no default value, while the session container presumably uses a hardcoded default. A developer looking to tune the timeout has no indication of the current default value. | severity: low | .env.example:46

- [OBSERVATION] The `ADLS_ACCOUNT_NAME` default in `deploy.sh` (line 35) is `"${PREFIX}adls"`, which expands to `"rfpagentadls"`. Azure storage account names must be 3-24 characters; `"rfpagentadls"` is 12 characters and valid, but if `PREFIX` is overridden to a longer value the name could silently exceed 24 characters, causing `az storage account create` to fail with an opaque error. There is no length validation. | severity: low | infra/deploy.sh:35

- [OBSERVATION] The `ACR_NAME` variable (line 27) is derived as `"${PREFIX}acr"` (default: `"rfpagentacr"`). ACR names must be globally unique and 5-50 alphanumeric characters. If `PREFIX` contains hyphens (common for Azure naming conventions), the ACR creation will fail because hyphens are not allowed in ACR names. There is no sanitization or validation. | severity: medium | infra/deploy.sh:27

- [OBSERVATION] `Storage Blob Data Contributor` is granted to the managed identity on the ADLS account (line 144-149). The CLAUDE.md documentation says only `Storage Blob Data Reader` is required for the search indexer, and the agent only needs to upload/read files. `Data Contributor` grants delete permissions on all blobs, which exceeds what is needed for the document processing and retrieval use cases. | severity: medium | infra/deploy.sh:142-149

- [OBSERVATION] `Search Service Contributor` is granted to the managed identity on the search service (lines 180-185). This role allows modifying search service configuration, creating and deleting indexes, and managing API keys — far beyond what the agent needs at runtime (which is only `Search Index Data Reader` for querying). The elevated role appears to be granted for the one-time `setup_knowledge_base.py` script but persists permanently on the production identity. | severity: medium | infra/deploy.sh:180-185

- [OBSERVATION] `ENTRA_REDIRECT_URI` is derived using a preview of the frontend URL before the frontend container app is actually deployed (line 357). The `FRONTEND_URL_PREVIEW` value is constructed from the ACA environment's default domain plus `FRONTEND_NAME`, but the actual FQDN assigned by ACA may differ (e.g., if a revision suffix is appended). If the derived URI is wrong, MSAL authentication will fail silently after deployment because the redirect URI baked into the frontend image will not match the registered URI. | severity: medium | infra/deploy.sh:357-358
