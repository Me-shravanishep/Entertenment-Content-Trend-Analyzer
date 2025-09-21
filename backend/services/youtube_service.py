# backend/services/youtube_service.py
"""YouTube data collection service"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from config.settings import Config
import requests
import re

class YouTubeService:
    """YouTube Data API service"""
    
    def __init__(self):
        self.api_key = Config.YOUTUBE_API_KEY
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    def search_trending_videos(self, category_id: str = "24", max_results: int = 50) -> List[Dict[str, Any]]:
        """Get trending videos from YouTube"""
        if self.api_key:
            try:
                return self._get_real_youtube_data(category_id, max_results)
            except Exception as e:
                print(f"YouTube API error: {e}, falling back to mock data")
                return self._get_mock_youtube_data(max_results)
        else:
            print("No YouTube API key found, using mock data")
            return self._get_mock_youtube_data(max_results)
    
    def _get_real_youtube_data(self, category_id: str = "24", max_results: int = 50) -> List[Dict[str, Any]]:
        """Get real YouTube trending data using API"""
        # Get trending videos
        trending_url = f"{self.base_url}/videos"
        params = {
            'part': 'snippet,statistics',
            'chart': 'mostPopular',
            'videoCategoryId': category_id,
            'regionCode': 'US',  # You can change this
            'maxResults': min(max_results, 50),
            'key': self.api_key
        }
        
        response = requests.get(trending_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        videos = []
        for item in data.get('items', []):
            video = self._format_youtube_video(item)
            videos.append(video)
        
        return videos
    
    def _format_youtube_video(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Format YouTube API response to our standard format"""
        snippet = item.get('snippet', {})
        statistics = item.get('statistics', {})
        
        # Extract hashtags from description
        description = snippet.get('description', '')
        hashtags = self._extract_hashtags(description + ' ' + snippet.get('title', ''))
        
        return {
            'id': f"youtube_{item.get('id')}",
            'title': snippet.get('title', ''),
            'description': description[:500],  # Truncate for storage
            'platform': 'youtube',
            'author': snippet.get('channelTitle', ''),
            'published_date': snippet.get('publishedAt', datetime.now().isoformat()),
            'url': f"https://www.youtube.com/watch?v={item.get('id')}",
            'view_count': int(statistics.get('viewCount', 0)),
            'like_count': int(statistics.get('likeCount', 0)),
            'comment_count': int(statistics.get('commentCount', 0)),
            'hashtags': hashtags
        }
    
    def _extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from text"""
        hashtag_pattern = r'#\w+'
        hashtags = re.findall(hashtag_pattern, text.lower())
        return [tag[1:] for tag in hashtags[:10]]  # Limit to 10 hashtags, remove #
    
    def _get_mock_youtube_data(self, max_results: int = 25) -> List[Dict[str, Any]]:
        """Generate mock YouTube data for development"""
        mock_titles = [
            "Top 10 Trending Dance Moves 2024 #viral #dance #trending",
            "Celebrity Interview Goes Viral #celebrity #interview",
            "Movie Trailer Reaction #movie #reaction #trailer",
            "Music Video Behind Scenes #music #behindthescenes",
            "Comedy Sketch Viral #comedy #funny #viral",
        ]
        
        mock_data = []
        for i in range(min(max_results, len(mock_titles))):
            mock_video = {
                'id': f'youtube_demo_{i}',
                'title': mock_titles[i],
                'platform': 'youtube',
                'author': f'Creator_{i}',
                'published_date': (datetime.now() - timedelta(hours=i*2)).isoformat(),
                'view_count': 10000 + (i * 1000),
                'like_count': 500 + (i * 50),
                'comment_count': 100 + (i * 10),
                'hashtags': ['viral', 'trending', 'entertainment']
            }
            mock_data.append(mock_video)
        
        return mock_data