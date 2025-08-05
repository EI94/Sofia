# Sofia Lite - Makefile
# Comandi per build, test e deployment

.PHONY: help build test deploy hammer clean

help:
	@echo "Sofia Lite - Comandi disponibili:"
	@echo "  build   - Build dell'immagine Docker"
	@echo "  test    - Esegue tutti i test unitari"
	@echo "  deploy  - Deploy su Cloud Run"
	@echo "  hammer  - Esegue Hammer Test Runner (100 conversazioni reali)"
	@echo "  clean   - Pulisce file temporanei"

build:
	@echo "🔨 Building Docker image..."
	gcloud builds submit --tag gcr.io/sofia-ai-464215/sofia-lite:latest

test:
	@echo "🧪 Running unit tests..."
	cd sofia_lite && python -m pytest tests/ -v

deploy:
	@echo "🚀 Deploying to Cloud Run..."
	gcloud run deploy sofia-lite \
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

hammer:
	@echo "🔨 Avvio Hammer Test Runner..."
	@echo "📋 Verifica credenziali Twilio..."
	@if [ -z "$$TWILIO_ACCOUNT_SID" ] || [ -z "$$TWILIO_AUTH_TOKEN" ]; then \
		echo "❌ Credenziali Twilio mancanti. Imposta:"; \
		echo "   export TWILIO_ACCOUNT_SID=your_account_sid"; \
		echo "   export TWILIO_AUTH_TOKEN=your_auth_token"; \
		exit 1; \
	fi
	@echo "✅ Credenziali Twilio trovate"
	@echo "🐍 Creazione ambiente virtuale..."
	python3 -m venv hammer_env
	@echo "📦 Installazione dipendenze..."
	hammer_env/bin/pip install -r requirements.txt
	hammer_env/bin/pip install twilio pyyaml requests
	@echo "🚀 Esecuzione Hammer Test Runner..."
	@if [ -n "$$FROM_NUM" ]; then \
		echo "📞 Usando numero FROM: $$FROM_NUM"; \
		TWILIO_FROM_WHATSAPP="$$FROM_NUM" TWILIO_FROM_VOICE="$$FROM_NUM" hammer_env/bin/python scripts/hammer_live_tests.py; \
	else \
		echo "📞 Usando numero di default"; \
		hammer_env/bin/python scripts/hammer_live_tests.py; \
	fi
	@echo "🧹 Pulizia ambiente..."
	rm -rf hammer_env

hammer-prod:
	@echo "🔨 Avvio Hammer Production Test Runner..."
	@echo "📋 Verifica credenziali ambiente..."
	@if [ -z "$$OPENAI_API_KEY" ] || [ -z "$$TWILIO_ACCOUNT_SID" ] || [ -z "$$TWILIO_AUTH_TOKEN" ]; then \
		echo "❌ Credenziali ambiente mancanti. Imposta:"; \
		echo "   export OPENAI_API_KEY=your_openai_key"; \
		echo "   export TWILIO_ACCOUNT_SID=your_account_sid"; \
		echo "   export TWILIO_AUTH_TOKEN=your_auth_token"; \
		exit 1; \
	fi
	@echo "✅ Credenziali ambiente trovate"
	@echo "🚀 Esecuzione Hammer Production Test..."
	@if [ -n "$$n" ]; then \
		echo "📊 Esecuzione $$n scenari..."; \
		SCENARIOS=$$n python scripts/hammer_live_tests.py; \
	else \
		echo "📊 Esecuzione 40 scenari di default..."; \
		python scripts/hammer_live_tests.py; \
	fi
	@if [ -n "$$to" ]; then \
		echo "📞 Usando numero TO: $$to"; \
		export TWILIO_TO_TEST="$$to"; \
	fi
	@if [ -n "$$msid" ]; then \
		echo "🔧 Usando MSID: $$msid"; \
		export TWILIO_MSID="$$msid"; \
	fi
	@if [ -n "$$outfile" ]; then \
		echo "📄 Output salvato in: $$outfile"; \
	fi
	@if [ -n "$$p95" ]; then \
		echo "📊 Calcolo P95 abilitato"; \
	fi

clean:
	@echo "🧹 Pulizia file temporanei..."
	rm -rf __pycache__
	rm -rf *.pyc
	rm -rf .pytest_cache
	rm -rf results/
	rm -rf hammer_env/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Comando per test rapido
quick-test:
	@echo "⚡ Test rapido Sofia..."
	curl -X POST https://sofia-lite-1075574333382.us-central1.run.app/webhook/whatsapp \
		-H "Content-Type: application/x-www-form-urlencoded" \
		-d "From=whatsapp:+393001234567&Body=ciao" | jq .

# Comando per monitoraggio logs
logs:
	@echo "📊 Monitoraggio logs Cloud Run..."
	gcloud beta logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=sofia-lite" \
		--format="table(timestamp,severity,textPayload)"

# Comando per build e deploy completo
full-deploy: build deploy
	@echo "✅ Build e deploy completati!"

# Comando per test completo
full-test: test hammer
	@echo "✅ Tutti i test completati!" 