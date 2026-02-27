#!/usr/bin/env bash
#
# Deploy the RFP Agent to Azure Container Apps with Dynamic Sessions.
#
# Prerequisites:
#   - Azure CLI (az) installed and logged in
#   - Docker (for building images)
#
# Usage:
#   ./infra/deploy.sh                          # uses defaults
#   LOCATION=westus2 ./infra/deploy.sh         # override location
#
set -euo pipefail

# ── Configuration ─────────────────────────────────────────────────────────
PREFIX="${PREFIX:-rfpagent}"
LOCATION="${LOCATION:-eastus2}"
RG="${PREFIX}-rg"
IDENTITY_NAME="${PREFIX}-identity"
ACR_NAME="${PREFIX}acr"
ENV_NAME="${PREFIX}-env"
SESSION_POOL_NAME="${PREFIX}-sessions"
APP_NAME="${PREFIX}-app"
FRONTEND_NAME="${PREFIX}-frontend"

AZURE_DEPLOYMENT="${AZURE_DEPLOYMENT:-gpt-5-codex}"
COSMOS_ENDPOINT="${COSMOS_ENDPOINT:-}"

echo "=== RFP Agent Deployment ==="
echo "Resource Group:  $RG"
echo "Location:        $LOCATION"
echo "ACR:             $ACR_NAME"
echo "Session Pool:    $SESSION_POOL_NAME"
echo "App:             $APP_NAME"
echo ""

# ── 1. Resource Group ────────────────────────────────────────────────────
echo ">>> Creating resource group..."
az group create --name "$RG" --location "$LOCATION" -o none

# ── 2. User-Assigned Managed Identity ────────────────────────────────────
echo ">>> Creating managed identity..."
az identity create --name "$IDENTITY_NAME" --resource-group "$RG" -o none

IDENTITY_ID=$(az identity show --name "$IDENTITY_NAME" --resource-group "$RG" --query id -o tsv)
IDENTITY_CLIENT_ID=$(az identity show --name "$IDENTITY_NAME" --resource-group "$RG" --query clientId -o tsv)
IDENTITY_PRINCIPAL_ID=$(az identity show --name "$IDENTITY_NAME" --resource-group "$RG" --query principalId -o tsv)

echo "    Identity Client ID: $IDENTITY_CLIENT_ID"

# ── 3. Azure Container Registry ─────────────────────────────────────────
echo ">>> Creating container registry..."
az acr create --name "$ACR_NAME" --resource-group "$RG" --sku Basic --admin-enabled false -o none

ACR_LOGIN_SERVER=$(az acr show --name "$ACR_NAME" --resource-group "$RG" --query loginServer -o tsv)
echo "    ACR Login Server: $ACR_LOGIN_SERVER"

# Grant AcrPull to the managed identity
echo ">>> Granting AcrPull to managed identity..."
ACR_ID=$(az acr show --name "$ACR_NAME" --resource-group "$RG" --query id -o tsv)
az role assignment create \
    --assignee-object-id "$IDENTITY_PRINCIPAL_ID" \
    --assignee-principal-type ServicePrincipal \
    --role AcrPull \
    --scope "$ACR_ID" \
    -o none

# ── 4. Cognitive Services role (needed by session containers for Azure OpenAI) ─
AZURE_ENDPOINT="${AZURE_ENDPOINT:-}"
if [ -z "$AZURE_ENDPOINT" ]; then
    echo "ERROR: AZURE_ENDPOINT must be set"
    exit 1
fi

