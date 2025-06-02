#!/usr/bin/env python3
"""
MongoDB Backup Service - Main Entry Point
"""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.app.main import app

if __name__ == "__main__":
    app.run() 