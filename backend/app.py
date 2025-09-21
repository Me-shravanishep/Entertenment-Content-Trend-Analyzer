# backend/app.py
"""Main Flask application factory"""

from flask import Flask, jsonify
from flask_cors import CORS
from config.settings import Config
from backend.routes.data_routes import data_bp
from backend.routes.analytics_routes import analytics_bp
import logging

def create_app():
    """Create and configure Flask application"""
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for frontend communication
    CORS(app, origins=["http://localhost:8501"])
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Validate configuration
    Config.validate_config()
    
    # Register blueprints
    app.register_blueprint(data_bp, url_prefix='/api/data')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'message': 'Entertainment Trend Analyzer API is running',
            'version': '1.0.0'
        })
    
    # Root endpoint
    @app.route('/')
    def root():
        """Root endpoint"""
        return jsonify({
            'message': 'Entertainment Content Trend Analyzer API',
            'endpoints': {
                'health': '/api/health',
                'youtube_trending': '/api/data/youtube/trending',
                'instagram_trending': '/api/data/instagram/trending',
                'analytics_summary': '/api/analytics/summary'
            }
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    logger.info("Flask application created successfully")
    return app