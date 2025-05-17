"""
Simple memory tool for storing and retrieving user preferences and context.
"""

import os
import json
from typing import Dict, List, Optional, Union
from datetime import datetime
from pathlib import Path

from strands import tool

# Directory for storing memory files
MEMORY_DIR = Path("./memory")

# Create memory directory if it doesn't exist
os.makedirs(MEMORY_DIR, exist_ok=True)

@tool
def memory_tool(action: str, user_id: str, content: Optional[str] = None, query: Optional[str] = None) -> Union[str, List[Dict[str, str]]]:
    """
    Store, retrieve, or list memory items for a user.
    
    Args:
        action: One of 'store', 'retrieve', or 'list'
        user_id: User identifier for memory persistence
        content: Text content to store (required for 'store' action)
        query: Search term for retrieving memories (optional for 'retrieve' action)
    
    Returns:
        String or list of memory items, depending on the action
    """
    # Validate user_id
    if not user_id or not isinstance(user_id, str):
        return "Error: Valid user_id is required"
    
    # Ensure valid action
    action = action.lower()
    if action not in ["store", "retrieve", "list"]:
        return f"Error: Invalid action '{action}'. Must be 'store', 'retrieve', or 'list'."
    
    # Get memory file path for this user
    memory_file = MEMORY_DIR / f"{user_id}.json"
    
    # Initialize memories
    memories = []
    
    # Load existing memories if file exists
    if memory_file.exists():
        try:
            with open(memory_file, "r") as f:
                memories = json.load(f)
        except Exception as e:
            return f"Error loading memories: {str(e)}"
    
    # Handle 'store' action
    if action == "store":
        if not content:
            return "Error: Content is required for 'store' action"
        
        # Create new memory entry
        memory_entry = {
            "timestamp": datetime.now().isoformat(),
            "content": content
        }
        
        # Add to memories and save
        memories.append(memory_entry)
        
        try:
            with open(memory_file, "w") as f:
                json.dump(memories, f, indent=2)
            return f"Successfully stored memory for user {user_id}"
        except Exception as e:
            return f"Error saving memory: {str(e)}"
    
    # Handle 'retrieve' action
    elif action == "retrieve":
        if not memories:
            return f"No memories found for user {user_id}"
        
        # If query is provided, filter memories
        if query:
            query = query.lower()
            filtered_memories = [
                m for m in memories 
                if query in m.get("content", "").lower()
            ]
            
            if not filtered_memories:
                return f"No memories found matching query '{query}'"
            
            return filtered_memories
        else:
            # Return all memories by default
            return memories
    
    # Handle 'list' action
    elif action == "list":
        if not memories:
            return f"No memories found for user {user_id}"
        
        return memories
    
    return "Invalid action"
