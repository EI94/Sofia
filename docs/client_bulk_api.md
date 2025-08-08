# Sofia Bulk API - Client Documentation

## Overview

Sofia Bulk API è un micro-servizio REST per test bulk conversazioni con l'assistente Sofia. Permette di processare conversazioni multiple e completare automaticamente i messaggi assistant vuoti.

## Quick Start

### Base URL
```
https://sofia-bulk-api-ew1-xxxx.run.app
```

### Authentication
Tutte le richieste richiedono autenticazione Bearer token:
```bash
Authorization: Bearer YOUR_API_KEY
```

### Swagger Documentation
📖 **API Documentation**: https://sofia-bulk-api-ew1-xxxx.run.app/docs

## Endpoints

### POST /api/sofia/conversation
Processa una conversazione e completa i messaggi assistant vuoti.

**Request Body:**
```json
{
  "conversation_id": "conv_123",
  "messages": [
    {
      "role": "user",
      "message": "Ciao, mi chiamo Mario"
    },
    {
      "role": "assistant",
      "message": ""
    },
    {
      "role": "user", 
      "message": "Vorrei informazioni sulla cittadinanza"
    },
    {
      "role": "assistant",
      "message": ""
    }
  ]
}
```

**Response:**
```json
{
  "conversation_id": "conv_123",
  "messages": [
    {
      "role": "user",
      "message": "Ciao, mi chiamo Mario"
    },
    {
      "role": "assistant",
      "message": "Ciao Mario! Sono Sofia di Studio Immigrato. Come posso aiutarti?"
    },
    {
      "role": "user",
      "message": "Vorrei informazioni sulla cittadinanza"
    },
    {
      "role": "assistant",
      "message": "Perfetto! Ti spiego i requisiti per la cittadinanza italiana..."
    }
  ],
  "timestamp_utc": "2025-08-07T12:00:00Z"
}
```

### GET /api/sofia/conversation/{conversation_id}
Recupera una conversazione salvata.

**Response:** Stesso formato del POST response.

## Rate Limiting

⚠️ **Rate Limit**: 10 requests/second per API key

**Headers di risposta:**
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 9
X-RateLimit-Reset: 1234567890
```

**Error Response (429):**
```json
{
  "error": "Rate limit exceeded",
  "detail": "Troppe richieste. Limite: 10/second per API key"
}
```

## Usage Examples

### cURL Example
```bash
curl -X POST https://sofia-bulk-api-ew1-xxxx.run.app/api/sofia/conversation \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d @conversation.json
```

### Python Example
```python
import requests
import json

url = "https://sofia-bulk-api-ew1-xxxx.run.app/api/sofia/conversation"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

data = {
    "conversation_id": "test_conv_001",
    "messages": [
        {"role": "user", "message": "Ciao"},
        {"role": "assistant", "message": ""}
    ]
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(json.dumps(result, indent=2))
```

### JavaScript Example
```javascript
const response = await fetch('https://sofia-bulk-api-ew1-xxxx.run.app/api/sofia/conversation', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    conversation_id: 'test_conv_001',
    messages: [
      {role: 'user', message: 'Ciao'},
      {role: 'assistant', message: ''}
    ]
  })
});

const result = await response.json();
console.log(result);
```

## How to Download Responses

### Save to File
```bash
curl -X POST https://sofia-bulk-api-ew1-xxxx.run.app/api/sofia/conversation \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d @conversation.json \
  -o response.json
```

### Python - Save Multiple Responses
```python
import requests
import json
from datetime import datetime

def save_conversation(conversation_id, messages, api_key):
    url = "https://sofia-bulk-api-ew1-xxxx.run.app/api/sofia/conversation"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "conversation_id": conversation_id,
        "messages": messages
    }
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    # Save to file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversation_{conversation_id}_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(result, f, indent=2)
    
    return filename

# Example usage
conversations = [
    {
        "id": "conv_001",
        "messages": [
            {"role": "user", "message": "Ciao"},
            {"role": "assistant", "message": ""}
        ]
    },
    {
        "id": "conv_002", 
        "messages": [
            {"role": "user", "message": "Informazioni cittadinanza"},
            {"role": "assistant", "message": ""}
        ]
    }
]

for conv in conversations:
    filename = save_conversation(conv["id"], conv["messages"], "YOUR_API_KEY")
    print(f"Saved: {filename}")
```

## Error Handling

### Common Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| 401 | Unauthorized | Check API key |
| 403 | Forbidden | Missing Authorization header |
| 429 | Too Many Requests | Wait and retry |
| 500 | Internal Server Error | Contact support |

### Error Response Format
```json
{
  "error": "Error type",
  "detail": "Detailed error message"
}
```

## Best Practices

1. **Rate Limiting**: Implement exponential backoff for 429 errors
2. **Conversation IDs**: Use unique, descriptive IDs
3. **Message Format**: Keep user messages clear and specific
4. **Error Handling**: Always check response status codes
5. **Data Storage**: Save responses locally for analysis

## Support

Per supporto tecnico o domande:
- 📧 Email: team@sofia.ai
- 🐛 Issues: https://github.com/EI94/Sofia/issues
- 📖 Docs: https://sofia-bulk-api-ew1-xxxx.run.app/docs
