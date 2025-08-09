#!/bin/bash

# Script semplificato per configurare Workload Identity
set -e

PROJECT_ID="sofia-ai-464215"
GITHUB_REPO="EI94/Sofia"
SERVICE_ACCOUNT_NAME="github-actions-sa"
WORKLOAD_IDENTITY_POOL="github-actions-pool"
WORKLOAD_IDENTITY_PROVIDER="github-actions-provider"

echo "🔧 Configurazione Workload Identity semplificata"
echo "Progetto: $PROJECT_ID"
echo ""

# Abilita le API necessarie
echo "📡 Abilitazione API necessarie..."
gcloud services enable iamcredentials.googleapis.com --project=$PROJECT_ID
gcloud services enable iam.googleapis.com --project=$PROJECT_ID

# Assegna i ruoli necessari al service account esistente
echo "🔑 Assegnazione ruoli al service account..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.admin"

# Crea il Workload Identity Pool
echo "🏊 Creazione Workload Identity Pool..."
gcloud iam workload-identity-pools create $WORKLOAD_IDENTITY_POOL \
    --location="global" \
    --display-name="GitHub Actions Pool" \
    --description="Pool per GitHub Actions" \
    --project=$PROJECT_ID

# Crea il Workload Identity Provider
echo "🔗 Creazione Workload Identity Provider..."
gcloud iam workload-identity-pools providers create-oidc $WORKLOAD_IDENTITY_PROVIDER \
    --workload-identity-pool=$WORKLOAD_IDENTITY_POOL \
    --issuer-uri="https://token.actions.githubusercontent.com" \
    --location="global" \
    --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
    --attribute-condition="assertion.repository=='$GITHUB_REPO'" \
    --project=$PROJECT_ID

# Ottieni l'ID del provider
PROVIDER_ID=$(gcloud iam workload-identity-pools providers describe $WORKLOAD_IDENTITY_PROVIDER \
    --workload-identity-pool=$WORKLOAD_IDENTITY_POOL \
    --location="global" \
    --project=$PROJECT_ID \
    --format="value(name)")

# Ottieni il project number
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')

# Permetti al provider di impersonare il service account
echo "🔐 Configurazione permessi di impersonazione..."
gcloud iam service-accounts add-iam-policy-binding $SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com \
    --role="roles/iam.workloadIdentityUser" \
    --member="principalSet://iam.googleapis.com/projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/$WORKLOAD_IDENTITY_POOL/attribute.repository/$GITHUB_REPO" \
    --project=$PROJECT_ID

echo ""
echo "✅ Configurazione completata!"
echo ""
echo "📋 Secrets da configurare su GitHub:"
echo ""
echo "WIF_PROVIDER=$PROVIDER_ID"
echo "GCP_SA_EMAIL=$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com"
echo "GCP_PROJECT=$PROJECT_ID"
echo ""
echo "🔗 Vai su: https://github.com/$GITHUB_REPO/settings/secrets/actions"
echo "E aggiungi questi secrets."
