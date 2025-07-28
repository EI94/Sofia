# 🚀 SOFIA AI - PRODUCTION DEPLOYMENT GUIDE

**Complete Step-by-Step Guide for Production Deployment**

---

## 📋 **Prerequisites Checklist**

Before deploying Sofia AI to production, ensure you have:

### **🔑 Required Accounts & API Keys**
- [ ] **OpenAI Account** with API key and sufficient credits
- [ ] **Twilio Account** with WhatsApp Business API enabled
- [ ] **Google Cloud Project** with Firestore and Vision API enabled
- [ ] **ElevenLabs Account** (optional, for advanced TTS)

### **🛠️ Development Tools**
- [ ] **Docker & Docker Compose** installed locally
- [ ] **Git** repository access
- [ ] **Cloud CLI** for your chosen platform (gcloud, Railway CLI, etc.)
- [ ] **SSH access** (for VPS deployment)

---

## 🎯 **STEP 1: Pre-Deployment Preparation**

### **1.1 Clone and Setup Repository**
```bash
git clone https://github.com/your-org/sofia-ai.git
cd sofia-ai
```

### **1.2 Configure Production Environment**
```bash
# Copy the production config template
cp config-production.env .env.production

# Edit with your actual values
nano .env.production
```

**Required Configuration:**
```env
# AI Configuration
OPENAI_API_KEY=sk-your-production-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.3

# Twilio Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your-production-twilio-auth-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
TWILIO_VOICE_NUMBER=+18149149892

# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=/app/keys/sofia-production-sa.json
FIRESTORE_PROJECT_ID=sofia-ai-production
GOOGLE_CLOUD_PROJECT=sofia-ai-production

# ElevenLabs (Optional)
ELEVENLABS_API_KEY=your-elevenlabs-api-key
USE_ELEVENLABS_TTS=true
SOFIA_VOICE_NAME=sarah

# Security
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

### **1.3 Test Build Locally**
```bash
# Test the production Docker build
docker build -f Dockerfile.production -t sofia-ai:test .

# Verify the build
docker run --rm sofia-ai:test python -c "import app.main; print('✅ Build OK')"

# Cleanup
docker rmi sofia-ai:test
```

---

## 🌐 **STEP 2: Choose Your Deployment Platform**

### **Option A: Google Cloud Run (Recommended)**

**Best for:** Auto-scaling, pay-per-use, enterprise-grade

#### **2A.1 Setup Google Cloud**
```bash
# Install Google Cloud SDK (if not installed)
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Authenticate
gcloud auth login

# Create or select project
gcloud projects create sofia-ai-production
gcloud config set project sofia-ai-production

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable vision.googleapis.com
```

#### **2A.2 Deploy to Cloud Run**
```bash
# Use the automated deploy script
chmod +x deploy.sh
./deploy.sh

# Select option 1 (Google Cloud Run)
# Follow the prompts
```

#### **2A.3 Manual Cloud Run Deploy** (Alternative)
```bash
gcloud run deploy sofia-ai \
    --source . \
    --dockerfile Dockerfile.production \
    --platform managed \
    --region europe-west1 \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 100 \
    --timeout 300 \
    --concurrency 1000 \
    --env-vars-file .env.production
```

---

### **Option B: Railway**

**Best for:** Simple deployment, fixed pricing, quick setup

#### **2B.1 Setup Railway**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login
```

#### **2B.2 Deploy to Railway**
```bash
# Use the automated deploy script
./deploy.sh

# Select option 2 (Railway)
# Follow the prompts
```

---

### **Option C: DigitalOcean/VPS**

**Best for:** Full control, predictable costs, custom configurations

#### **2C.1 Prepare Your VPS**
```bash
# Connect to your VPS
ssh root@your-server-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

#### **2C.2 Deploy to VPS**
```bash
# Use the automated deploy script from your local machine
./deploy.sh

# Select option 3 (DigitalOcean/VPS)
# Enter your server details
```

---

## ⚙️ **STEP 3: Configure Twilio Webhooks**

### **3.1 WhatsApp Configuration**
1. **Login to Twilio Console**: https://console.twilio.com/
2. **Navigate to Messaging > Try it out > Send a WhatsApp message**
3. **Configure Webhook URL**: `https://your-domain.com/webhook/whatsapp`
4. **Set HTTP Method**: POST
5. **Test the integration**

### **3.2 Voice Configuration**
1. **Navigate to Phone Numbers > Manage > Active numbers**
2. **Select your Twilio phone number**
3. **Configure Voice webhook**: `https://your-domain.com/webhook/voice/inbound`
4. **Set HTTP Method**: POST
5. **Test with a phone call**

---

## 📊 **STEP 4: Setup Monitoring (Optional but Recommended)**

### **4.1 Deploy Monitoring Stack**
```bash
# Navigate to monitoring directory
cd monitoring/

# Start monitoring services
docker-compose -f docker-compose.monitoring.yml up -d
```

### **4.2 Access Monitoring Dashboards**
- **Grafana**: http://your-domain:3000 (admin/sofia-admin-2024)
- **Prometheus**: http://your-domain:9090
- **AlertManager**: http://your-domain:9093
- **Uptime Kuma**: http://your-domain:3001

### **4.3 Configure Alerts**
Edit `monitoring/alertmanager.yml` to configure:
- Email notifications
- Slack integrations
- Custom webhook endpoints

