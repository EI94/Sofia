#!/bin/bash
# Sofia Lite - Load Test Runner

set -e

SOFIA_URL=${1:-"http://localhost:8000"}
TEST_TYPE=${2:-"standard"}

echo "🚀 Sofia Lite Load Test Runner"
echo "=============================="
echo "Target URL: $SOFIA_URL"
echo "Test Type: $TEST_TYPE"
echo ""

# Check if k6 is installed
if ! command -v k6 &> /dev/null; then
    echo "❌ k6 is not installed. Please install it first."
    exit 1
fi

echo "✅ k6 version: $(k6 version)"

# Health check
echo "🏥 Running health check..."
HEALTH_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/health_response.txt "$SOFIA_URL/health" || echo "000")
HTTP_CODE="${HEALTH_RESPONSE: -3}"

if [ "$HTTP_CODE" != "200" ]; then
    echo "❌ Health check failed (HTTP $HTTP_CODE)"
    exit 1
fi

echo "✅ Health check passed"

# Run test based on type
case $TEST_TYPE in
    "smoke")
        echo "💨 Running smoke test (1 VU, 30 seconds)..."
        k6 run --vus 1 --duration 30s k6_script.js
        ;;
    "quick")
        echo "⚡ Running quick test (5 VUs, 1 minute)..."
        k6 run --vus 5 --duration 1m k6_script.js
        ;;
    "standard")
        echo "📊 Running standard test (50 VUs, 5 minutes)..."
        k6 run k6_script.js
        ;;
    "stress")
        echo "🔥 Running stress test (100 VUs, 10 minutes)..."
        k6 run --vus 100 --duration 10m k6_script.js
        ;;
    *)
        echo "❌ Unknown test type: $TEST_TYPE"
        echo "Available types: smoke, quick, standard, stress"
        exit 1
        ;;
esac

echo "🚀 Sofia Lite load test completed successfully!"
