import json
import os
from typing import Dict, Optional, Any
from google import genai

class GeminiClient:
    def __init__(self, api_key: str = None):
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY", "demo-key")
        self.client = genai.Client(api_key=api_key)
    
    def explain(self, prompt: str) -> Dict[str, Any]:
        """
        Get explanation from Gemini AI
        """
        try:
            # For demo - return mock response if no real API key
            if os.getenv("GEMINI_API_KEY", "demo-key") == "demo-key":
                return self._mock_explanation(prompt)
            
            # Real Gemini API call
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            
            # Parse response
            response_text = response.text
            
            # Try to extract JSON from response
            try:
                # Look for JSON in the response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start != -1 and json_end != 0:
                    json_str = response_text[json_start:json_end]
                    return json.loads(json_str)
            except:
                # Fallback to structured response
                return {
                    "what_happened": response_text[:200] + "...",
                    "root_cause": "AI analysis",
                    "remediation": "Review thread details",
                    "sentiment": "neutral",
                    "urgency": "medium"
                }
                
        except Exception as e:
            print(f"[ERROR] Gemini call failed: {e}")
            return self._mock_explanation(prompt)
    
    def _mock_explanation(self, prompt: str) -> Dict[str, Any]:
        """Mock response for demo purposes"""
        return {
            "what_happened": "Users reported plugin compatibility issues after v2.2 update, causing timeout errors and crashes for multiple users.",
            "root_cause": [
                "Breaking changes in API endpoints in v2.2",
                "Missing backward compatibility layer",
                "Insufficient testing with popular plugins"
            ],
            "remediation": [
                "Immediate: Downgrade to v2.1 as temporary fix",
                "Short-term: Release hotfix patch within 24 hours", 
                "Long-term: Implement compatibility testing suite"
            ],
            "sentiment": "negative",
            "urgency": "high",
            "confidence": 0.92
        }

def explain_incident(prompt_data: Dict, client: Optional[GeminiClient] = None) -> Dict[str, Any]:
    """
    Main function to get incident explanation
    """
    if client is None:
        client = GeminiClient()
    
    prompt_text = prompt_data.get("prompt", "")
    explanation = client.explain(prompt_text)
    
    return explanation

if __name__ == "__main__":
    # Test the explainer
    client = GeminiClient()
    test_prompt = {"prompt": "Summarize: Users reporting login issues"}
    result = explain_incident(test_prompt, client)
    print(f"Explanation: {json.dumps(result, indent=2)}")
