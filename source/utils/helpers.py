"""
Utility functions for AI Block Backend
"""

import sys
import os
from typing import Optional, Dict, Any

def add_source_to_path():
    """Add source directory to Python path"""
    source_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'source')
    if source_path not in sys.path:
        sys.path.insert(0, source_path)

def format_address(address: str, length: int = 8) -> str:
    """Format a blockchain address for display"""
    if not address or len(address) <= length * 2:
        return address
    return f"{address[:length]}...{address[-length:]}"

def convert_units_to_ksm(units: str) -> float:
    """Convert smallest units to KSM"""
    try:
        units_int = int(units)
        return units_int / 1_000_000_000_000  # 1 KSM = 1e12 units
    except (ValueError, TypeError):
        return 0.0

def format_ksm_amount(amount: float) -> str:
    """Format KSM amount for display"""
    if amount >= 1_000_000:
        return f"{amount/1_000_000:.2f}M KSM"
    elif amount >= 1_000:
        return f"{amount/1_000:.2f}K KSM"
    else:
        return f"{amount:.4f} KSM"

def validate_environment() -> Dict[str, Any]:
    """Validate environment setup"""
    from source.config import settings
    
    validation_result = {
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Check OpenAI API key
    if not settings.OPENAI_API_KEY:
        validation_result["valid"] = False
        validation_result["errors"].append("OPENAI_API_KEY is not set")
    
    # Check GraphQL endpoint
    if not settings.GRAPHQL_ENDPOINT:
        validation_result["valid"] = False
        validation_result["errors"].append("GRAPHQL_ENDPOINT is not set")
    
    # Check ChromaDB path
    if not os.path.exists(settings.CHROMA_DB_PATH):
        validation_result["warnings"].append(f"ChromaDB path does not exist: {settings.CHROMA_DB_PATH}")
    
    return validation_result

def get_system_info() -> Dict[str, Any]:
    """Get system information"""
    import platform
    
    return {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "architecture": platform.architecture()[0],
        "processor": platform.processor()
    } 