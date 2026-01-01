from typing import Dict, List, Any
from collections import Counter
import re

def analyze_sentiment(text: str) -> str:
    """
    Simple sentiment analysis
    """
    text_lower = text.lower()
    
    positive_words = ["good", "great", "excellent", "thanks", "helpful", "fixed", "solved", "works", "awesome"]
    negative_words = ["bad", "error", "broken", "issue", "problem", "fail", "crash", "terrible", "frustrating"]
    
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    else:
        return "neutral"

def detect_toxicity(text: str) -> float:
    """
    Simple toxicity detection (0.0 to 1.0)
    """
    toxic_patterns = [
        r"\b(idiot|stupid|dumb|moron)\b",
        r"\b(hate|suck|worthless|garbage)\b",
        r"\b(fuck|shit|damn|hell)\b",
        r"all caps shouting",
        r"excessive punctuation !!!"
    ]
    
    score = 0.0
    for pattern in toxic_patterns:
        if re.search(pattern, text.lower()):
            score += 0.2
    
    return min(score, 1.0)

def aggregate_trends(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Aggregate trends from incidents
    """
    incidents = data.get("incidents", [])
    
    if not incidents:
        return {
            "total_incidents": 0,
            "trends": {},
            "aggregates": {},
            "summary": "No data to analyze"
        }
    
    # Analyze each incident
    sentiments = []
    toxicities = []
    error_types = []
    
    for incident in incidents:
        message = incident.get("message", "")
        
        # Sentiment
        sentiment = analyze_sentiment(message)
        sentiments.append(sentiment)
        
        # Toxicity
        toxicity = detect_toxicity(message)
        toxicities.append(toxicity)
        
        # Error type detection
        if any(word in message.lower() for word in ["error", "fail", "broken"]):
            error_types.append("technical")
        elif any(word in message.lower() for word in ["question", "help", "how to"]):
            error_types.append("support")
        elif any(word in message.lower() for word in ["suggestion", "feature", "improve"]):
            error_types.append("feedback")
        else:
            error_types.append("discussion")
    
    # Calculate aggregates
    sentiment_counts = Counter(sentiments)
    error_type_counts = Counter(error_types)
    
    avg_toxicity = sum(toxicities) / len(toxicities) if toxicities else 0
    
    # Determine dominant trends
    dominant_sentiment = sentiment_counts.most_common(1)[0][0] if sentiment_counts else "neutral"
    common_error_type = error_type_counts.most_common(1)[0][0] if error_type_counts else "discussion"
    
    # Generate trend insights
    insights = []
    if avg_toxicity > 0.3:
        insights.append(f"Elevated toxicity detected ({avg_toxicity:.1%})")
    if sentiment_counts.get("negative", 0) > len(incidents) * 0.5:
        insights.append("Majority negative sentiment in thread")
    if error_type_counts.get("technical", 0) > 2:
        insights.append("Multiple technical issues reported")
    
    return {
        "total_incidents": len(incidents),
        "aggregates": {
            "sentiment_distribution": dict(sentiment_counts),
            "error_type_distribution": dict(error_type_counts),
            "avg_toxicity": avg_toxicity,
            "toxicity_high": avg_toxicity > 0.3,
            "dominant_sentiment": dominant_sentiment,
            "common_error_type": common_error_type
        },
        "trends": {
            "rising_issues": error_type_counts.get("technical", 0) > 0,
            "community_health": "concerning" if avg_toxicity > 0.5 else "healthy",
            "support_needed": error_type_counts.get("support", 0) > 1
        },
        "insights": insights,
        "summary": f"Thread analysis: {len(insights)} key insights found"
    }

if __name__ == "__main__":
    # Test aggregation
    test_data = {
        "incidents": [
            {"message": "Great plugin, works perfectly!"},
            {"message": "Having issues with installation, help needed."},
            {"message": "This is garbage, doesn't work at all!"}
        ]
    }
    
    trends = aggregate_trends(test_data)
    print(f"Trends: {trends}")
