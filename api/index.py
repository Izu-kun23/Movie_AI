"""
Vercel serverless function entry point.
Imports the FastAPI app from backend/main.py
"""
import sys
import os

# Get paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
backend_dir = os.path.join(project_root, 'backend')

# Add backend directory to Python path
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Set working directory to backend for relative file paths (movies.csv)
# This ensures the model can find movies.csv in backend/
os.chdir(backend_dir)

# Import the FastAPI app
from main import app

# Export for Vercel
__all__ = ['app']

