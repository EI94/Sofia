import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const responseTime = new Trend('response_time');

// Test configuration
export const options = {
  stages: [
    { duration: '1m', target: 10 },  // Ramp up to 10 VUs
    { duration: '2m', target: 50 },  // Ramp up to 50 VUs
    { duration: '5m', target: 50 },  // Stay at 50 VUs for 5 minutes
    { duration: '1m', target: 0 },   // Ramp down to 0 VUs
  ],
  thresholds: {
    http_req_duration: ['p(95)<1500'], // 95% of requests must complete below 1500ms
    http_req_failed: ['rate<0.1'],     // Error rate must be less than 10%
    errors: ['rate<0.1'],              // Custom error rate must be less than 10%
  },
};

// Sofia Lite conversation flow
const CONVERSATION_FLOW = [
  { message: "Ciao", expected_state: "ASK_NAME" },
  { message: "Mi chiamo Mario Rossi", expected_state: "ASK_SERVICE" },
  { message: "Ho bisogno di un permesso di soggiorno", expected_state: "PROPOSE_CONSULT" },
  { message: "Sì, voglio prenotare", expected_state: "ASK_CHANNEL" },
  { message: "Online", expected_state: "ASK_SLOT" },
  { message: "Domani alle 15:00", expected_state: "ASK_PAYMENT" },
  { message: "Sì, confermo", expected_state: "CONFIRMED" },
];

// Helper function to extract state from response
function extractState(response) {
  try {
    const body = response.body;
    // Look for state indicators in the response
    if (body.includes("Come ti chiami") || body.includes("What's your name")) {
      return "ASK_NAME";
    } else if (body.includes("permesso di soggiorno") || body.includes("cittadinanza") || body.includes("ricongiungimento")) {
      return "ASK_SERVICE";
    } else if (body.includes("60€") || body.includes("consulenza")) {
      return "PROPOSE_CONSULT";
    } else if (body.includes("online") || body.includes("in presenza")) {
      return "ASK_CHANNEL";
    } else if (body.includes("orari") || body.includes("disponibilità")) {
      return "ASK_SLOT";
    } else if (body.includes("pagamento") || body.includes("IBAN")) {
      return "ASK_PAYMENT";
    } else if (body.includes("confermata") || body.includes("prenotazione")) {
      return "CONFIRMED";
    }
    return "UNKNOWN";
  } catch (e) {
    return "ERROR";
  }
}

// Helper function to generate unique phone number
function generatePhoneNumber() {
  const prefix = "+39";
  const number = Math.floor(Math.random() * 900000000) + 100000000;
  return `${prefix}${number}`;
}

// Main test function
export default function () {
  const baseUrl = __ENV.SOFIA_URL || 'http://localhost:8000';
  const phone = generatePhoneNumber();
  let conversationErrors = 0;
  let totalResponseTime = 0;

  // Simulate complete conversation flow
  for (let i = 0; i < CONVERSATION_FLOW.length; i++) {
    const step = CONVERSATION_FLOW[i];
    const payload = {
      From: `whatsapp:${phone}`,
      Body: step.message,
    };

    const startTime = Date.now();
    
    const response = http.post(`${baseUrl}/webhook/whatsapp`, payload, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      timeout: '10s',
    });

    const endTime = Date.now();
    const responseTimeMs = endTime - startTime;
    totalResponseTime += responseTimeMs;

    // Check response
    const success = check(response, {
      'status is 200': (r) => r.status === 200,
      'response has body': (r) => r.body.length > 0,
      'response time < 1500ms': (r) => r.timings.duration < 1500,
    });

    // Extract and verify state
    const actualState = extractState(response);
    const stateCheck = check(response, {
      [`state is ${step.expected_state}`]: (r) => actualState === step.expected_state,
    });

    if (!success || !stateCheck) {
      conversationErrors++;
      console.log(`❌ Step ${i + 1} failed for ${phone}: expected=${step.expected_state}, actual=${actualState}`);
    } else {
      console.log(`✅ Step ${i + 1} passed for ${phone}: ${step.expected_state}`);
    }

    // Record metrics
    errorRate.add(!success);
    responseTime.add(responseTimeMs);

    // Sleep between messages to simulate real user behavior
    sleep(Math.random() * 2 + 1); // 1-3 seconds
  }

  // Log conversation summary
  if (conversationErrors === 0) {
    console.log(`🎉 Complete conversation successful for ${phone} (${totalResponseTime}ms total)`);
  } else {
    console.log(`⚠️ Conversation had ${conversationErrors} errors for ${phone}`);
  }
}

// Setup function (runs once before the test)
export function setup() {
  console.log('🚀 Starting Sofia Lite Load Test');
  console.log(`📊 Configuration: ${options.stages.length} stages, max ${Math.max(...options.stages.map(s => s.target))} VUs`);
  console.log(`🎯 Thresholds: p95 < 1500ms, error rate < 10%`);
  
  // Test endpoint availability
  const baseUrl = __ENV.SOFIA_URL || 'http://localhost:8000';
  const healthCheck = http.get(`${baseUrl}/health`);
  
  if (healthCheck.status !== 200) {
    throw new Error(`Health check failed: ${healthCheck.status}`);
  }
  
  console.log('✅ Health check passed, starting load test...');
  return { baseUrl };
}

// Teardown function (runs once after the test)
export function teardown(data) {
  console.log('🏁 Load test completed');
  console.log('📈 Check the metrics above for performance analysis');
} 