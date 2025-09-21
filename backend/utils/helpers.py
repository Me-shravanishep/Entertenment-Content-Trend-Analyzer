"""Helper functions for data processing"""

import re
import hashlib
from typing import List, Set, Dict, Any
from datetime import datetime, timedelta
from collections import Counter
from textblob import TextBlob

def extract_hashtags(text: str) -> List[str]:
    """Extract hashtags from text"""
    hashtag_pattern = r'#\w+'
    hashtags = re.findall(hashtag_pattern, text.lower())
    return [tag[1:] for tag in hashtags]  # Remove # symbol

def extract_mentions(text: str) -> List[str]:
    """Extract mentions from text"""
    mention_pattern = r'@\w+'
    mentions = re.findall(mention_pattern, text.lower())
    return [mention[1:] for mention in mentions]  # Remove @ symbol

def clean_text(text: str) -> str:
    """Clean text for analysis"""
    if not text:
        return ""
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove special characters but keep spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text.strip()

def calculate_engagement_rate(likes: int, comments: int, shares: int, views: int) -> float:
    """Calculate engagement rate"""
    if views == 0:
        return 0.0
    
    total_engagement = (likes or 0) + (comments or 0) + (shares or 0)
    return (total_engagement / views) * 100

def generate_content_id(title: str, author: str, platform: str) -> str:
    """Generate unique content ID"""
    content_string = f"{title}_{author}_{platform}"
    return hashlib.md5(content_string.encode()).hexdigest()

def analyze_sentiment(text: str) -> Dict[str, Any]:
    """Analyze sentiment of text using TextBlob"""
    try:
        blob = TextBlob(clean_text(text))
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Classify sentiment
        if polarity > 0.1:
            label = 'positive'
        elif polarity < -0.1:
            label = 'negative'
        else:
            label = 'neutral'
        
        return {
            'polarity': polarity,
            'subjectivity': subjectivity,
            'label': label,
            'confidence': abs(polarity)
        }
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return {
            'polarity': 0.0,
            'subjectivity': 0.0,
            'label': 'neutral',
            'confidence': 0.0
        }

def calculate_trending_score(engagement_rate: float, growth_rate: float, 
                           recency_hours: float) -> float:
    """Calculate trending score for content"""
    # Weight factors
    engagement_weight = 0.4
    growth_weight = 0.4
    recency_weight = 0.2
    
    # Normalize recency (more recent = higher score)
    recency_score = max(0, 1 - (recency_hours / 168))  # 7 days normalization
    
    # Calculate weighted score
    trending_score = (
        engagement_rate * engagement_weight +
        growth_rate * growth_weight +
        recency_score * recency_weight
    )
    
    return min(1.0, max(0.0, trending_score))  # Clamp between 0 and 1