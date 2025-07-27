# Session Management Example

## Simple Session IDs (1, 2, 3, etc.)

### First Request (Creates Session 1)
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "user", "query": "I lost my phone"}'
```

**Response:**
```json
{
  "response": "I understand you lost your phone...",
  "session_id": "1"
}
```

### Follow-up Request (Uses Session 1)
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "user", "query": "It is a black iPhone", "session_id": "1"}'
```

**Response:**
```json
{
  "response": "Thank you for the details about your black iPhone...",
  "session_id": "1"
}
```

### Another Follow-up (Continues Session 1)
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "user", "query": "I lost it in the food court", "session_id": "1"}'
```

## New Session (Session 2)
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "admin", "query": "How many users are there?"}'
```

**Response:**
```json
{
  "response": "Based on the data...",
  "session_id": "2"
}
```

## Benefits of Simple Session IDs:
- ✅ **Easy to remember**: 1, 2, 3, etc.
- ✅ **Short and clean**: No long UUIDs
- ✅ **Sequential**: Easy to track
- ✅ **Human-friendly**: Simple numbers 