# backend/services/instagram_service.py
"""Instagram data collection service"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from config.settings import Config

class InstagramService:
    """Instagram Basic Display API service"""
    
    def __init__(self):
        self.access_token = Config.INSTAGRAM_ACCESS_TOKEN
    
    def get_trending_posts(self, max_results: int = 25) -> List[Dict[str, Any]]:
        """Get trending posts from Instagram"""
        # For now, return demo data
        return self._get_mock_instagram_data(max_results)
    
    def _get_mock_instagram_data(self, max_results: int = 25) -> List[Dict[str, Any]]:
        """Generate mock Instagram data for development"""
        mock_captions = [
            "Fashion trending now! #fashion #style #ootd #trending",
            "Food that's taking over social media #food #viral #cooking",
            "Travel destinations everyone's talking about #travel #wanderlust",
            "Fitness motivation for your day #fitness #health #motivation",
            "Art that's capturing hearts #art #creative #inspiration"
        ]
        
        mock_data = []
        for i in range(min(max_results, len(mock_captions))):
            mock_post = {
                'id': f'instagram_demo_{i}',
                'title': mock_captions[i],
                'platform': 'instagram',
                'author': f'Influencer_{i}',
                'published_date': (datetime.now() - timedelta(hours=i*3)).isoformat(),
                'like_count': 5000 + (i * 500),
                'comment_count': 200 + (i * 20),
                'hashtags': ['fashion', 'viral', 'trending', 'lifestyle']
            }
            mock_data.append(mock_post)
        
        return mock_data