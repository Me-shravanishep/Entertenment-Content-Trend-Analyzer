"""Database utilities and connection management"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from config.settings import Config

class DatabaseManager:
    """Simple database manager for storing trends data"""
    
    def __init__(self):
        self.db_path = Config.DATA_DIR / 'trends.db'
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Content items table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS content_items (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    platform TEXT NOT NULL,
                    author TEXT,
                    published_date TEXT,
                    url TEXT,
                    view_count INTEGER,
                    like_count INTEGER,
                    comment_count INTEGER,
                    hashtags TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Trending topics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trending_topics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    score REAL,
                    volume INTEGER,
                    growth_rate REAL,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Analytics results table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analytics_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content_id TEXT NOT NULL,
                    sentiment_score REAL,
                    sentiment_label TEXT,
                    engagement_prediction REAL,
                    trending_probability REAL,
                    analysis_timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def insert_content_item(self, item: Dict[str, Any]) -> bool:
        """Insert content item into database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO content_items 
                    (id, title, description, platform, author, published_date, 
                     url, view_count, like_count, comment_count, hashtags)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item['id'], item['title'], item['description'],
                    item['platform'], item['author'], item['published_date'],
                    item['url'], item.get('view_count'), item.get('like_count'),
                    item.get('comment_count'), json.dumps(item.get('hashtags', []))
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error inserting content item: {e}")
            return False
    
    def get_recent_content(self, platform: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent content items"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if platform:
                    cursor.execute('''
                        SELECT * FROM content_items 
                        WHERE platform = ? 
                        ORDER BY created_at DESC 
                        LIMIT ?
                    ''', (platform, limit))
                else:
                    cursor.execute('''
                        SELECT * FROM content_items 
                        ORDER BY created_at DESC 
                        LIMIT ?
                    ''', (limit,))
                
                columns = [desc[0] for desc in cursor.description]
                results = []
                
                for row in cursor.fetchall():
                    item = dict(zip(columns, row))
                    if item['hashtags']:
                        item['hashtags'] = json.loads(item['hashtags'])
                    results.append(item)
                
                return results
        except Exception as e:
            print(f"Error getting recent content: {e}")
            return []