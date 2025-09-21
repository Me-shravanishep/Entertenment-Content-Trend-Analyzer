#!/usr/bin/env python3
"""
Backend Core Test File
Place this file in the ROOT directory of your project
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_basic_setup():
    """Test basic setup and configuration"""
    print("🧪 Testing Entertainment Trend Analyzer Backend...")
    print("=" * 50)
    
    try:
        # Test 1: Import configuration
        print("1. Testing configuration import...")
        from config.settings import Config
        print("   ✅ Configuration imported successfully")
        
        # Test 2: Validate config
        print("2. Testing configuration validation...")
        Config.validate_config()
        print("   ✅ Configuration validated")
        
        # Test 3: Test Flask app creation
        print("3. Testing Flask app creation...")
        from backend.app import create_app
        app = create_app()
        print("   ✅ Flask app created successfully")
        
        # Test 4: Test database utilities
        print("4. Testing database utilities...")
        from backend.utils.database import DatabaseManager
        db = DatabaseManager()
        print("   ✅ Database manager initialized")
        
        # Test 5: Test helper functions
        print("5. Testing helper functions...")
        from backend.utils.helpers import clean_text, extract_hashtags
        test_text = "Check out this amazing #trend #viral content!"
        cleaned = clean_text(test_text)
        hashtags = extract_hashtags(test_text)
        print(f"   ✅ Text processing works: {hashtags}")
        
        # Test 6: Test data models
        print("6. Testing data models...")
        from backend.models.content_models import ContentItem
        from datetime import datetime
        
        test_item = ContentItem(
            id="test123",
            title="Test Content",
            description="Test description",
            platform="youtube",
            author="Test Author",
            published_date=datetime.now(),
            url="https://example.com",
            hashtags=["test", "demo"]
        )
        print("   ✅ Content models working")
        
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED! Backend core setup successful!")
        print("✅ Ready to proceed to Step 9 - Backend Services")
        print("=" * 50)
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Import Error: {e}")
        print("   💡 Make sure all files are created and in correct folders")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_environment():
    """Test environment setup"""
    print("\n🌍 Environment Check:")
    print("-" * 30)
    
    # Check Python version
    print(f"Python Version: {sys.version}")
    
    # Check required directories
    required_dirs = ['config', 'backend', 'data', 'mcp_integration']
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}/ exists")
        else:
            print(f"❌ {directory}/ missing")
    
    # Check required files
    required_files = ['.env', 'requirements.txt', 'run.py']
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")

if __name__ == "__main__":
    # Run environment check first
    test_environment()
    
    # Run main tests
    success = test_basic_setup()
    
    if success:
        print("\n🚀 Next Step: Reply with 'Step 6 completed' to get backend services code!")
    else:
        print("\n🔧 Fix the errors above before proceeding.")