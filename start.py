#!/usr/bin/env python3
"""
Quick start script for AI Block Backend
"""

import os
import sys
import subprocess
import time

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        sys.exit(1)
    print(f"✅ Python version: {sys.version}")

def check_env_file():
    """Check if .env file exists and validate environment"""
    if not os.path.exists('.env'):
        print("⚠️  .env file not found. Creating from template...")
        if os.path.exists('env.example'):
            import shutil
            shutil.copy('env.example', '.env')
            print("📝 Created .env file from template")
            print("🔑 Please edit .env and add your OpenAI API key")
            return False
        else:
            print("❌ env.example file not found")
            return False
    
    print("✅ .env file exists")
    
    # Validate environment after ensuring .env exists
    try:
        # Add source directory to Python path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'source'))
        
        from source.utils import validate_environment
        validation = validate_environment()
        
        if not validation["valid"]:
            print("❌ Environment validation failed:")
            for error in validation["errors"]:
                print(f"   - {error}")
            return False
        
        if validation["warnings"]:
            print("⚠️  Environment warnings:")
            for warning in validation["warnings"]:
                print(f"   - {warning}")
        
        print("✅ Environment validation passed")
        return True
    except Exception as e:
        print(f"⚠️  Could not validate environment: {e}")
        return True  # Continue anyway

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting AI Block Backend server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("📖 API docs will be available at: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Add source directory to Python path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'source'))
        
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)

def main():
    """Main function"""
    print("🤖 AI Block Backend - Quick Start")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Check environment file
    if not check_env_file():
        print("\n⚠️  Please add your OpenAI API key to .env file and run again")
        sys.exit(1)
    
    # Install dependencies
    install_dependencies()
    
    # Start server
    start_server()

if __name__ == "__main__":
    main() 