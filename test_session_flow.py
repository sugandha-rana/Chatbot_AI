import requests
import json
import time

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

def test_session_flow():
    """Test a conversation flow with session management"""
    print("🧪 Testing Session Flow with Follow-up Questions\n")
    
    # Test conversation flow
    conversation = [
        {
            "user_type": "user",
            "query": "I lost my phone"
        },
        {
            "user_type": "user", 
            "query": "It's a black iPhone"
        },
        {
            "user_type": "user",
            "query": "I lost it in the food court"
        },
        {
            "user_type": "user",
            "query": "About 30 minutes ago"
        }
    ]
    
    session_id = None
    
    for i, query_data in enumerate(conversation, 1):
        print(f"📝 Turn {i}: {query_data['query']}")
        print("-" * 50)
        
        # Add session_id to subsequent requests
        if session_id:
            query_data["session_id"] = session_id
        
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
                print(f"Session ID: {result['session_id']} (Simple number)")
                
                # Store session_id for next request
                session_id = result['session_id']
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Error details: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print("\n" + "="*60 + "\n")
        time.sleep(1)  # Small delay between requests

def test_lost_and_found_search():
    """Test searching for lost items with session"""
    print("🔍 Testing Lost and Found Search with Session\n")
    
    conversation = [
        {
            "user_type": "user",
            "query": "Has anyone found a black phone?"
        },
        {
            "user_type": "user",
            "query": "What about a wallet?"
        },
        {
            "user_type": "user",
            "query": "Any bags found?"
        }
    ]
    
    session_id = None
    
    for i, query_data in enumerate(conversation, 1):
        print(f"📝 Search {i}: {query_data['query']}")
        print("-" * 50)
        
        if session_id:
            query_data["session_id"] = session_id
        
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
                print(f"Session ID: {result['session_id']} (Simple number)")
                
                session_id = result['session_id']
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Error details: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print("\n" + "="*60 + "\n")
        time.sleep(1)

if __name__ == "__main__":
    print("🚀 CrowdGuard AI - Session Flow Tester")
    print("=" * 60)
    
    # Test conversation flow
    test_session_flow()
    
    print("\n" + "="*60 + "\n")
    
    # Test lost and found search
    test_lost_and_found_search() 