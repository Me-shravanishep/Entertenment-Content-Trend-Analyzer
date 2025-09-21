# mcp_integration/trend_analyzer.py
"""MCP-powered trend analysis"""

from typing import Dict, Any, List
from datetime import datetime

class TrendAnalyzer:
    """Advanced trend analysis using MCP"""
    
    def __init__(self):
        # Import here to avoid circular imports
        try:
            from .mcp_client import MCPClient
            from .context_manager import ContextManager
            self.mcp_client = MCPClient()
            self.context_manager = ContextManager()
        except:
            # Fallback if MCP components aren't available
            self.mcp_client = None
            self.context_manager = None
    
    def analyze_content_trends(self, content_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Comprehensive trend analysis"""
        
        if not content_items:
            return {
                'trend_detection': {'trending_hashtags': []},
                'sentiment_overview': {},
                'total_analyzed': 0,
                'context_id': 'empty_analysis',
                'timestamp': datetime.now().isoformat()
            }
        
        # Create analysis context
        context_id = f"trend_analysis_{datetime.now().timestamp()}"
        
        if self.context_manager:
            self.context_manager.create_context(context_id, {
                'content_count': len(content_items),
                'platforms': list(set(item.get('platform') for item in content_items)),
                'analysis_type': 'comprehensive_trends'
            })
        
        # Analyze trends
        if self.mcp_client:
            trend_results = self.mcp_client.detect_trends(content_items)
        else:
            # Fallback trend analysis
            trend_results = self._fallback_trend_analysis(content_items)
        
        # Perform sentiment analysis on titles
        sentiments = []
        for item in content_items:
            if item.get('title'):
                if self.mcp_client:
                    sentiment = self.mcp_client.analyze_sentiment(item['title'])
                    sentiments.append(sentiment['label'])
                else:
                    sentiments.append('neutral')  # Fallback
        
        from collections import Counter
        sentiment_dist = dict(Counter(sentiments))
        
        return {
            'trend_detection': trend_results,
            'sentiment_overview': sentiment_dist,
            'total_analyzed': len(content_items),
            'context_id': context_id,
            'timestamp': datetime.now().isoformat()
        }
    
    def _fallback_trend_analysis(self, content_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback trend analysis when MCP is not available"""
        hashtags = []
        for item in content_items:
            hashtags.extend(item.get('hashtags', []))
        
        from collections import Counter
        top_hashtags = Counter(hashtags).most_common(10)
        
        return {
            'trending_hashtags': [{'tag': tag, 'count': count} for tag, count in top_hashtags],
            'analysis_timestamp': datetime.now().isoformat(),
            'method': 'fallback_trend_detection'
        }