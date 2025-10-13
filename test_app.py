#!/usr/bin/env python3
"""
Test script for Code Review Assistant

This script tests the basic functionality of the application
without requiring an OpenAI API key.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

def test_imports():
    """Test that all modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        from app import database, models, llm_service, main
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_database_creation():
    """Test database table creation."""
    print("🧪 Testing database creation...")
    
    try:
        from app.database import create_tables, engine
        create_tables()
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_models():
    """Test Pydantic models."""
    print("🧪 Testing models...")
    
    try:
        from app.models import CodeReviewRequest, CodeReviewResponse, ReviewScores, ReviewReport
        
        # Test CodeReviewRequest
        request = CodeReviewRequest(
            filename="test.py",
            content="def hello():\n    print('Hello, World!')"
        )
        assert request.filename == "test.py"
        
        # Test ReviewScores
        scores = ReviewScores(
            readability_score=8.5,
            modularity_score=7.0,
            bug_risk_score=6.0,
            overall_score=7.5
        )
        assert scores.overall_score == 7.5
        
        print("✅ Models work correctly")
        return True
    except Exception as e:
        print(f"❌ Model error: {e}")
        return False

def test_llm_service_structure():
    """Test LLM service structure (without API call)."""
    print("🧪 Testing LLM service structure...")
    
    try:
        from app.llm_service import LLMCodeReviewer
        
        # Create instance (will fail if no API key, but that's expected)
        reviewer = LLMCodeReviewer()
        
        # Test helper methods
        ext = reviewer._get_file_extension("test.py")
        assert ext == "py"
        
        ext = reviewer._get_file_extension("test")
        assert ext == "text"
        
        # Test fallback response creation
        fallback = reviewer._create_fallback_response("Test report")
        assert "report" in fallback
        assert "scores" in fallback
        assert "suggestions" in fallback
        
        print("✅ LLM service structure is correct")
        return True
    except Exception as e:
        print(f"❌ LLM service error: {e}")
        return False

def test_file_structure():
    """Test that all required files exist."""
    print("🧪 Testing file structure...")
    
    required_files = [
        "app/__init__.py",
        "app/main.py",
        "app/database.py",
        "app/models.py",
        "app/llm_service.py",
        "templates/index.html",
        "static/style.css",
        "static/script.js",
        "requirements.txt",
        "README.md",
        "run.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files exist")
        return True

def main():
    """Run all tests."""
    print("🚀 Running Code Review Assistant Tests")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_imports,
        test_models,
        test_database_creation,
        test_llm_service_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application structure is correct.")
        print("💡 To run the full application:")
        print("   1. Set up your OpenAI API key in .env file")
        print("   2. Run: python run.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
