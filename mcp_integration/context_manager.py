# mcp_integration/context_manager.py
"""MCP context management"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

class ContextManager:
    """Manage MCP contexts for different analysis tasks"""
    
    def __init__(self):
        self.contexts = {}
        self.max_contexts = 100
    
    def create_context(self, context_id: str, data: Dict[str, Any]) -> None:
        """Create a new context"""
        self.contexts[context_id] = {
            'data': data,
            'created_at': datetime.now(),
            'last_used': datetime.now(),
            'usage_count': 0
        }
        
        # Clean old contexts if needed
        if len(self.contexts) > self.max_contexts:
            self._cleanup_contexts()
    
    def get_context(self, context_id: str) -> Optional[Dict[str, Any]]:
        """Get context by ID"""
        if context_id in self.contexts:
            self.contexts[context_id]['last_used'] = datetime.now()
            self.contexts[context_id]['usage_count'] += 1
            return self.contexts[context_id]['data']
        return None
    
    def _cleanup_contexts(self) -> None:
        """Remove old contexts"""
        cutoff_time = datetime.now() - timedelta(hours=24)
        to_remove = [
            ctx_id for ctx_id, ctx in self.contexts.items()
            if ctx['last_used'] < cutoff_time
        ]
        for ctx_id in to_remove:
            del self.contexts[ctx_id]