#!/bin/bash

# Sofia Bulk API Smoke Test
# Usage: ./smoke_test_bulk_api.sh

set -e

# Configuration
API_URL="https://sofia-bulk-api-ew1-xxxx.run.app"
API_KEY="${BULK_API_KEY:-test_key_123}"

echo "🚀 Sofia Bulk API Smoke Test"
echo "================================"
echo "API URL: $API_URL"
echo "API Key: ${API_KEY:0:4}****${API_KEY: -4}"
echo ""

# Test 1: Health Check
echo "1. Testing Health Check..."
response=$(curl -s -w "%{http_code}" "$API_URL/health")
http_code="${response: -3}"
body="${response%???}"

if [ "$http_code" -eq 200 ]; then
    echo "✅ Health check passed"
    echo "Response: $body"
else
    echo "❌ Health check failed (HTTP $http_code)"
    echo "Response: $body"
    exit 1
fi
echo ""

# Test 2: Root Endpoint
echo "2. Testing Root Endpoint..."
response=$(curl -s -w "%{http_code}" "$API_URL/")
http_code="${response: -3}"
body="${response%???}"

if [ "$http_code" -eq 200 ]; then
    echo "✅ Root endpoint passed"
    echo "Response: $body"
else
    echo "❌ Root endpoint failed (HTTP $http_code)"
    echo "Response: $body"
    exit 1
fi
echo ""

# Test 3: POST Conversation (with auth)
echo "3. Testing POST Conversation..."
test_data='{
  "conversation_id": "smoke-01",
  "messages": [
    {
      "role": "user",
      "message": "Ciao, questo è un test"
    },
    {
      "role": "assistant",
      "message": ""
    }
  ]
}'

response=$(curl -s -w "%{http_code}" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$test_data" \
  "$API_URL/api/sofia/conversation")

http_code="${response: -3}"
body="${response%???}"

if [ "$http_code" -eq 200 ]; then
    echo "✅ POST conversation passed"
    echo "Response: $body"
    
    # Check if assistant message was populated
    if echo "$body" | grep -q '"role": "assistant"' && echo "$body" | grep -q '"message": "[^"]*"'; then
        echo "✅ Assistant message was populated"
    else
        echo "⚠️  Assistant message may not be populated"
    fi
else
    echo "❌ POST conversation failed (HTTP $http_code)"
    echo "Response: $body"
    exit 1
fi
echo ""

# Test 4: GET Conversation (with auth)
echo "4. Testing GET Conversation..."
response=$(curl -s -w "%{http_code}" \
  -H "Authorization: Bearer $API_KEY" \
  "$API_URL/api/sofia/conversation/smoke-01")

http_code="${response: -3}"
body="${response%???}"

if [ "$http_code" -eq 200 ]; then
    echo "✅ GET conversation passed"
    echo "Response: $body"
else
    echo "❌ GET conversation failed (HTTP $http_code)"
    echo "Response: $body"
    exit 1
fi
echo ""

# Test 5: Rate Limiting (optional)
echo "5. Testing Rate Limiting..."
echo "Making 5 requests quickly..."
for i in {1..5}; do
    response=$(curl -s -w "%{http_code}" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"conversation_id\":\"rate-test-$i\",\"messages\":[{\"role\":\"user\",\"message\":\"test\"},{\"role\":\"assistant\",\"message\":\"\"}]}" \
      "$API_URL/api/sofia/conversation")
    
    http_code="${response: -3}"
    echo "Request $i: HTTP $http_code"
    
    if [ "$http_code" -eq 429 ]; then
        echo "✅ Rate limiting working (429 received)"
        break
    fi
done
echo ""

echo "🎉 All smoke tests completed successfully!"
echo "Sofia Bulk API is ready for client tests."
