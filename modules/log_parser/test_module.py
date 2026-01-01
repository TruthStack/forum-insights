import unittest
from .main import parse_log, mask_pii

class TestLogParser(unittest.TestCase):
    
    def test_mask_pii(self):
        text = "Email me at test@example.com or call 555-123-4567"
        masked = mask_pii(text)
        self.assertIn("[EMAIL_MASKED]", masked)
        self.assertIn("[PHONE_MASKED]", masked)
        self.assertNotIn("test@example.com", masked)
    
    def test_parse_log_string(self):
        log = '{"message": "Hello world", "level": "info"}'
        result = parse_log(log)
        self.assertEqual(result["message"], "Hello world")
        self.assertEqual(result["level"], "info")
        self.assertTrue(result["parsed"])
    
    def test_parse_log_dict(self):
        log = {"message": "Test message", "user": "alice"}
        result = parse_log(log)
        self.assertEqual(result["message"], "Test message")
        self.assertEqual(result["user"], "alice")
    
    def test_pii_detection(self):
        log = {"message": "Email: user@domain.com"}
        result = parse_log(log)
        self.assertTrue(result["has_pii"])

if __name__ == '__main__':
    unittest.main()
