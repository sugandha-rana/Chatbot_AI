import requests
import json
import time

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

# Mock responder queries for testing
RESPONDER_QUERIES = [
    # Document Search Queries
    {
        "user_type": "responder",
        "query": "Show me emergency protocols"
    },
    {
        "user_type": "responder", 
        "query": "What are the safety guidelines?"
    },
    {
        "user_type": "responder",
        "query": "I need the medical response SOP"
    },
    {
        "user_type": "responder",
        "query": "Show me the venue map"
    },
    {
        "user_type": "responder",
        "query": "What are the FAQs for this event?"
    },
    # Dispatch Queries
    {
        "user_type": "responder",
        "query": "Dispatch to zone A"
    },
    {
        "user_type": "responder",
        "query": "Send help to food court"
    },
    {
        "user_type": "responder",
        "query": "Need assistance in exhibition hall B"
    },
    {
        "user_type": "responder",
        "query": "Emergency in outdoor plaza"
    },
    {
        "user_type": "responder",
        "query": "Dispatch to conference room 1"
    }
]

def test_responder_queries():
    """Test responder queries one by one"""
    print("🧪 Testing Responder Queries\n")
    
    for i, query_data in enumerate(RESPONDER_QUERIES, 1):
        print(f"📝 Test {i}: {query_data['query']}")
        print("-" * 50)
        
        try:
            response = requests.post(
                f"{BASE_URL}/generate",
                headers={"Content-Type": "application/json"},
                json=query_data
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success!")
                print(f"Response: {result['response']}")
                print(f"Session ID: {result['session_id']}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Error details: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print("\n" + "="*60 + "\n")
        time.sleep(1)  # Small delay between requests

def test_single_responder_query(query_text):
    """Test a single custom responder query"""
    query_data = {
        "user_type": "responder",
        "query": query_text
    }
    
    print(f"🔍 Testing: {query_text}")
    print("-" * 50)
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate",
            headers={"Content-Type": "application/json"},
            json=query_data
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success!")
            print(f"Response: {result['response']}")
            print(f"Session ID: {result['session_id']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Error details: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    print("🚀 CrowdGuard AI - Responder Query Tester")
    print("=" * 60)
    
    # Test all predefined queries
    test_responder_queries()
    
    # You can also test custom queries
    # test_single_responder_query("Your custom responder query here") 