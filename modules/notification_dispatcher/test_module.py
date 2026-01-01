import unittest
from unittest.mock import patch
from .main import dispatch, send_slack_alert, send_email_alert

class TestNotificationDispatcher(unittest.TestCase):
    
    @patch('modules.notification_dispatcher.main.os.getenv')
    def test_send_slack_alert(self, mock_getenv):
        mock_getenv.return_value = "test-webhook"
        message = {
            "what_happened": "Test incident",
            "urgency": "high",
            "sentiment": "negative"
        }
        
        result = send_slack_alert(message)
        self.assertEqual(result["status"], "sent")
        self.assertEqual(result["platform"], "slack")
        self.assertEqual(result["urgency"], "high")
    
    @patch('modules.notification_dispatcher.main.os.getenv')
    def test_send_email_alert(self, mock_getenv):
        mock_getenv.return_value = "test@example.com"
        message = {
            "what_happened": "Test email alert",
            "urgency": "medium"
        }
        
        result = send_email_alert(message)
        self.assertEqual(result["status"], "sent")
        self.assertEqual(result["platform"], "email")
        self.assertIn("@", result["recipient"])
    
    def test_dispatch_slack(self):
        message = {"what_happened": "Test"}
        result = dispatch(message, "slack")
        self.assertEqual(result["platform"], "slack")
    
    def test_dispatch_email(self):
        message = {"what_happened": "Test"}
        result = dispatch(message, "email", recipient="test@example.com")
        self.assertEqual(result["platform"], "email")
    
    def test_dispatch_invalid(self):
        result = dispatch({}, "invalid")
        self.assertEqual(result["status"], "error")

if __name__ == '__main__':
    unittest.main()
