# backend/routes/analytics_routes.py
"""Analytics and trend analysis routes"""

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import logging
from collections import Counter

# Create blueprint
analytics_bp = Blueprint('analytics', __name__)
logger = logging.getLogger(__name__)

@analytics_bp.route('/health')
def analytics_health():
    """Analytics service health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'analytics',
        'timestamp': datetime.now().isoformat()
    })

@analytics_bp.route('/summary')
def get_analytics_summary():
    """Get comprehensive analytics summary"""
    try:
        from backend.utils.database import DatabaseManager
        from backend.utils.helpers import analyze_sentiment
        
        db = DatabaseManager()
        
        # Get recent content
        recent_content = db.get_recent_content(limit=100)
        
        if not recent_content:
            return jsonify({
                'status': 'success',
                'message': 'No data available for analysis',
                'summary': {
                    'total_content': 0,
                    'platforms': {},
                    'sentiment_distribution': {},
                    'top_hashtags': [],
                    'engagement_stats': {}
                }
            })
        
        # Platform distribution
        platform_counts = Counter(item['platform'] for item in recent_content)
        
        # Hashtag analysis
        all_hashtags = []
        for item in recent_content:
            if item.get('hashtags'):
                if isinstance(item['hashtags'], str):
                    import json
                    try:
                        hashtags = json.loads(item['hashtags'])
                        all_hashtags.extend(hashtags)
                    except:
                        pass
                elif isinstance(item['hashtags'], list):
                    all_hashtags.extend(item['hashtags'])
        
        top_hashtags = Counter(all_hashtags).most_common(10)
        
        # Basic sentiment analysis on titles
        sentiments = []
        for item in recent_content:
            if item.get('title'):
                sentiment = analyze_sentiment(item['title'])
                sentiments.append(sentiment['label'])
        
        sentiment_distribution = dict(Counter(sentiments))
        
        # Engagement statistics
        engagement_data = []
        for item in recent_content:
            views = item.get('view_count', 0) or 0
            likes = item.get('like_count', 0) or 0
            comments = item.get('comment_count', 0) or 0
            
            if views > 0:
                engagement_rate = ((likes + comments) / views) * 100
                engagement_data.append(engagement_rate)
        
        avg_engagement = sum(engagement_data) / len(engagement_data) if engagement_data else 0
        
        summary = {
            'total_content': len(recent_content),
            'platforms': dict(platform_counts),
            'sentiment_distribution': sentiment_distribution,
            'top_hashtags': [{'hashtag': tag, 'count': count} for tag, count in top_hashtags],
            'engagement_stats': {
                'average_engagement_rate': round(avg_engagement, 2),
                'total_analyzed': len(engagement_data)
            },
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return jsonify({
            'status': 'success',
            'summary': summary
        })
        
    except Exception as e:
        logger.error(f"Error generating analytics summary: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to generate analytics summary: {str(e)}'
        }), 500

@analytics_bp.route('/trending')
def get_trending_analysis():
    """Get trending topics analysis"""
    try:
        from backend.utils.database import DatabaseManager
        from backend.utils.helpers import calculate_trending_score
        
        db = DatabaseManager()
        recent_content = db.get_recent_content(limit=200)
        
        # Simple trending analysis based on hashtags and engagement
        hashtag_scores = {}
        
        for item in recent_content:
            # Calculate recency (hours since published)
            try:
                if item.get('published_date'):
                    published = datetime.fromisoformat(item['published_date'].replace('Z', '+00:00'))
                    recency_hours = (datetime.now() - published.replace(tzinfo=None)).total_seconds() / 3600
                else:
                    recency_hours = 24  # Default if no date
            except:
                recency_hours = 24
            
            # Calculate engagement rate
            views = item.get('view_count', 0) or 1
            likes = item.get('like_count', 0) or 0
            comments = item.get('comment_count', 0) or 0
            engagement_rate = ((likes + comments) / views) * 100
            
            # Process hashtags
            hashtags = []
            if item.get('hashtags'):
                if isinstance(item['hashtags'], str):
                    import json
                    try:
                        hashtags = json.loads(item['hashtags'])
                    except:
                        pass
                elif isinstance(item['hashtags'], list):
                    hashtags = item['hashtags']
            
            # Calculate scores for each hashtag
            for hashtag in hashtags:
                if hashtag not in hashtag_scores:
                    hashtag_scores[hashtag] = {
                        'total_engagement': 0,
                        'content_count': 0,
                        'platforms': set(),
                        'recent_hours': []
                    }
                
                hashtag_scores[hashtag]['total_engagement'] += engagement_rate
                hashtag_scores[hashtag]['content_count'] += 1
                hashtag_scores[hashtag]['platforms'].add(item['platform'])
                hashtag_scores[hashtag]['recent_hours'].append(recency_hours)
        
        # Calculate trending scores
        trending_topics = []
        for hashtag, data in hashtag_scores.items():
            if data['content_count'] >= 2:  # Minimum content count
                avg_engagement = data['total_engagement'] / data['content_count']
                avg_recency = sum(data['recent_hours']) / len(data['recent_hours'])
                growth_rate = min(1.0, data['content_count'] / 10)  # Simple growth metric
                
                trending_score = calculate_trending_score(
                    avg_engagement, growth_rate, avg_recency
                )
                
                trending_topics.append({
                    'hashtag': hashtag,
                    'score': round(trending_score, 3),
                    'volume': data['content_count'],
                    'engagement_rate': round(avg_engagement, 2),
                    'platforms': list(data['platforms']),
                    'avg_recency_hours': round(avg_recency, 1)
                })
        
        # Sort by trending score
        trending_topics.sort(key=lambda x: x['score'], reverse=True)
        
        return jsonify({
            'status': 'success',
            'trending_topics': trending_topics[:20],  # Top 20
            'analysis_timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in trending analysis: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to analyze trending topics: {str(e)}'
        }), 500

@analytics_bp.route('/sentiment')
def get_sentiment_analysis():
    """Get sentiment analysis of content"""
    try:
        from backend.utils.database import DatabaseManager
        from backend.utils.helpers import analyze_sentiment
        
        # Get query parameters
        platform = request.args.get('platform')
        limit = request.args.get('limit', 50, type=int)
        
        db = DatabaseManager()
        content = db.get_recent_content(platform=platform, limit=limit)
        
        sentiment_results = []
        for item in content:
            if item.get('title') or item.get('description'):
                text = f"{item.get('title', '')} {item.get('description', '')}"
                sentiment = analyze_sentiment(text)
                
                sentiment_results.append({
                    'content_id': item['id'],
                    'platform': item['platform'],
                    'title': item.get('title', '')[:100],  # Truncate for response
                    'sentiment': sentiment,
                    'author': item.get('author', 'Unknown')
                })
        
        # Aggregate statistics
        sentiment_counts = Counter(result['sentiment']['label'] for result in sentiment_results)
        avg_polarity = sum(result['sentiment']['polarity'] for result in sentiment_results) / len(sentiment_results) if sentiment_results else 0
        
        return jsonify({
            'status': 'success',
            'sentiment_analysis': {
                'results': sentiment_results,
                'statistics': {
                    'total_analyzed': len(sentiment_results),
                    'sentiment_distribution': dict(sentiment_counts),
                    'average_polarity': round(avg_polarity, 3),
                    'analysis_timestamp': datetime.now().isoformat()
                }
            }
        })
        
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to perform sentiment analysis: {str(e)}'
        }), 500

@analytics_bp.route('/engagement')
def get_engagement_analysis():
    """Get engagement analysis"""
    try:
        from backend.utils.database import DatabaseManager
        from backend.utils.helpers import calculate_engagement_rate
        
        platform = request.args.get('platform')
        limit = request.args.get('limit', 100, type=int)
        
        db = DatabaseManager()
        content = db.get_recent_content(platform=platform, limit=limit)
        
        engagement_data = []
        for item in content:
            views = item.get('view_count', 0) or 0
            likes = item.get('like_count', 0) or 0
            comments = item.get('comment_count', 0) or 0
            shares = item.get('share_count', 0) or 0
            
            if views > 0:
                engagement_rate = calculate_engagement_rate(likes, comments, shares, views)
                engagement_data.append({
                    'content_id': item['id'],
                    'title': item.get('title', '')[:50],
                    'platform': item['platform'],
                    'author': item.get('author', 'Unknown'),
                    'views': views,
                    'likes': likes,
                    'comments': comments,
                    'shares': shares,
                    'engagement_rate': round(engagement_rate, 2)
                })
        
        # Sort by engagement rate
        engagement_data.sort(key=lambda x: x['engagement_rate'], reverse=True)
        
        # Calculate statistics
        rates = [item['engagement_rate'] for item in engagement_data]
        avg_engagement = sum(rates) / len(rates) if rates else 0
        
        return jsonify({
            'status': 'success',
            'engagement_analysis': {
                'top_performing': engagement_data[:20],
                'statistics': {
                    'total_analyzed': len(engagement_data),
                    'average_engagement_rate': round(avg_engagement, 2),
                    'highest_engagement': max(rates) if rates else 0,
                    'lowest_engagement': min(rates) if rates else 0
                }
            }
        })
        
    except Exception as e:
        logger.error(f"Error in engagement analysis: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to analyze engagement: {str(e)}'
        }), 500