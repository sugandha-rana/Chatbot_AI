import requests
import json

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

# Mock user queries for testing
USER_QUERIES = [
    # Incident Report Queries
    {
        "user_type": "user",
        "query": "I lost my phone at the event"
    },
    {
        "user_type": "user", 
        "query": "I need to report an injury"
    },
    {
        "user_type": "user",
        "query": "Someone is causing trouble in the crowd"
    },
    {
        "user_type": "user",
        "query": "I lost my wallet with my ID inside"
    },
    {
        "user_type": "user",
        "query": "There's a medical emergency in zone A"
    },
    # Lost and Found Queries
    {
        "user_type": "user",
        "query": "Has anyone found a black phone?"
    },
    {
        "user_type": "user",
        "query": "I'm looking for my lost wallet"
    },
    {
        "user_type": "user",
        "query": "Did anyone find a red jacket?"
    },
    {
        "user_type": "user",
        "query": "I lost my keys, has anyone seen them?"
    },
    {
        "user_type": "user",
        "query": "Looking for a blue backpack"
    }
]

def test_user_queries():
    """Test user queries one by one"""
    print("🧪 Testing User Queries\n")
    
    for i, query_data in enumerate(USER_QUERIES, 1):
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
                print(f"Response: {result}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Error details: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print("\n" + "="*60 + "\n")

def test_single_user_query(query_text):
    """Test a single custom user query"""
    query_data = {
        "user_type": "user",
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
            print(f"Response: {result}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Error details: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    print("🚀 CrowdGuard AI - User Query Tester")
    print("=" * 60)
    
    # Test all predefined queries
    test_user_queries()
    
    # You can also test custom queries
    # test_single_user_query("Your custom user query here") 