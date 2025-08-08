# Sofia - Root Makefile
# Comandi per build, test e deployment di tutti i servizi

.PHONY: help build test deploy clean build-monitor deploy-monitor build-bulk deploy-bulk

help:
	@echo "Sofia - Comandi disponibili:"
	@echo "  build         - Build dell'immagine Docker Sofia Lite"
	@echo "  test          - Esegue tutti i test unitari"
	@echo "  deploy        - Deploy Sofia Lite su Cloud Run"
	@echo "  build-monitor - Build dell'immagine Docker Monitor"
	@echo "  deploy-monitor - Deploy Monitor su Cloud Run"
	@echo "  build-bulk    - Build dell'immagine Docker Bulk API"
	@echo "  deploy-bulk   - Deploy Bulk API su Cloud Run"
	@echo "  clean         - Pulisce file temporanei"

# Sofia Lite targets
build:
	@echo "🔨 Building Sofia Lite Docker image..."
	cd Sofia-AI && gcloud builds submit --tag gcr.io/sofia-ai-464215/sofia-lite:latest

test:
	@echo "🧪 Running Sofia Lite unit tests..."
	cd Sofia-AI/sofia_lite && python -m pytest tests/ -v

deploy:
	@echo "🚀 Deploying Sofia Lite to Cloud Run..."
	cd Sofia-AI && gcloud run deploy sofia-lite \
		--image gcr.io/sofia-ai-464215/sofia-lite:latest \
		--platform managed \
		--region us-central1 \
		--allow-unauthenticated \
		--port 8000 \
		--memory 2Gi \
		--cpu 2 \
		--max-instances 10 \
		--set-env-vars GOOGLE_PROJECT_ID=sofia-ai-464215 \
		--set-secrets OPENAI_API_KEY=OPENAI_API_KEY:latest,TWILIO_ACCOUNT_SID=TWILIO_ACCOUNT_SID:latest,TWILIO_AUTH_TOKEN=TWILIO_AUTH_TOKEN:latest,ELEVENLABS_API_KEY=ELEVENLABS_API_KEY:latest,GOOGLE_APPLICATION_CREDENTIALS=GOOGLE_CREDENTIALS_JSON:latest

# Monitor targets
build-monitor:
	@echo "🔨 Building Monitor Docker image..."
	docker build -t sofia-monitor:latest -f monitoring/Dockerfile .

deploy-monitor:
	@echo "🚀 Deploying Monitor to Cloud Run..."
	gcloud run deploy sofia-monitor \
		--source monitoring \
		--region europe-west1 \
		--platform managed \
		--allow-unauthenticated \
		--port 8080 \
		--memory 1Gi \
		--cpu 1 \
		--max-instances 5

# Bulk API targets
build-bulk:
	@echo "🔨 Building Bulk API Docker image..."
	docker build -t sofia-bulk-api:latest -f Dockerfile .

deploy-bulk:
	@echo "🚀 Deploying Bulk API to Cloud Run..."
	gcloud run deploy sofia-bulk-api-ew1 \
		--image sofia-bulk-api:latest \
		--platform managed \
		--region europe-west1 \
		--allow-unauthenticated \
		--port 8080 \
		--memory 1Gi \
		--cpu 1 \
		--max-instances 10 \
		--set-env-vars BULK_API_KEY=$(BULK_API_KEY),CORE_SOFIA_URL=$(CORE_SOFIA_URL)

# Test targets
test-bulk:
	@echo "🧪 Running Bulk API tests..."
	python -m pytest tests_bulk/ -v -m bulk

test-all: test test-bulk
	@echo "✅ All tests completed!"

# Clean target
clean:
	@echo "🧹 Pulizia file temporanei..."
	rm -rf __pycache__
	rm -rf *.pyc
	rm -rf .pytest_cache
	rm -rf results/
	rm -rf hammer_env/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Full deployment targets
deploy-all: deploy deploy-monitor deploy-bulk
	@echo "✅ All services deployed!"

build-all: build build-monitor build-bulk
	@echo "✅ All images built!"

# Quick test targets
test-smoke:
	@echo "🧪 Running smoke tests..."
	./smoke_test_bulk_api.sh

# Help targets
show-env:
	@echo "🔧 Environment variables needed:"
	@echo "  BULK_API_KEY: API key for bulk API"
	@echo "  CORE_SOFIA_URL: URL of Sofia Core service"
	@echo "  GOOGLE_PROJECT_ID: Google Cloud Project ID"