echo ">>> Granting Cognitive Services OpenAI User to managed identity..."
AOAI_RESOURCE_NAME=$(echo "$AZURE_ENDPOINT" | sed -n 's|https://\(.*\)\.cognitiveservices.*|\1|p')
if [ -n "$AOAI_RESOURCE_NAME" ]; then
    AOAI_ID=$(az cognitiveservices account list --resource-group "$RG" \
        --query "[?name=='$AOAI_RESOURCE_NAME'].id" -o tsv 2>/dev/null || true)
    if [ -z "$AOAI_ID" ]; then
        echo "    Note: Azure OpenAI resource not found in $RG. Assigning at subscription scope."
        az role assignment create \
            --assignee-object-id "$IDENTITY_PRINCIPAL_ID" \
            --assignee-principal-type ServicePrincipal \
            --role "Cognitive Services OpenAI User" \
            --scope "/subscriptions/$(az account show --query id -o tsv)" \
            -o none
    else
        az role assignment create \
            --assignee-object-id "$IDENTITY_PRINCIPAL_ID" \
            --assignee-principal-type ServicePrincipal \
            --role "Cognitive Services OpenAI User" \
            --scope "$AOAI_ID" \
            -o none
    fi
fi

# ── 5. Container Apps Environment ────────────────────────────────────────
echo ">>> Creating Container Apps environment..."
az containerapp env create \
    --name "$ENV_NAME" \
    --resource-group "$RG" \
    --location "$LOCATION" \
    -o none

# ── 6. Build & Push Session Container Image ─────────────────────────────
echo ">>> Building session container image..."
SESSION_IMAGE="$ACR_LOGIN_SERVER/rfp-session:latest"
az acr build \
    --registry "$ACR_NAME" \
    --image "rfp-session:latest" \
    --file session-container/Dockerfile \
    session-container/ \
    -o none

# ── 7. Create Session Pool (Custom Container) ───────────────────────────
echo ">>> Creating session pool..."

# Get the environment ID
ENV_ID=$(az containerapp env show --name "$ENV_NAME" --resource-group "$RG" --query id -o tsv)

az containerapp sessionpool create \
    --name "$SESSION_POOL_NAME" \
    --resource-group "$RG" \
    --location "$LOCATION" \
    --environment "$ENV_ID" \
    --container-type CustomContainer \
    --image "$SESSION_IMAGE" \
    --registry-server "$ACR_LOGIN_SERVER" \
    --registry-identity "$IDENTITY_ID" \
    --target-port 8080 \
    --cooldown-period 600 \
    --network-status EgressEnabled \
    --max-sessions 50 \
    --ready-sessions 2 \
    --cpu 0.5 --memory 1Gi \
    --env-vars \
        "AZURE_ENDPOINT=$AZURE_ENDPOINT" \
        "AZURE_DEPLOYMENT=$AZURE_DEPLOYMENT" \
    -o none

POOL_ENDPOINT=$(az containerapp sessionpool show \
    --name "$SESSION_POOL_NAME" \
    --resource-group "$RG" \
    --query "properties.poolManagementEndpoint" -o tsv)

echo "    Pool Management Endpoint: $POOL_ENDPOINT"

# ── 8. Session Executor role (needed by orchestrator to call session pool) ─
echo ">>> Granting Session Executor to managed identity..."
POOL_ID=$(az containerapp sessionpool show \
    --name "$SESSION_POOL_NAME" \
    --resource-group "$RG" \
    --query id -o tsv)

az role assignment create \
    --assignee-object-id "$IDENTITY_PRINCIPAL_ID" \
    --assignee-principal-type ServicePrincipal \
    --role "Azure ContainerApps Session Executor" \
    --scope "$POOL_ID" \
    -o none

# ── 9. Build & Push Orchestrator Image ───────────────────────────────────
echo ">>> Building orchestrator image..."
az acr build \
    --registry "$ACR_NAME" \
    --image "rfp-orchestrator:latest" \
    --file Dockerfile \
    . \
    -o none

# ── 10. Deploy Orchestrator as Container App ─────────────────────────────
echo ">>> Deploying orchestrator container app..."
ORCHESTRATOR_IMAGE="$ACR_LOGIN_SERVER/rfp-orchestrator:latest"

