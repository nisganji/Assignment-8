"""
Pytest configuration and shared fixtures for Flask website tests.
This file provides common test setup and teardown functionality.
"""

import pytest
import os
import tempfile
import sqlite3
import DAL
import contact_DAL


@pytest.fixture(scope="function")
def temp_dir():
    """Create a temporary directory for each test"""
    temp_dir = tempfile.TemporaryDirectory()
    yield temp_dir
    temp_dir.cleanup()


@pytest.fixture(scope="function")
def test_projects_db(temp_dir):
    """Set up a test projects database"""
    original_filename = DAL.DB_FILENAME
    DAL.DB_FILENAME = os.path.join(temp_dir.name, "test_projects.db")
    DAL.init_db()
    yield DAL.DB_FILENAME
    DAL.DB_FILENAME = original_filename


@pytest.fixture(scope="function")
def test_contacts_db(temp_dir):
    """Set up a test contacts database"""
    original_filename = contact_DAL.DB_FILENAME
    contact_DAL.DB_FILENAME = os.path.join(temp_dir.name, "test_contacts.db")
    contact_DAL.init_contact_db()
    yield contact_DAL.DB_FILENAME
    contact_DAL.DB_FILENAME = original_filename


@pytest.fixture(scope="function")
def test_databases(temp_dir):
    """Set up both test databases"""
    # Set up projects database
    original_projects_filename = DAL.DB_FILENAME
    DAL.DB_FILENAME = os.path.join(temp_dir.name, "test_projects.db")
    DAL.init_db()
    
    # Set up contacts database
    original_contacts_filename = contact_DAL.DB_FILENAME
    contact_DAL.DB_FILENAME = os.path.join(temp_dir.name, "test_contacts.db")
    contact_DAL.init_contact_db()
    
    yield {
        'projects_db': DAL.DB_FILENAME,
        'contacts_db': contact_DAL.DB_FILENAME
    }
    
    # Restore original filenames
    DAL.DB_FILENAME = original_projects_filename
    contact_DAL.DB_FILENAME = original_contacts_filename


@pytest.fixture(scope="function")
def sample_projects():
    """Sample project data for testing"""
    return [
        {
            'title': 'Sample Project 1',
            'description': 'This is a sample project description',
            'image_file_name': 'sample1.jpg'
        },
        {
            'title': 'Sample Project 2',
            'description': 'Another sample project with different content',
            'image_file_name': 'sample2.png'
        },
        {
            'title': 'Project with Special Characters: !@#$%',
            'description': 'Description with émojis 🚀 and unicode: ñáéíóú',
            'image_file_name': 'special_chars.webp'
        }
    ]


@pytest.fixture(scope="function")
def sample_contacts():
    """Sample contact data for testing"""
    return [
        {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123'
        },
        {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'password': 'securepassword456'
        },
        {
            'first_name': 'José',
            'last_name': "O'Connor-Smith",
            'email': 'jose.o\'connor-smith@example.com',
            'password': 'P@ssw0rd!@#$%^&*()'
        }
    ]


@pytest.fixture(scope="function")
def flask_app():
    """Set up Flask app for testing"""
    from app import app
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app


@pytest.fixture(scope="function")
def flask_client(flask_app, test_databases):
    """Set up Flask test client with test databases"""
    with flask_app.test_client() as client:
        yield client


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom settings"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically"""
    for item in items:
        # Add unit marker to database tests
        if "test_database" in item.nodeid or "test_projects" in item.nodeid or "test_contact" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        
        # Add integration marker to app tests
        if "test_app" in item.nodeid:
            item.add_marker(pytest.mark.integration)


# Test data validation helpers
def validate_project_structure(project):
    """Validate that a project has the expected structure"""
    required_fields = ['id', 'Title', 'Description', 'ImageFileName', 'CreatedAt']
    for field in required_fields:
        assert field in project, f"Project missing required field: {field}"
    
    assert isinstance(project['id'], int)
    assert isinstance(project['Title'], str)
    assert isinstance(project['Description'], str)
    assert isinstance(project['ImageFileName'], str)


def validate_contact_structure(contact):
    """Validate that a contact has the expected structure"""
    required_fields = ['id', 'first_name', 'last_name', 'email', 'password', 'created_at']
    for field in required_fields:
        assert field in contact, f"Contact missing required field: {field}"
    
    assert isinstance(contact['id'], int)
    assert isinstance(contact['first_name'], str)
    assert isinstance(contact['last_name'], str)
    assert isinstance(contact['email'], str)
    assert isinstance(contact['password'], str)
