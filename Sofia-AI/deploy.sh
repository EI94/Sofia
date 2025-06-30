#!/bin/bash

# Script di deploy per Sofia AI in produzione

echo "🚀 Deploy Sofia AI in Produzione"

# 1. Railway (raccomandato)
deploy_railway() {
    echo "📡 Deploy su Railway..."
    railway login
    railway init
    railway add
    railway up
    echo "✅ Sofia AI deployata su Railway!"
    echo "🔗 URL: https://sofia-ai.railway.app"
}

# 2. Google Cloud Run
deploy_gcp() {
    echo "☁️ Deploy su Google Cloud Run..."
    gcloud auth login
    gcloud config set project sofia-ai-464215
    gcloud run deploy sofia-ai \
        --source . \
        --region europe-west1 \
        --allow-unauthenticated \
        --set-env-vars="OPENAI_API_KEY=$OPENAI_API_KEY,TWILIO_ACCOUNT_SID=$TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN=$TWILIO_AUTH_TOKEN"
    echo "✅ Sofia AI deployata su Google Cloud Run!"
}

# 3. DigitalOcean VPS
deploy_vps() {
    echo "🖥️ Deploy su VPS..."
    # Copia file sul server
    scp -r . root@your-server-ip:/opt/sofia-ai/
    
    # Comandi remoti
    ssh root@your-server-ip << 'EOF'
        cd /opt/sofia-ai
        docker-compose -f docker-compose.prod.yml down
        docker-compose -f docker-compose.prod.yml up -d --build
        echo "✅ Sofia AI attiva su VPS!"
EOF
}

# Menu di scelta
echo "Scegli piattaforma di deploy:"
echo "1) Railway (raccomandato - $5/mese)"
echo "2) Google Cloud Run (pay-per-use)"
echo "3) DigitalOcean VPS ($12/mese)"
read -p "Scelta [1-3]: " choice

case $choice in
    1) deploy_railway ;;
    2) deploy_gcp ;;
    3) deploy_vps ;;
    *) echo "Scelta non valida" ;;
esac

echo ""
echo "🎯 Setup Twilio Webhook:"
echo "URL: https://your-domain.com/webhook/whatsapp"
echo ""
echo "🔧 Configurazione completata!" 