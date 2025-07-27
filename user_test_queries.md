# User Query Test Commands

## Quick Test Commands (curl)

### Incident Report Queries

#### 1. Lost Phone Report
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "user", "query": "I lost my phone at the event"}'
```

#### 2. Injury Report
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "user", "query": "I need to report an injury"}'
```

#### 3. Security Issue Report
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "user", "query": "Someone is causing trouble in the crowd"}'
```

#### 4. Lost Wallet Report
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "user", "query": "I lost my wallet with my ID inside"}'
```

#### 5. Medical Emergency Report
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "user", "query": "There is a medical emergency in zone A"}'
```

### Lost and Found Queries

#### 6. Search for Phone
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "user", "query": "Has anyone found a black phone?"}'
```

#### 7. Search for Wallet
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "user", "query": "I am looking for my lost wallet"}'
```

#### 8. Search for Jacket
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "user", "query": "Did anyone find a red jacket?"}'
```

#### 9. Search for Keys
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "user", "query": "I lost my keys, has anyone seen them?"}'
```

#### 10. Search for Backpack
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "user", "query": "Looking for a blue backpack"}'
```

## Python Test Script

You can also run the Python test script:
```bash
cd Chatbot_AI
python test_user_queries.py
```

## Custom User Queries

You can test any custom user query by replacing the "query" value:
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "user", "query": "YOUR_CUSTOM_USER_QUERY_HERE"}'
```

## User Tool Features

### Incident Report Tool:
- Reports lost items
- Reports injuries
- Reports security issues
- Reports medical emergencies
- Generates unique report IDs

### Lost and Found Tool:
- Searches for lost items
- Matches descriptions
- Shows location where items were found
- Provides helpful responses 