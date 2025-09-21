# config/settings.py
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/trends.db')
    
    # API Keys
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
    
    # MCP Configuration
    MCP_ENABLED = os.getenv('MCP_ENABLED', 'true').lower() == 'true'
    MCP_MODEL = os.getenv('MCP_MODEL', 'claude-3-sonnet')
    MCP_CONTEXT_SIZE = int(os.getenv('MCP_CONTEXT_SIZE', '100000'))
    
    # Data Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / 'data'
    RAW_DATA_DIR = DATA_DIR / 'raw'
    PROCESSED_DATA_DIR = DATA_DIR / 'processed'
    EXPORTS_DIR = DATA_DIR / 'exports'
    
    # API Rate Limits
    YOUTUBE_REQUESTS_PER_DAY = 10000
    INSTAGRAM_REQUESTS_PER_HOUR = 200
    
    # Analysis Configuration
    TRENDING_THRESHOLD = 0.7
    SENTIMENT_CACHE_HOURS = 24
    MAX_VIDEOS_PER_REQUEST = 50
    
    @classmethod
    def validate_config(cls):
        """Validate required configuration"""
        missing_keys = []
        
        if not cls.YOUTUBE_API_KEY:
            missing_keys.append('YOUTUBE_API_KEY')
            
        if missing_keys:
            print(f"⚠️  Warning: Missing environment variables: {', '.join(missing_keys)}")
            print("   Some features may not work properly.")
        
        # Create directories if they don't exist
        for directory in [cls.DATA_DIR, cls.RAW_DATA_DIR, 
                         cls.PROCESSED_DATA_DIR, cls.EXPORTS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
        
        return len(missing_keys) == 0