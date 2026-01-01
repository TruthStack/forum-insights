import unittest
from unittest.mock import patch, MagicMock
from .main import ingest_from_webhook, poll_forums

class TestIncidentIngestion(unittest.TestCase):
    
    def test_ingest_from_webhook(self):
        payload = {
            "events": ["eyJtZXNzYWdlIjogIkhlbGxvIFdvcmxkIn0="]  # base64 of {"message": "Hello World"}
        }
        result = ingest_from_webhook(payload)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["message"], "Hello World")
    
    def test_ingest_empty_payload(self):
        result = ingest_from_webhook({})
        self.assertEqual(result, [])
    
    @patch('modules.incident_ingestion.main.os.getenv')
    def test_poll_forums(self, mock_getenv):
        mock_getenv.return_value = "test-key"
        result = poll_forums("thread_123")
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0]["user"], "tech_support")

if __name__ == '__main__':
    unittest.main()
