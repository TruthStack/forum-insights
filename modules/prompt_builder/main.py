from typing import Dict, List, Any

def build_prompt(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build a prompt for LLM summarization
    """
    messages = data.get("parsed_fields", {}).get("message", "")
    
    prompt_template = f"""
    Analyze this forum thread discussion and provide a comprehensive summary:
    
    THREAD CONTENT:
    {messages}
    
    Please structure your response as JSON with these exact keys:
    1. "what_happened": Brief overview of the main issue/event (1-2 sentences)
    2. "root_cause": Key debate or underlying causes (2-3 bullet points)
    3. "remediation": Actionable next steps or solutions suggested (2-3 bullet points)
    4. "sentiment": Overall sentiment (positive/negative/neutral/mixed)
    5. "urgency": How urgent is this issue? (low/medium/high)
    
    Return ONLY valid JSON, no other text.
    """
    
    return {
        "prompt": prompt_template,
        "metadata": {
            "source": "forum_thread",
            "message_count": len(messages.split('\n')) if messages else 0,
            "prompt_type": "summary_analysis"
        }
    }

def build_summary_prompt(messages: List[str], additional_context: str = "") -> Dict[str, Any]:
    """
    Alternative prompt builder for simple summaries
    """
    combined_messages = "\n".join([f"• {msg}" for msg in messages])
    
    prompt = f"""
    Summarize this forum discussion:
    
    {combined_messages}
    
    {additional_context}
    
    Provide a concise TL;DR (2-3 sentences).
    """
    
    return {
        "prompt": prompt,
        "type": "tldr_summary",
        "length": "concise"
    }

if __name__ == "__main__":
    test_data = {"parsed_fields": {"message": "User reported bug. Admin responded with fix."}}
    result = build_prompt(test_data)
    print(f"Built prompt: {result['prompt'][:100]}...")