---

## 🧪 **STEP 5: Production Testing**

### **5.1 Health Checks**
```bash
# Basic health check
curl https://your-domain.com/health

# Detailed health check
curl https://your-domain.com/api/health/detailed

# Metrics endpoint
curl https://your-domain.com/api/health/metrics
```

### **5.2 End-to-End Testing**
```bash
# Test WhatsApp integration
curl -X POST https://your-domain.com/api/health/integration-test

# Test Voice capabilities
curl https://your-domain.com/webhook/voice/test
```

### **5.3 Load Testing**
```bash
# Install Apache Bench (if needed)
sudo apt-get install apache2-utils

# Run load test
ab -n 1000 -c 10 https://your-domain.com/health
```

---

## 🔒 **STEP 6: Security Hardening**

### **6.1 SSL/TLS Configuration**
- **Cloud Run**: Automatic HTTPS
- **Railway**: Automatic HTTPS
- **VPS**: Configure reverse proxy (Nginx) with Let's Encrypt

### **6.2 Environment Variables**
Ensure all sensitive data is properly configured:
```bash
# Verify no secrets in logs
docker logs sofia-ai | grep -i "api.*key" || echo "✅ No API keys in logs"
```

### **6.3 Firewall Configuration** (VPS only)
```bash
# Configure UFW firewall
sudo ufw allow 22     # SSH
sudo ufw allow 80     # HTTP
sudo ufw allow 443    # HTTPS
sudo ufw enable
```

---

## 📈 **STEP 7: Performance Optimization**

### **7.1 Resource Monitoring**
Monitor these key metrics:
- **Response Time**: < 2 seconds average
- **Memory Usage**: < 80% of allocated
- **CPU Usage**: < 70% sustained
- **Error Rate**: < 1%

### **7.2 Auto-Scaling Configuration**

#### **Google Cloud Run**
```bash
gcloud run services update sofia-ai \
    --region europe-west1 \
    --min-instances 1 \
    --max-instances 50 \
    --concurrency 1000
```

#### **VPS with Docker Swarm**
```bash
# Initialize swarm
docker swarm init

# Deploy as a service with scaling
docker service create \
    --name sofia-ai \
    --replicas 3 \
    --publish 8000:8000 \
    sofia-ai:latest
```

---

## 🚨 **STEP 8: Backup & Disaster Recovery**

### **8.1 Automated Backups**
```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Backup configuration
tar -czf "$BACKUP_DIR/sofia-config-$DATE.tar.gz" .env.production monitoring/

# Backup logs (last 7 days)
find /var/log -name "*sofia*" -mtime -7 -exec tar -czf "$BACKUP_DIR/sofia-logs-$DATE.tar.gz" {} +

echo "Backup completed: $DATE"
EOF

chmod +x backup.sh

# Schedule daily backups
echo "0 2 * * * /path/to/backup.sh" | crontab -
```

### **8.2 Recovery Procedures**
Create disaster recovery runbook:
```bash
# Quick recovery commands
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d --force-recreate
```

---

## 🎯 **STEP 9: Go-Live Checklist**

### **Pre-Launch**
- [ ] All tests passing
- [ ] Monitoring configured and active
- [ ] SSL certificates valid
- [ ] Twilio webhooks configured
- [ ] Backup procedures tested
- [ ] Emergency contacts notified

### **Launch Day**
- [ ] Deploy to production
- [ ] Verify all endpoints responding
- [ ] Test WhatsApp and Voice flows
- [ ] Monitor for 1 hour post-deployment
- [ ] Send test messages/calls

### **Post-Launch**
- [ ] Monitor performance metrics for 24 hours
- [ ] Review logs for any errors
- [ ] Validate billing/usage patterns
- [ ] Document any issues and resolutions

---

## 📞 **STEP 10: Support & Maintenance**

### **10.1 Daily Operations**
- Monitor Grafana dashboards
- Review error logs
- Check Twilio usage
- Verify OpenAI credit balance

### **10.2 Weekly Maintenance**
- Update dependencies (if needed)
- Review performance metrics
- Test backup/recovery procedures
- Update documentation

### **10.3 Emergency Procedures**
```bash
# Quick health diagnosis
curl https://your-domain.com/api/health/detailed

# Restart application
docker-compose -f docker-compose.prod.yml restart sofia-ai

# View recent logs
docker-compose -f docker-compose.prod.yml logs --tail=100 sofia-ai

# Rollback to previous version
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🎉 **Success! Sofia AI is Production Ready**

Your Sofia AI deployment is now live and ready to handle:
- ✅ **24/7 WhatsApp conversations**
- ✅ **Voice call interactions** 
- ✅ **Multi-language support**
- ✅ **Enterprise-grade monitoring**
- ✅ **Auto-scaling capabilities**
- ✅ **Comprehensive error handling**

**Next Steps:**
1. Configure custom domain (if needed)
2. Set up advanced analytics
3. Customize responses for your use case
4. Scale based on usage patterns

**Need Help?**
- 📧 Email: support@sofia-ai.com
- 📚 Documentation: https://docs.sofia-ai.com
- 💬 Community: https://discord.gg/sofia-ai

---

**🌟 Congratulations! Sofia AI is now serving your customers with intelligent, multi-channel AI assistance!** 