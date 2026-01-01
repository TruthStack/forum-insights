import json
from typing import Dict, List, Any, Optional
import os

class StorageClient:
    def __init__(self, collection_name: str = "forum_incidents"):
        self.collection_name = collection_name
        self.data = []  # In-memory storage for demo
        
    def store(self, data: Dict[str, Any]) -> str:
        """
        Store incident data
        """
        import uuid
        import time
        
        incident_id = str(uuid.uuid4())[:8]
        data["id"] = incident_id
        data["timestamp"] = time.time()
        
        self.data.append(data)
        print(f"[INFO] Stored incident {incident_id} in {self.collection_name}")
        
        return incident_id
    
    def query(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Query incidents with filters
        """
        results = []
        
        for incident in self.data:
            match = True
            
            for key, value in filters.items():
                if key in incident:
                    if isinstance(value, list):
                        if incident[key] not in value:
                            match = False
                            break
                    elif incident[key] != value:
                        match = False
                        break
                else:
                    match = False
                    break
            
            if match:
                results.append(incident)
        
        print(f"[INFO] Query returned {len(results)} results for filters {filters}")
        return results
    
    def get_similar_threads(self, current_thread: Dict[str, Any], limit: int = 3) -> List[Dict[str, Any]]:
        """
        Find similar historical threads
        """
        # Simple keyword matching for demo
        keywords = []
        if "message" in current_thread:
            text = current_thread["message"].lower()
            keywords = [word for word in ["error", "bug", "issue", "fix", "update", "plugin"] 
                       if word in text]
        
        similar = []
        for incident in self.data:
            if "message" in incident:
                incident_text = incident["message"].lower()
                score = sum(1 for keyword in keywords if keyword in incident_text)
                if score > 0:
                    similar.append({"incident": incident, "score": score})
        
        similar.sort(key=lambda x: x["score"], reverse=True)
        return [item["incident"] for item in similar[:limit]]

def store_incident(incident: Dict[str, Any], client: Optional[StorageClient] = None) -> str:
    if client is None:
        client = StorageClient()
    
    return client.store(incident)

def query_incidents(filters: Dict[str, Any], client: Optional[StorageClient] = None) -> List[Dict[str, Any]]:
    if client is None:
        client = StorageClient()
    
    return client.query(filters)

if __name__ == "__main__":
    # Test storage
    client = StorageClient()
    
    test_incident = {"message": "Test error occurred", "service": "forum"}
    incident_id = client.store(test_incident)
    print(f"Stored incident ID: {incident_id}")
    
    results = client.query({"service": "forum"})
    print(f"Query results: {len(results)} incidents")
