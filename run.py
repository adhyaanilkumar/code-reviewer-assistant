#!/usr/bin/env python3
"""
Code Review Assistant - Main Entry Point

This script provides an easy way to run the Code Review Assistant application.
It handles environment setup and starts the FastAPI server.
"""

import os
import sys
import uvicorn
from pathlib import Path

def check_environment():
    """Check if required environment variables are set."""
    env_file = Path(".env")
    if not env_file.exists():
        print("Warning: .env file not found!")
        print("Please copy env.example to .env and add your OpenAI API key:")
        print("   cp env.example .env")
        print("   # Then edit .env and add: OPENAI_API_KEY=your_key_here")
        print()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set!")
        print("Please set your OpenAI API key in the .env file")
        return False
    
    return True

def main():
    """Main entry point for the application."""
    print("Starting Code Review Assistant...")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Create necessary directories
    os.makedirs("static", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    
    print("Environment check passed")
    print("Starting web server...")
    print("Open your browser and go to: http://localhost:8000")
    print("API documentation: http://localhost:8000/docs")
    print("=" * 50)
    
    # Start the server
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nShutting down Code Review Assistant...")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
