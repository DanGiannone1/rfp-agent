#!/usr/bin/env bash
set -e

if [[ ! -f .env ]]; then
    echo "Error: .env not found. Copy .env.example to .env and fill in values."
    exit 1
fi

set -a; source .env; set +a
export POOL_MANAGEMENT_ENDPOINT=http://localhost:8080
export WORKSPACE="$(pwd)/workspace"
mkdir -p workspace

cleanup() {
    echo ""
    echo "Shutting down..."
    kill $(jobs -p) 2>/dev/null
    wait 2>/dev/null
}
trap cleanup EXIT INT TERM

echo "Starting session container on :8080..."
(cd session-container && uv run uvicorn server:app --port 8080 --reload) &

echo "Starting orchestrator on :8000..."
uv run uvicorn app:app --port 8000 --reload &

echo "Starting frontend on :3000..."
(cd frontend && npm run dev) &

echo ""
echo "  Frontend:  http://localhost:3000"
echo "  API:       http://localhost:8000"
echo "  Session:   http://localhost:8080"
echo ""

wait
