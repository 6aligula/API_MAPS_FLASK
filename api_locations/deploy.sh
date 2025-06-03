#!/usr/bin/env bash
set -euo pipefail

IMAGE="gcr.io/senderos-dev/senderos-gps"
SERVICE="senderos-gps"
REGION="europe-west1"
PROJECT="senderos-dev"

# 1. Build
gcloud builds submit --tag "${IMAGE}"

# 2. Deploy
gcloud run deploy "${SERVICE}" \
  --image="${IMAGE}" \
  --region="${REGION}" \
  --platform=managed \
  --project="${PROJECT}" \
  --allow-unauthenticated \
  --execution-environment=gen2 \
  --timeout=120 \
  --memory=512Mi \
  --max-instances=3 \
  --set-env-vars=GCP_PROJECT="${PROJECT}"   

# 3. Health-check
URL=$(gcloud run services describe "${SERVICE}" \
        --platform=managed --region="${REGION}" \
        --format="value(status.url)")
echo "Deploy completo: $URL"

if curl -fsS "$URL/health" >/dev/null; then
  echo "✓ /health OK"
else
  echo "✗ /health falló" >&2
  exit 1
fi
