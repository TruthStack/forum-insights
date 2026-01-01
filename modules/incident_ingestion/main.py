import json
import base64
from typing import Dict, List, Any
import requests
import os

def ingest_from_webhook(payload: Dict) -> List[Dict]:
    """
    Simulate ingestion from webhook - for demo purposes
    """
    print(f"[INFO] Ingesting webhook payload with {len(payload.get('events', []))} events")
    
    events = []
    for event in payload.get("events", []):
        try:
            # Decode base64 if needed
            if isinstance(event, str):
                decoded = base64.b64decode(event).decode('utf-8')
                data = json.loads(decoded)
            else:
                data = event
            events.append(data)
        except:
            events.append({"message": str(event), "source": "webhook"})
    
    return events

def poll_forums(thread_id: str, api_key: str = None) -> List[Dict]:
    """
    Fetch posts from Foru.ms API
    """
    if api_key is None:
        api_key = os.getenv("FORU_API_KEY", "demo-key")
    
    # Mock response for demo
    print(f"[INFO] Polling Foru.ms thread {thread_id}")
    
    mock_posts = [
        {
            "id": "post_1",
            "user": "tech_support",
            "message": "Having issues with plugin after v2.2 update. Getting timeout errors.",
            "timestamp": "2024-12-31T10:00:00Z",
            "likes": 15
        },
        {
            "id": "post_2",
            "user": "community_helper",
            "message": "Try clearing cache and restarting. Worked for me yesterday.",
            "timestamp": "2024-12-31T10:05:00Z",
            "likes": 8
        },
        {
            "id": "post_3",
            "user": "developer_alpha",
            "message": "We're aware of the issue. Patch coming tomorrow. Temporary fix: downgrade to v2.1.",
            "timestamp": "2024-12-31T10:10:00Z",
            "likes": 42
        },
        {
            "id": "post_4", 
            "user": "frustrated_user",
            "message": "This keeps happening! Need better QA before releases.",
            "timestamp": "2024-12-31T10:15:00Z",
            "likes": 25
        },
        {
            "id": "post_5",
            "user": "solution_provider",
            "message": "Here's a workaround script: https://gist.github.com/... Works for 90% of cases.",
            "timestamp": "2024-12-31T10:20:00Z",
            "likes": 31
        }
    ]
    
    return mock_posts

if __name__ == "__main__":
    # Test the module
    test_payload = {"events": ["eyJtZXNzYWdlIjogIlRlc3QgbWVzc2FnZSJ9"]}
    result = ingest_from_webhook(test_payload)
    print(f"Test result: {result}")
