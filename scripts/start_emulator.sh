#!/bin/bash
"""
Sofia Lite - Firestore Emulator Starter
Starts Firestore emulator for local E2E testing.
"""

set -e

echo "🚀 Starting Firestore Emulator for Sofia Lite E2E Tests"
echo "=================================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK not found. Please install it first:"
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "⚠️  Not authenticated with gcloud. Running with default credentials..."
fi

# Set environment variables
export FIRESTORE_EMULATOR_HOST=localhost:8080
export GOOGLE_CLOUD_PROJECT=test-project
export GOOGLE_APPLICATION_CREDENTIALS=/dev/null

echo "📋 Environment variables set:"
echo "   FIRESTORE_EMULATOR_HOST=$FIRESTORE_EMULATOR_HOST"
echo "   GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT"
echo "   GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS"

# Start Firestore emulator
echo "🔥 Starting Firestore emulator..."
gcloud emulators firestore start \
    --host-port=localhost:8080 \
    --project=test-project \
    --quiet

echo "✅ Firestore emulator started successfully!"
echo "📊 Emulator running on: http://localhost:8080"
echo ""
echo "🧪 To run E2E tests:"
echo "   python scripts/run_e2e.py"
echo ""
echo "🛑 To stop emulator: Ctrl+C" 