import json
import re
from typing import Dict, Any

def mask_pii(text: str) -> str:
    """
    Mask personally identifiable information in text
    """
    # Mask email addresses
    text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[EMAIL_MASKED]', text)
    
    # Mask IP addresses
    text = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[IP_MASKED]', text)
    
    # Mask phone numbers
    text = re.sub(r'\b(?:\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b', '[PHONE_MASKED]', text)
    
    # Mask URLs with credentials
    text = re.sub(r'https?://[^:]+:[^@]+@[^\s]+', '[URL_WITH_CREDS_MASKED]', text)
    
    return text

def parse_log(log_entry: Any) -> Dict[str, Any]:
    """
    Parse a log entry into structured format
    """
    if isinstance(log_entry, str):
        try:
            data = json.loads(log_entry)
        except json.JSONDecodeError:
            data = {"message": log_entry}
    elif isinstance(log_entry, dict):
        data = log_entry
    else:
        data = {"raw": str(log_entry)}
    
    # Ensure required fields
    if "message" not in data:
        data["message"] = str(data.get("raw", "No message"))
    
    # Mask PII in message
    if "message" in data:
        data["message_original"] = data["message"]
        data["message"] = mask_pii(data["message"])
    
    # Add metadata
    data["parsed"] = True
    data["has_pii"] = "MASKED" in data.get("message", "")
    
    return data

if __name__ == "__main__":
    # Test the parser
    test_log = '{"user": "john@example.com", "message": "Contact me at 555-123-4567 or john@example.com"}'
    parsed = parse_log(test_log)
    print(f"Parsed: {parsed}")
