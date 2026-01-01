import unittest
from .main import aggregate_trends, analyze_sentiment, detect_toxicity

class TestTrendAggregator(unittest.TestCase):
    
    def test_analyze_sentiment(self):
        self.assertEqual(analyze_sentiment("Great work!"), "positive")
        self.assertEqual(analyze_sentiment("This is broken"), "negative")
        self.assertEqual(analyze_sentiment("Hello world"), "neutral")
    
    def test_detect_toxicity(self):
        self.assertGreater(detect_toxicity("This is stupid"), 0.0)
        self.assertEqual(detect_toxicity("Normal message"), 0.0)
    
    def test_aggregate_trends(self):
        data = {
            "incidents": [
                {"message": "Good job team"},
                {"message": "Having some issues"},
                {"message": "Terrible experience"}
            ]
        }
        
        result = aggregate_trends(data)
        self.assertEqual(result["total_incidents"], 3)
        self.assertIn("aggregates", result)
        self.assertIn("trends", result)
        self.assertIn("sentiment_distribution", result["aggregates"])
    
    def test_empty_aggregate(self):
        result = aggregate_trends({})
        self.assertEqual(result["total_incidents"], 0)
        self.assertEqual(result["summary"], "No data to analyze")

if __name__ == '__main__':
    unittest.main()
