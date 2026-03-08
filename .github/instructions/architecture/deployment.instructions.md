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

## Build (Run in Parallel)

```bash
TAG="deploy-$(date +%Y%m%d-%H%M%S)"

az acr build --registry rfpagentacr \
  --image rfp-session:latest --image rfp-session:$TAG \
  --file session-container/Dockerfile session-container/

az acr build --registry rfpagentacr \
  --image rfp-orchestrator:latest \
  --file Dockerfile .

az acr build --registry rfpagentacr \
  --image rfp-frontend:latest \
  --build-arg "NEXT_PUBLIC_API_URL=https://rfpagent-app.kindground-24020708.eastus2.azurecontainerapps.io" \
  --file frontend/Dockerfile frontend/
```

## Update (Run Sequentially)

```bash
# IMPORTANT: Never use :latest for session pools — ACA caches tag resolution
az containerapp sessionpool update \
  --name rfpagent-sessions \
  --resource-group rfpagent-rg \
  --image rfpagentacr.azurecr.io/rfp-session:$TAG \
  --cooldown-period 300 --max-sessions 20 --ready-sessions 5

az containerapp update \
  --name rfpagent-app \
  --resource-group rfpagent-rg \
  --image rfpagentacr.azurecr.io/rfp-orchestrator:latest

az containerapp update \
  --name rfpagent-frontend \
  --resource-group rfpagent-rg \
  --image rfpagentacr.azurecr.io/rfp-frontend:latest
```

## Full Deployment Script

`infra/deploy.sh` — provisions ACA, ACR, ADLS Gen2, Azure AI Search, and all required Azure resources from scratch. Entra ID app registration is a **manual prerequisite** — pass `ENTRA_TENANT_ID`, `ENTRA_CLIENT_ID`, and `ENTRA_CLIENT_SECRET` to the script to configure Easy Auth using an existing registration.

## Public URLs

- Frontend: `https://rfpagent-frontend.kindground-24020708.eastus2.azurecontainerapps.io`
- Orchestrator: `https://rfpagent-app.kindground-24020708.eastus2.azurecontainerapps.io`
