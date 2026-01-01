import unittest
from unittest.mock import Mock, patch
from .main import explain_incident, GeminiClient

class TestGeminiExplainer(unittest.TestCase):
    
    @patch('modules.gemini_explainer.main.os.getenv')
    def test_gemini_client_mock(self, mock_getenv):
        mock_getenv.return_value = "demo-key"
        client = GeminiClient()
        result = client.explain("Test prompt")
        self.assertIn("what_happened", result)
        self.assertIn("root_cause", result)
        self.assertIn("remediation", result)
    
    def test_explain_incident(self):
        prompt_data = {"prompt": "Test prompt"}
        result = explain_incident(prompt_data)
        self.assertIsInstance(result, dict)
        self.assertIn("what_happened", result)
    
    @patch('modules.gemini_explainer.main.GeminiClient')
    def test_explain_with_custom_client(self, mock_client):
        mock_instance = Mock()
        mock_instance.explain.return_value = {"test": "value"}
        mock_client.return_value = mock_instance
        
        result = explain_incident({"prompt": "test"}, mock_instance)
        self.assertEqual(result, {"test": "value"})

if __name__ == '__main__':
    unittest.main()
