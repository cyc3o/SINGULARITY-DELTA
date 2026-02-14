"""
Data Loader Service
Handles loading and parsing of system data files
"""
import json
from typing import Dict, Any
from pathlib import Path


class DataLoader:
    """
    Loads system data from various sources.
    Supports JSON files and dictionaries.
    """
    
    @staticmethod
    def load_from_file(filepath: str) -> Dict[str, Any]:
        """
        Load system data from a JSON file.
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            Parsed data dictionary
            
        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If file contains invalid JSON
        """
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        if not path.is_file():
            raise ValueError(f"Not a file: {filepath}")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data
    
    @staticmethod
    def load_from_string(json_string: str) -> Dict[str, Any]:
        """
        Load system data from a JSON string.
        
        Args:
            json_string: JSON formatted string
            
        Returns:
            Parsed data dictionary
            
        Raises:
            json.JSONDecodeError: If string contains invalid JSON
        """
        return json.loads(json_string)
    
    @staticmethod
    def load_from_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and return dictionary data.
        
        Args:
            data: Dictionary to validate
            
        Returns:
            Validated data dictionary
            
        Raises:
            ValueError: If data is not a dictionary
        """
        if not isinstance(data, dict):
            raise ValueError(f"Data must be a dictionary, got {type(data).__name__}")
        
        return data
    
    @staticmethod
    def get_target_name(data: Dict[str, Any]) -> str:
        """
        Extract target system name from data.
        
        Args:
            data: System data dictionary
            
        Returns:
            System name or 'unknown'
        """
        return data.get("system_name", "unknown")