az containerapp create \
    --name "$APP_NAME" \
    --resource-group "$RG" \
    --environment "$ENV_NAME" \
    --image "$ORCHESTRATOR_IMAGE" \
    --registry-server "$ACR_LOGIN_SERVER" \
    --registry-identity "$IDENTITY_ID" \
    --user-assigned "$IDENTITY_ID" \
    --target-port 8000 \
    --ingress external \
    --min-replicas 1 \
    --max-replicas 3 \
    --env-vars \
        "POOL_MANAGEMENT_ENDPOINT=$POOL_ENDPOINT" \
        "COSMOS_ENDPOINT=$COSMOS_ENDPOINT" \
        "AZURE_CLIENT_ID=$IDENTITY_CLIENT_ID" \
    -o none

APP_URL=$(az containerapp show \
    --name "$APP_NAME" \
    --resource-group "$RG" \
    --query "properties.configuration.ingress.fqdn" -o tsv)

echo "    App URL: https://$APP_URL"

# ── 11. Entra ID — Backend App Registration ─────────────────────────────
echo ">>> Creating backend Entra ID app registration..."
TENANT_ID=$(az account show --query tenantId -o tsv)

BACKEND_APP_ID=$(az ad app create \
    --display-name "${PREFIX}-orchestrator" \
    --sign-in-audience AzureADMyOrg \
    --query appId -o tsv)

# Create service principal (idempotent — ignores "already exists" errors)
az ad sp create --id "$BACKEND_APP_ID" 2>/dev/null || true

BACKEND_SECRET=$(az ad app credential reset \
    --id "$BACKEND_APP_ID" \
    --display-name "easy-auth" \
    --query password -o tsv)

echo "    Backend App ID: $BACKEND_APP_ID"

# Expose an API scope (Application ID URI + user_impersonation)
echo ">>> Configuring backend API scope..."
az ad app update --id "$BACKEND_APP_ID" \
    --identifier-uris "api://$BACKEND_APP_ID"

# Add oauth2PermissionScopes via MS Graph REST API
SCOPE_ID=$(python3 -c "import uuid; print(uuid.uuid4())")
az rest --method PATCH \
    --uri "https://graph.microsoft.com/v1.0/applications/$(az ad app show --id "$BACKEND_APP_ID" --query id -o tsv)" \
    --headers "Content-Type=application/json" \
    --body "{
        \"api\": {
            \"oauth2PermissionScopes\": [{
                \"adminConsentDescription\": \"Allow the app to access the RFP Agent API on behalf of the signed-in user\",
                \"adminConsentDisplayName\": \"Access RFP Agent\",
                \"id\": \"$SCOPE_ID\",
                \"isEnabled\": true,
                \"type\": \"User\",
                \"userConsentDescription\": \"Allow the app to access the RFP Agent API on your behalf\",
                \"userConsentDisplayName\": \"Access RFP Agent\",
                \"value\": \"user_impersonation\"
            }]
        }
    }" \
    -o none

# ── 12. Entra ID — Enable Easy Auth on Orchestrator ─────────────────────
echo ">>> Enabling Easy Auth on orchestrator..."
az containerapp auth microsoft update \
    --name "$APP_NAME" --resource-group "$RG" \
    --client-id "$BACKEND_APP_ID" \
    --client-secret "$BACKEND_SECRET" \
    --tenant-id "$TENANT_ID" \
    --issuer "https://login.microsoftonline.com/$TENANT_ID/v2.0" \
    --yes \
    -o none

az containerapp auth update \
    --name "$APP_NAME" --resource-group "$RG" \
    --unauthenticated-client-action Return401 \
    -o none

# ── 13. Entra ID — Frontend App Registration (SPA) ──────────────────────
echo ">>> Creating frontend Entra ID app registration..."

# Deploy frontend first to get the URL, then create the app registration
# (we need the URL for redirect URIs)

# ── 14. Build & Push Frontend Image (first pass — no auth) ──────────────
echo ">>> Building frontend image..."
az acr build \
    --registry "$ACR_NAME" \
    --image "rfp-frontend:latest" \
    --file frontend/Dockerfile \
    --build-arg "NEXT_PUBLIC_API_URL=https://$APP_URL" \
    frontend/ \
    -o none

