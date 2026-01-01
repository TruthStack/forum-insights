import unittest
from .main import StorageClient, store_incident, query_incidents

class TestHistoricalStorage(unittest.TestCase):
    
    def setUp(self):
        self.client = StorageClient()
    
    def test_store_incident(self):
        data = {"message": "Test incident", "level": "error"}
        result = store_incident(data, self.client)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 8)  # UUID short
    
    def test_query_incidents(self):
        # Store test data
        self.client.store({"message": "Error 500", "service": "api"})
        self.client.store({"message": "Timeout", "service": "forum"})
        
        # Query
        results = query_incidents({"service": "forum"}, self.client)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["message"], "Timeout")
    
    def test_get_similar_threads(self):
        # Add some test data
        self.client.store({"message": "Plugin error after update", "type": "bug"})
        self.client.store({"message": "Login timeout issue", "type": "error"})
        self.client.store({"message": "General discussion", "type": "chat"})
        
        current = {"message": "Getting plugin compatibility errors with new version"}
        similar = self.client.get_similar_threads(current)
        self.assertEqual(len(similar), 1)
        self.assertIn("Plugin error", similar[0]["message"])

if __name__ == '__main__':
    unittest.main()
