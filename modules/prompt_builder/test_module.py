import unittest
from .main import build_prompt, build_summary_prompt

class TestPromptBuilder(unittest.TestCase):
    
    def test_build_prompt(self):
        data = {
            "parsed_fields": {
                "message": "Test message content here"
            }
        }
        result = build_prompt(data)
        self.assertIn("prompt", result)
        self.assertIn("Test message content here", result["prompt"])
        self.assertIn("what_happened", result["prompt"])
    
    def test_build_prompt_empty(self):
        data = {"parsed_fields": {"message": ""}}
        result = build_prompt(data)
        self.assertIn("THREAD CONTENT:", result["prompt"])
    
    def test_build_summary_prompt(self):
        messages = ["First post", "Second post", "Third post"]
        result = build_summary_prompt(messages, "Focus on technical issues")
        self.assertIn("First post", result["prompt"])
        self.assertIn("Focus on technical issues", result["prompt"])
        self.assertEqual(result["type"], "tldr_summary")

if __name__ == '__main__':
    unittest.main()