# ── 15. Deploy Frontend as Container App ────────────────────────────────
echo ">>> Deploying frontend container app..."
FRONTEND_IMAGE="$ACR_LOGIN_SERVER/rfp-frontend:latest"

az containerapp create \
    --name "$FRONTEND_NAME" \
    --resource-group "$RG" \
    --environment "$ENV_NAME" \
    --image "$FRONTEND_IMAGE" \
    --registry-server "$ACR_LOGIN_SERVER" \
    --registry-identity "$IDENTITY_ID" \
    --target-port 3000 \
    --ingress external \
    --min-replicas 1 \
    --max-replicas 3 \
    --cpu 0.25 --memory 0.5Gi \
    -o none

FRONTEND_URL=$(az containerapp show \
    --name "$FRONTEND_NAME" \
    --resource-group "$RG" \
    --query "properties.configuration.ingress.fqdn" -o tsv)

echo "    Frontend URL: https://$FRONTEND_URL"

# Now create the SPA app registration with the real frontend URL
FRONTEND_APP_ID=$(az ad app create \
    --display-name "${PREFIX}-frontend" \
    --sign-in-audience AzureADMyOrg \
    --enable-id-token-issuance true \
    --query appId -o tsv)

# Configure SPA redirect URIs via REST API (az ad app create --web-redirect-uris
# sets web platform, not SPA platform)
az rest --method PATCH \
    --uri "https://graph.microsoft.com/v1.0/applications/$(az ad app show --id "$FRONTEND_APP_ID" --query id -o tsv)" \
    --headers "Content-Type=application/json" \
    --body "{
        \"spa\": {
            \"redirectUris\": [
                \"https://$FRONTEND_URL\",
                \"http://localhost:3000\"
            ]
        }
    }" \
    -o none

# Grant the frontend app permission to call the backend API
az ad app permission add \
    --id "$FRONTEND_APP_ID" \
    --api "$BACKEND_APP_ID" \
    --api-permissions "$SCOPE_ID=Scope" \
    -o none

echo "    Frontend App ID: $FRONTEND_APP_ID"

# ── 16. Rebuild Frontend with Auth Config ────────────────────────────────
echo ">>> Rebuilding frontend with Entra ID config..."
az acr build \
    --registry "$ACR_NAME" \
    --image "rfp-frontend:latest" \
    --file frontend/Dockerfile \
    --build-arg "NEXT_PUBLIC_API_URL=https://$APP_URL" \
    --build-arg "NEXT_PUBLIC_ENTRA_CLIENT_ID=$FRONTEND_APP_ID" \
    --build-arg "NEXT_PUBLIC_ENTRA_TENANT_ID=$TENANT_ID" \
    --build-arg "NEXT_PUBLIC_ENTRA_BACKEND_CLIENT_ID=$BACKEND_APP_ID" \
    --build-arg "NEXT_PUBLIC_ENTRA_REDIRECT_URI=https://$FRONTEND_URL" \
    frontend/ \
    -o none

# Update the frontend container app with the new image
az containerapp update \
    --name "$FRONTEND_NAME" \
    --resource-group "$RG" \
    --image "$FRONTEND_IMAGE" \
    -o none

# ── 17. Update orchestrator CORS with frontend URL ──────────────────────
echo ">>> Updating orchestrator CORS..."
az containerapp update \
    --name "$APP_NAME" \
    --resource-group "$RG" \
    --set-env-vars "FRONTEND_URL=https://$FRONTEND_URL" \
    -o none

# ── 18. Summary ──────────────────────────────────────────────────────────
echo ""
echo "=== Deployment Complete ==="
echo ""
echo "Frontend URL:             https://$FRONTEND_URL"
echo "Orchestrator URL:         https://$APP_URL"
echo "Pool Management Endpoint: $POOL_ENDPOINT"
echo "Managed Identity:         $IDENTITY_CLIENT_ID"
echo ""
echo "Entra ID (auth):"
echo "  Backend App ID:         $BACKEND_APP_ID"
echo "  Frontend App ID:        $FRONTEND_APP_ID"
echo "  Tenant ID:              $TENANT_ID"
echo ""
