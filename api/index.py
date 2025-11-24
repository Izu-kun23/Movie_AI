"""
Vercel serverless function entry point.
Imports the FastAPI app from backend/main.py
"""
import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import the FastAPI app
from main import app

# Export for Vercel
__all__ = ['app']

