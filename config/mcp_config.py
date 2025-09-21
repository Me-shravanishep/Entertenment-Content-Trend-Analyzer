"""MCP (Model Context Protocol) Configuration"""

import json
from typing import Dict, Any, Optional
from pathlib import Path

class MCPConfig:
    """MCP Configuration Manager"""
    
    def __init__(self):
        self.config_file = Path(__file__).parent.parent / 'data' / 'mcp_config.json'
        self.default_config = {
            "model_settings": {
                "name": "claude-3-sonnet",
                "temperature": 0.7,
                "max_tokens": 4000,
                "context_window": 100000
            },
            "analysis_prompts": {
                "sentiment_analysis": "Analyze the sentiment of the following social media content: {content}",
                "trend_detection": "Identify trending topics from this data: {data}",
                "engagement_prediction": "Predict engagement for content with these features: {features}"
            },
            "context_management": {
                "max_context_items": 1000,
                "context_retention_hours": 24,
                "auto_cleanup": True
            },
            "processing_settings": {
                "batch_size": 10,
                "parallel_processing": True,
                "retry_attempts": 3
            }
        }
    
    def load_config(self) -> Dict[str, Any]:
        """Load MCP configuration"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults for any missing keys
                    return {**self.default_config, **config}
            else:
                self.save_config(self.default_config)
                return self.default_config
        except Exception as e:
            print(f"Error loading MCP config: {e}")
            return self.default_config
    
    def save_config(self, config: Dict[str, Any]) -> None:
        """Save MCP configuration"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving MCP config: {e}")
    
    def get_prompt_template(self, prompt_type: str) -> Optional[str]:
        """Get prompt template by type"""
        config = self.load_config()
        return config.get("analysis_prompts", {}).get(prompt_type)
    
    def update_model_settings(self, settings: Dict[str, Any]) -> None:
        """Update model settings"""
        config = self.load_config()
        config["model_settings"].update(settings)
        self.save_config(config)

# Initialize global MCP config
mcp_config = MCPConfig()