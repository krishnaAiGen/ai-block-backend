#!/usr/bin/env python3
"""
Main entry point for AI Block Backend
"""

import sys
import os

# Add source directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'source'))

if __name__ == "__main__":
    import uvicorn
    from source.api.main import app
    
    print("🚀 Starting AI Block Backend...")
    print("📡 Server will be available at: http://localhost:8000")
    print("📖 API docs will be available at: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000) 