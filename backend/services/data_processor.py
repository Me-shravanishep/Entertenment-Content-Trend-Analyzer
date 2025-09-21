# backend/services/data_processor.py
"""Data processing service for content analysis"""

from typing import List, Dict, Any
from datetime import datetime
from collections import Counter
from backend.utils.helpers import analyze_sentiment, clean_text, extract_hashtags

class DataProcessor:
    """Process and analyze collected content data"""
    
    def __init__(self):
        pass
    
    def process_content_batch(self, content_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a batch of content items"""
        processed_items = []
        
        for item in content_items:
            processed_item = self.process_single_item(item)
            processed_items.append(processed_item)
        
        return processed_items
    
    def process_single_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single content item"""
        # Add processing timestamp
        item['processed_at'] = datetime.now().isoformat()
        
        # Basic engagement calculation
        if 'view_count' in item and 'like_count' in item:
            views = item.get('view_count', 0) or 0
            likes = item.get('like_count', 0) or 0
            comments = item.get('comment_count', 0) or 0
            
            if views > 0:
                engagement_rate = ((likes + comments) / views) * 100
                item['engagement_rate'] = round(engagement_rate, 2)
            else:
                item['engagement_rate'] = 0.0
        
        # Clean and process text content
        title = item.get('title', '')
        description = item.get('description', '')
        
        if title:
            item['title_clean'] = clean_text(title)
            
            # Extract hashtags from title if not already present
            if not item.get('hashtags'):
                item['hashtags'] = extract_hashtags(title)
        
        if description:
            item['description_clean'] = clean_text(description)
        
        # Basic sentiment analysis
        text_for_analysis = f"{title} {description}".strip()
        if text_for_analysis:
            try:
                sentiment = analyze_sentiment(text_for_analysis)
                item['sentiment'] = sentiment
            except Exception as e:
                item['sentiment'] = {
                    'polarity': 0.0,
                    'subjectivity': 0.0,
                    'label': 'neutral',
                    'confidence': 0.0
                }
        
        # Calculate trending score (basic algorithm)
        item['trending_score'] = self._calculate_trending_score(item)
        
        return item
    
    def _calculate_trending_score(self, item: Dict[str, Any]) -> float:
        """Calculate a basic trending score for content"""
        score = 0.0
        
        # Engagement factor (40% of score)
        engagement_rate = item.get('engagement_rate', 0)
        if engagement_rate > 0:
            # Normalize engagement rate (assume 10% is very high)
            normalized_engagement = min(engagement_rate / 10.0, 1.0)
            score += normalized_engagement * 0.4
        
        # Recency factor (30% of score)
        try:
            if 'published_date' in item:
                published = datetime.fromisoformat(item['published_date'].replace('Z', '+00:00'))
                hours_old = (datetime.now() - published.replace(tzinfo=None)).total_seconds() / 3600
                
                # More recent content gets higher score
                if hours_old < 24:
                    recency_score = 1.0 - (hours_old / 24.0)
                    score += recency_score * 0.3
        except:
            # Default recency score if date parsing fails
            score += 0.15
        
        # Hashtag factor (20% of score)
        hashtags = item.get('hashtags', [])
        if hashtags:
            # More hashtags indicate more engagement potential
            hashtag_score = min(len(hashtags) / 5.0, 1.0)  # Normalize to max 5 hashtags
            score += hashtag_score * 0.2
        
        # Sentiment factor (10% of score)
        sentiment = item.get('sentiment', {})
        if sentiment:
            # Positive sentiment gets slight boost
            polarity = sentiment.get('polarity', 0)
            if polarity > 0:
                sentiment_score = min(polarity, 1.0)
                score += sentiment_score * 0.1
        
        return round(min(score, 1.0), 3)  # Cap at 1.0 and round to 3 decimals
    
    def analyze_trends(self, content_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze trends in content items"""
        if not content_items:
            return {
                'trending_hashtags': [],
                'platform_distribution': {},
                'sentiment_analysis': {},
                'engagement_stats': {}
            }
        
        # Count hashtags
        hashtag_counts = {}
        platform_counts = {}
        sentiment_counts = {}
        engagement_rates = []
        
        for item in content_items:
            # Platform distribution
            platform = item.get('platform', 'unknown')
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
            
            # Hashtag analysis
            hashtags = item.get('hashtags', [])
            for hashtag in hashtags:
                hashtag_counts[hashtag] = hashtag_counts.get(hashtag, 0) + 1
            
            # Sentiment analysis
            sentiment = item.get('sentiment', {})
            if sentiment:
                label = sentiment.get('label', 'neutral')
                sentiment_counts[label] = sentiment_counts.get(label, 0) + 1
            
            # Engagement rates
            engagement_rate = item.get('engagement_rate')
            if engagement_rate is not None:
                engagement_rates.append(engagement_rate)
        
        # Get top hashtags
        trending_hashtags = sorted(
            hashtag_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:15]
        
        # Calculate engagement statistics
        engagement_stats = {}
        if engagement_rates:
            engagement_stats = {
                'average': round(sum(engagement_rates) / len(engagement_rates), 2),
                'max': round(max(engagement_rates), 2),
                'min': round(min(engagement_rates), 2),
                'count': len(engagement_rates)
            }
        
        return {
            'trending_hashtags': [
                {
                    'hashtag': tag, 
                    'count': count,
                    'trend_score': self._calculate_hashtag_trend_score(tag, count, len(content_items))
                }
                for tag, count in trending_hashtags
            ],
            'platform_distribution': platform_counts,
            'sentiment_analysis': {
                'distribution': sentiment_counts,
                'total_analyzed': sum(sentiment_counts.values())
            },
            'engagement_stats': engagement_stats,
            'total_analyzed': len(content_items),
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _calculate_hashtag_trend_score(self, hashtag: str, count: int, total_items: int) -> float:
        """Calculate trending score for a hashtag"""
        if total_items == 0:
            return 0.0
        
        # Base frequency score
        frequency_score = count / total_items
        
        # Boost for certain trending keywords
        trending_keywords = ['viral', 'trending', 'hot', 'breaking', 'new', 'latest']
        keyword_boost = 1.0
        
        if any(keyword in hashtag.lower() for keyword in trending_keywords):
            keyword_boost = 1.5
        
        # Calculate final score
        trend_score = frequency_score * keyword_boost
        
        return round(min(trend_score, 1.0), 3)
    
    def get_top_trending_content(self, content_items: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
        """Get top trending content based on trending scores"""
        # Sort by trending score
        sorted_content = sorted(
            content_items,
            key=lambda x: x.get('trending_score', 0),
            reverse=True
        )
        
        return sorted_content[:limit]
    
    def filter_by_platform(self, content_items: List[Dict[str, Any]], platform: str) -> List[Dict[str, Any]]:
        """Filter content by platform"""
        return [item for item in content_items if item.get('platform') == platform]
    
    def filter_by_sentiment(self, content_items: List[Dict[str, Any]], sentiment_label: str) -> List[Dict[str, Any]]:
        """Filter content by sentiment"""
        return [
            item for item in content_items 
            if item.get('sentiment', {}).get('label') == sentiment_label
        ]
    
    def get_content_summary(self, content_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get comprehensive content summary"""
        if not content_items:
            return {
                'total_content': 0,
                'summary': 'No content available for analysis'
            }
        
        # Process all items if not already processed
        processed_items = []
        for item in content_items:
            if 'processed_at' not in item:
                processed_items.append(self.process_single_item(item.copy()))
            else:
                processed_items.append(item)
        
        # Generate trend analysis
        trend_analysis = self.analyze_trends(processed_items)
        
        # Get top trending content
        top_trending = self.get_top_trending_content(processed_items, limit=5)
        
        return {
            'total_content': len(processed_items),
            'trend_analysis': trend_analysis,
            'top_trending_content': top_trending,
            'processing_summary': {
                'items_processed': len(processed_items),
                'processing_timestamp': datetime.now().isoformat()
            }
        }