# backend/routes/data_routes.py
"""Data collection and retrieval routes"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import logging

# Create blueprint
data_bp = Blueprint('data', __name__)
logger = logging.getLogger(__name__)

@data_bp.route('/health')
def data_health():
    """Data service health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'data_collection',
        'timestamp': datetime.now().isoformat()
    })

@data_bp.route('/youtube/trending')
def get_youtube_trending():
    """Get YouTube trending content"""
    try:
        # Import here to avoid circular imports
        from backend.services.youtube_service import YouTubeService
        
        # Get query parameters
        max_results = request.args.get('max_results', 25, type=int)
        category_id = request.args.get('category', '24')  # Entertainment
        
        # Initialize service and get data
        youtube_service = YouTubeService()
        trending_videos = youtube_service.search_trending_videos(
            category_id=category_id, 
            max_results=max_results
        )
        
        return jsonify({
            'status': 'success',
            'platform': 'youtube',
            'count': len(trending_videos),
            'data': trending_videos,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error fetching YouTube trending: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to fetch YouTube trending: {str(e)}',
            'platform': 'youtube'
        }), 500

@data_bp.route('/instagram/trending')
def get_instagram_trending():
    """Get Instagram trending content"""
    try:
        # Import here to avoid circular imports
        from backend.services.instagram_service import InstagramService
        
        # Get query parameters
        max_results = request.args.get('max_results', 25, type=int)
        
        # Initialize service and get data
        instagram_service = InstagramService()
        trending_posts = instagram_service.get_trending_posts(max_results=max_results)
        
        return jsonify({
            'status': 'success',
            'platform': 'instagram',
            'count': len(trending_posts),
            'data': trending_posts,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error fetching Instagram trending: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to fetch Instagram trending: {str(e)}',
            'platform': 'instagram'
        }), 500

@data_bp.route('/collect')
def collect_data():
    """Trigger data collection from all platforms"""
    try:
        results = {
            'youtube': {'status': 'pending', 'data': []},
            'instagram': {'status': 'pending', 'data': []}
        }
        
        # Collect YouTube data
        try:
            from backend.services.youtube_service import YouTubeService
            youtube_service = YouTubeService()
            youtube_data = youtube_service.search_trending_videos(max_results=20)
            results['youtube'] = {
                'status': 'success',
                'count': len(youtube_data),
                'data': youtube_data
            }
        except Exception as e:
            results['youtube'] = {
                'status': 'error',
                'message': str(e)
            }
        
        # Collect Instagram data
        try:
            from backend.services.instagram_service import InstagramService
            instagram_service = InstagramService()
            instagram_data = instagram_service.get_trending_posts(max_results=20)
            results['instagram'] = {
                'status': 'success',
                'count': len(instagram_data),
                'data': instagram_data
            }
        except Exception as e:
            results['instagram'] = {
                'status': 'error',
                'message': str(e)
            }
        
        return jsonify({
            'status': 'completed',
            'message': 'Data collection completed',
            'results': results,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in data collection: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Data collection failed: {str(e)}'
        }), 500

@data_bp.route('/recent')
def get_recent_content():
    """Get recently collected content"""
    try:
        # Import here to avoid circular imports
        from backend.utils.database import DatabaseManager
        
        # Get query parameters
        platform = request.args.get('platform')
        limit = request.args.get('limit', 50, type=int)
        
        # Get data from database
        db = DatabaseManager()
        recent_content = db.get_recent_content(platform=platform, limit=limit)
        
        return jsonify({
            'status': 'success',
            'count': len(recent_content),
            'data': recent_content,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error fetching recent content: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to fetch recent content: {str(e)}'
        }), 500

@data_bp.route('/stats')
def get_data_stats():
    """Get data collection statistics"""
    try:
        from backend.utils.database import DatabaseManager
        
        db = DatabaseManager()
        
        # Get stats for different platforms
        youtube_count = len(db.get_recent_content(platform='youtube', limit=1000))
        instagram_count = len(db.get_recent_content(platform='instagram', limit=1000))
        total_count = len(db.get_recent_content(limit=1000))
        
        return jsonify({
            'status': 'success',
            'stats': {
                'total_content': total_count,
                'youtube_content': youtube_count,
                'instagram_content': instagram_count,
                'last_updated': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Error fetching data stats: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to fetch data stats: {str(e)}'
        }), 500