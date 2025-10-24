# Flask Website Testing Suite

This directory contains comprehensive test scripts for the Flask website with database-driven projects page. The tests are designed to work with GitHub Actions for automated verification.

## Test Files

### Core Test Files
- **`test_database.py`** - Tests database connections and operations for both projects and contacts databases
- **`test_projects.py`** - Tests project-related functionality including CRUD operations and validation
- **`test_contact.py`** - Tests contact form functionality including form submission and validation
- **`test_app.py`** - Tests Flask routes and application behavior including HTTP requests and responses

### Configuration Files
- **`conftest.py`** - Pytest configuration with shared fixtures and test helpers
- **`pytest.ini`** - Pytest configuration settings
- **`run_tests.py`** - Test runner script for easy local testing

## Test Coverage

### Database Tests (`test_database.py`)
- ✅ Database connection functionality
- ✅ Database file creation
- ✅ Table structure validation
- ✅ CRUD operations for projects
- ✅ CRUD operations for contacts
- ✅ Data validation and error handling
- ✅ Auto-increment ID functionality
- ✅ Timestamp creation

### Project Tests (`test_projects.py`)
- ✅ Project structure validation
- ✅ Project ordering (by ID ASC)
- ✅ Title, description, and image filename validation
- ✅ Special character handling
- ✅ Multiple project insertion
- ✅ Empty data handling
- ✅ Whitespace validation

### Contact Tests (`test_contact.py`)
- ✅ Contact structure validation
- ✅ Contact ordering (by created_at DESC)
- ✅ First name, last name, email, and password validation
- ✅ Special character handling
- ✅ Multiple contact insertion
- ✅ Contact count functionality
- ✅ Empty data handling

### Flask App Tests (`test_app.py`)
- ✅ All route accessibility (GET requests)
- ✅ Form submission (POST requests)
- ✅ Form validation and error handling
- ✅ Flash message functionality
- ✅ Redirect behavior
- ✅ Database integration
- ✅ Error handling (404, validation errors)
- ✅ Multiple submissions

## Running Tests

### Prerequisites
Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Running All Tests
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=. --cov-report=html
```

### Running Individual Test Files
```bash
# Test database functionality
pytest test_database.py -v

# Test project functionality
pytest test_projects.py -v

# Test contact functionality
pytest test_contact.py -v

# Test Flask app functionality
pytest test_app.py -v
```

### Running by Test Type
```bash
# Run only unit tests
pytest -m unit -v

# Run only integration tests
pytest -m integration -v

# Skip slow tests
pytest -m "not slow" -v
```

### Using the Test Runner Script
```bash
# Run the comprehensive test suite
python run_tests.py
```

## GitHub Actions Integration

The tests are configured to run automatically on GitHub Actions with the workflow file `.github/workflows/test.yml`. The workflow:

- Runs on Python versions 3.8, 3.9, 3.10, and 3.11
- Installs dependencies from `requirements.txt`
- Runs all test files individually
- Generates coverage reports
- Uploads coverage to Codecov

## Test Features

### Database Isolation
- Each test uses temporary databases to avoid conflicts
- Tests clean up after themselves automatically
- No interference between test runs

### Comprehensive Validation
- Tests cover both success and failure scenarios
- Validates data structure and types
- Tests edge cases and special characters
- Validates error messages and exceptions

### Flask Integration
- Tests actual HTTP requests and responses
- Validates form submission and validation
- Tests flash messages and redirects
- Verifies database integration

### Fixtures and Helpers
- Shared test data fixtures
- Database setup/teardown helpers
- Validation helper functions
- Flask app configuration for testing

## Test Data

The tests use sample data that includes:
- Normal project and contact data
- Special characters and unicode
- Edge cases (empty strings, whitespace)
- Various file formats and email formats

## Coverage Reports

After running tests with coverage, you can view detailed reports:
- HTML report: `htmlcov/index.html`
- Terminal output: Shows coverage percentages
- XML report: `coverage.xml` (for CI/CD integration)

## Continuous Integration

The test suite is designed to work seamlessly with:
- GitHub Actions
- Codecov integration
- Multiple Python versions
- Automated testing on pull requests

## Troubleshooting

### Common Issues
1. **Database errors**: Ensure test databases are properly isolated
2. **Import errors**: Make sure all dependencies are installed
3. **Flask app errors**: Check that the app is properly configured for testing

### Debug Mode
Run tests with more verbose output:
```bash
pytest -v -s --tb=long
```

This testing suite ensures your Flask website works correctly and can be automatically verified by GitHub Actions.
