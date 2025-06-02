#!/usr/bin/env python3
"""
Test runner script for MongoDB Backup Service
"""

import sys
import subprocess
from pathlib import Path

def run_tests():
    """Run all tests for the MongoDB Backup Service."""
    
    # Add src to Python path
    project_root = Path(__file__).parent.parent
    src_path = project_root / "src"
    sys.path.insert(0, str(src_path))
    
    print("MongoDB Backup Service - Test Runner")
    print("=" * 50)
    
    # Run integration tests
    test_file = project_root / "src" / "tests" / "test_backup.py"
    
    try:
        print("Running integration tests...")
        result = subprocess.run([sys.executable, str(test_file)], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
            
        if result.returncode == 0:
            print("SUCCESS: All tests passed!")
        else:
            print("ERROR: Some tests failed!")
            return False
            
    except Exception as e:
        print(f"ERROR: Failed to run tests: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 