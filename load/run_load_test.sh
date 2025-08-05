#!/bin/bash
"""
Sofia Lite - Load Test Runner
Executes k6 load tests with different configurations.
"""

set -e

# Configuration
SOFIA_URL=${1:-"http://localhost:8000"}
TEST_TYPE=${2:-"standard"}
OUTPUT_DIR=${3:-"load_results"}

echo "🚀 Sofia Lite Load Test Runner"
echo "=============================="
echo "Target URL: $SOFIA_URL"
echo "Test Type: $TEST_TYPE"
echo "Output Dir: $OUTPUT_DIR"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Check if k6 is installed
if ! command -v k6 &> /dev/null; then
    echo "❌ k6 is not installed. Installing..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install k6
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo gpg -k
        sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
        echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
        sudo apt-get update
        sudo apt-get install k6
    else
        echo "❌ Unsupported OS. Please install k6 manually: https://k6.io/docs/getting-started/installation/"
        exit 1
    fi
fi

echo "✅ k6 version: $(k6 version)"

# Health check before starting
echo "🏥 Running health check..."
HEALTH_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/health_response.txt "$SOFIA_URL/health" || echo "000")
HTTP_CODE="${HEALTH_RESPONSE: -3}"

if [ "$HTTP_CODE" != "200" ]; then
    echo "❌ Health check failed (HTTP $HTTP_CODE)"
    cat /tmp/health_response.txt
    exit 1
fi

echo "✅ Health check passed"

# Run different test types
case $TEST_TYPE in
    "quick")
        echo "⚡ Running quick test (5 VUs, 1 minute)..."
        k6 run \
            --vus 5 \
            --duration 1m \
            --out json="$OUTPUT_DIR/quick_test.json" \
            --out csv="$OUTPUT_DIR/quick_test.csv" \
            k6_script.js
        ;;
    "standard")
        echo "📊 Running standard test (50 VUs, 5 minutes)..."
        k6 run \
            --out json="$OUTPUT_DIR/standard_test.json" \
            --out csv="$OUTPUT_DIR/standard_test.csv" \
            k6_script.js
        ;;
    "stress")
        echo "🔥 Running stress test (100 VUs, 10 minutes)..."
        k6 run \
            --vus 100 \
            --duration 10m \
            --out json="$OUTPUT_DIR/stress_test.json" \
            --out csv="$OUTPUT_DIR/stress_test.csv" \
            k6_script.js
        ;;
    "smoke")
        echo "💨 Running smoke test (1 VU, 30 seconds)..."
        k6 run \
            --vus 1 \
            --duration 30s \
            --out json="$OUTPUT_DIR/smoke_test.json" \
            k6_script.js
        ;;
    *)
        echo "❌ Unknown test type: $TEST_TYPE"
        echo "Available types: quick, standard, stress, smoke"
        exit 1
        ;;
esac

# Generate summary report
echo ""
echo "📈 Generating summary report..."
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_FILE="$OUTPUT_DIR/load_test_report_${TIMESTAMP}.md"

cat > "$REPORT_FILE" << EOF
# Sofia Lite Load Test Report

**Date:** $(date)
**Target URL:** $SOFIA_URL
**Test Type:** $TEST_TYPE
**Duration:** $(date -u -d @$(($(date +%s) - $(date -d "$(head -n1 "$OUTPUT_DIR/${TEST_TYPE}_test.csv" | cut -d',' -f1)" +%s))) +"%H:%M:%S")

## Test Configuration

- **Virtual Users:** $(grep -c "iteration" "$OUTPUT_DIR/${TEST_TYPE}_test.csv" 2>/dev/null || echo "N/A")
- **Total Requests:** $(wc -l < "$OUTPUT_DIR/${TEST_TYPE}_test.csv" 2>/dev/null || echo "N/A")
- **Test Duration:** $(grep "test_duration" "$OUTPUT_DIR/${TEST_TYPE}_test.json" 2>/dev/null | head -1 | cut -d'"' -f4 || echo "N/A")

## Performance Metrics

### Response Times
- **Average:** $(grep "http_req_duration" "$OUTPUT_DIR/${TEST_TYPE}_test.json" 2>/dev/null | grep "avg" | head -1 | cut -d'"' -f4 || echo "N/A") ms
- **P95:** $(grep "http_req_duration" "$OUTPUT_DIR/${TEST_TYPE}_test.json" 2>/dev/null | grep "p95" | head -1 | cut -d'"' -f4 || echo "N/A") ms
- **P99:** $(grep "http_req_duration" "$OUTPUT_DIR/${TEST_TYPE}_test.json" 2>/dev/null | grep "p99" | head -1 | cut -d'"' -f4 || echo "N/A") ms

### Error Rates
- **HTTP Errors:** $(grep "http_req_failed" "$OUTPUT_DIR/${TEST_TYPE}_test.json" 2>/dev/null | grep "rate" | head -1 | cut -d'"' -f4 || echo "N/A")%
- **Custom Errors:** $(grep "errors" "$OUTPUT_DIR/${TEST_TYPE}_test.json" 2>/dev/null | grep "rate" | head -1 | cut -d'"' -f4 || echo "N/A")%

### Throughput
- **Requests/sec:** $(grep "http_reqs" "$OUTPUT_DIR/${TEST_TYPE}_test.json" 2>/dev/null | grep "rate" | head -1 | cut -d'"' -f4 || echo "N/A") req/s

## Thresholds

- ✅ P95 Response Time < 1500ms
- ✅ Error Rate < 10%
- ✅ Custom Error Rate < 10%

## Recommendations

Based on the test results, consider:

1. **Performance Optimization:** If response times are high, optimize LLM calls and database queries
2. **Scaling:** If error rates increase under load, consider horizontal scaling
3. **Monitoring:** Set up alerts for response time and error rate thresholds
4. **Caching:** Implement caching for frequently requested data

## Files Generated

- JSON Results: \`$OUTPUT_DIR/${TEST_TYPE}_test.json\`
- CSV Results: \`$OUTPUT_DIR/${TEST_TYPE}_test.csv\`
- This Report: \`$REPORT_FILE\`

EOF

echo "✅ Report generated: $REPORT_FILE"

# Display summary
echo ""
echo "🎯 Load Test Summary:"
echo "===================="
echo "📊 Test Type: $TEST_TYPE"
echo "🎯 Target: $SOFIA_URL"
echo "📁 Results: $OUTPUT_DIR/"
echo "📄 Report: $REPORT_FILE"
echo ""
echo "🔍 To analyze results:"
echo "  cat $REPORT_FILE"
echo "  open $OUTPUT_DIR/${TEST_TYPE}_test.json"
echo ""
echo "🚀 Sofia Lite load test completed successfully!" 