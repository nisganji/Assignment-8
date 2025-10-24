#!/usr/bin/env python3
"""
Test runner script for Flask website tests.
This script provides an easy way to run all tests with different configurations.
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False


def main():
    """Main test runner function"""
    print("Flask Website Test Runner")
    print("=" * 60)
    
    # Check if pytest is installed
    try:
        subprocess.run(["pytest", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ pytest is not installed. Please install it with: pip install pytest")
        sys.exit(1)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ app.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    success = True
    
    # Run individual test files
    test_files = [
        "test_database.py",
        "test_projects.py", 
        "test_contact.py",
        "test_app.py"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            if not run_command(f"pytest {test_file} -v", f"Running {test_file}"):
                success = False
        else:
            print(f"⚠️  {test_file} not found, skipping...")
    
    # Run all tests together
    if not run_command("pytest test_*.py -v", "Running all tests"):
        success = False
    
    # Run tests with coverage
    if not run_command("pytest --cov=. --cov-report=html --cov-report=term", "Running tests with coverage"):
        success = False
    
    # Run only unit tests
    if not run_command("pytest -m unit -v", "Running unit tests only"):
        success = False
    
    # Run only integration tests
    if not run_command("pytest -m integration -v", "Running integration tests only"):
        success = False
    
    print(f"\n{'='*60}")
    if success:
        print("🎉 All tests completed successfully!")
        print("📊 Coverage report generated in htmlcov/index.html")
    else:
        print("❌ Some tests failed. Please check the output above.")
        sys.exit(1)
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
