"""
Memory Store - Manages short-term and long-term memory for the system
"""

from typing import Dict, Any, List, Optional
from collections import defaultdict
import json
from pathlib import Path


class MemoryStore:
    """
    Centralized memory management for all agents
    """
    
    def __init__(self, persistence_file: Optional[str] = None):
        self.short_term_memory = {}
        self.long_term_memory = {}
        self.conversation_history = []
        self.completed_phases = set()
        self.current_phase = None
        self.persistence_file = persistence_file
        
        if persistence_file and Path(persistence_file).exists():
            self.load_from_file(persistence_file)
    
    def store(self, key: str, value: Any, long_term: bool = False):
        """
        Store information in memory
        
        Args:
            key: Memory key
            value: Value to store
            long_term: If True, store in long-term memory
        """
        if long_term:
            self.long_term_memory[key] = value
        else:
            self.short_term_memory[key] = value
        
        # Add to conversation history
        self.conversation_history.append({
            "key": key,
            "type": "store",
            "long_term": long_term
        })
    
    def retrieve(self, key: str, default: Any = None) -> Any:
        """Retrieve information from memory"""
        # Check short-term first
        if key in self.short_term_memory:
            return self.short_term_memory[key]
        
        # Then check long-term
        if key in self.long_term_memory:
            return self.long_term_memory[key]
        
        return default
    
    def get_all(self) -> Dict[str, Any]:
        """Get all memory contents"""
        return {
            **self.long_term_memory,
            **self.short_term_memory
        }
    
    def clear_short_term(self):
        """Clear short-term memory"""
        self.short_term_memory = {}
    
    def mark_phase_complete(self, phase: str):
        """Mark a pipeline phase as complete"""
        self.completed_phases.add(phase)
        self.current_phase = None
    
    def set_current_phase(self, phase: str):
        """Set the current pipeline phase"""
        self.current_phase = phase
    
    def get_completed_phases(self) -> List[str]:
        """Get list of completed phases"""
        return list(self.completed_phases)
    
    def get_current_phase(self) -> Optional[str]:
        """Get current phase"""
        return self.current_phase
    
    def save_to_file(self, filepath: str):
        """Save memory to file"""
        data = {
            "short_term": self.short_term_memory,
            "long_term": self.long_term_memory,
            "completed_phases": list(self.completed_phases),
            "current_phase": self.current_phase
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def load_from_file(self, filepath: str):
        """Load memory from file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.short_term_memory = data.get("short_term", {})
        self.long_term_memory = data.get("long_term", {})
        self.completed_phases = set(data.get("completed_phases", []))
        self.current_phase = data.get("current_phase")
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
    
    def add_to_history(self, agent: str, action: str, content: str):
        """Add entry to conversation history"""
        self.conversation_history.append({
            "agent": agent,
            "action": action,
            "content": content[:200]  # Truncate long content
        })