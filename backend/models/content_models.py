# backend/models/content_models.py
"""Data models for content storage and processing"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

@dataclass
class ContentItem:
    """Base content item model"""
    id: str
    title: str
    description: str
    platform: str
    author: str
    published_date: datetime
    url: str
    thumbnail_url: Optional[str] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    comment_count: Optional[int] = None
    share_count: Optional[int] = None
    hashtags: List[str] = None
    
    def __post_init__(self):
        if self.hashtags is None:
            self.hashtags = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['published_date'] = self.published_date.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContentItem':
        """Create from dictionary"""
        data['published_date'] = datetime.fromisoformat(data['published_date'])
        return cls(**data)

@dataclass
class TrendingTopic:
    """Trending topic model"""
    keyword: str
    platform: str
    score: float
    volume: int
    growth_rate: float
    related_content: List[str]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'keyword': self.keyword,
            'platform': self.platform,
            'score': self.score,
            'volume': self.volume,
            'growth_rate': self.growth_rate,
            'related_content': self.related_content,
            'timestamp': self.timestamp.isoformat()
        }

@dataclass
class AnalyticsResult:
    """Analytics result model"""
    content_id: str
    sentiment_score: float
    sentiment_label: str
    emotion_scores: Dict[str, float]
    engagement_prediction: float
    trending_probability: float
    analysis_timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'content_id': self.content_id,
            'sentiment_score': self.sentiment_score,
            'sentiment_label': self.sentiment_label,
            'emotion_scores': self.emotion_scores,
            'engagement_prediction': self.engagement_prediction,
            'trending_probability': self.trending_probability,
            'analysis_timestamp': self.analysis_timestamp.isoformat()
        }