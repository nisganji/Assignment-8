"""
Test script for database operations and connections.
Tests both projects and contacts database functionality.
"""

import pytest
import sqlite3
import os
import tempfile
import DAL
import contact_DAL


class TestDatabaseConnection:
    """Test database connection functionality"""
    
    def test_projects_database_connection(self):
        """Test that projects database connection works"""
        conn = DAL.get_connection()
        assert conn is not None
        assert isinstance(conn, sqlite3.Connection)
        conn.close()
    
    def test_contacts_database_connection(self):
        """Test that contacts database connection works"""
        conn = contact_DAL.get_connection()
        assert conn is not None
        assert isinstance(conn, sqlite3.Connection)
        conn.close()
    
    def test_projects_database_file_creation(self):
        """Test that projects database file is created"""
        # Use temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            original_filename = DAL.DB_FILENAME
            DAL.DB_FILENAME = os.path.join(temp_dir, "test_projects.db")
            
            try:
                DAL.init_db()
                assert os.path.exists(DAL.DB_FILENAME)
            finally:
                DAL.DB_FILENAME = original_filename
    
    def test_contacts_database_file_creation(self):
        """Test that contacts database file is created"""
        # Use temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            original_filename = contact_DAL.DB_FILENAME
            contact_DAL.DB_FILENAME = os.path.join(temp_dir, "test_contacts.db")
            
            try:
                contact_DAL.init_contact_db()
                assert os.path.exists(contact_DAL.DB_FILENAME)
            finally:
                contact_DAL.DB_FILENAME = original_filename


class TestProjectsDatabase:
    """Test projects database operations"""
    
    def setup_method(self):
        """Set up test database before each test"""
        # Use temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        original_filename = DAL.DB_FILENAME
        DAL.DB_FILENAME = os.path.join(self.temp_dir.name, "test_projects.db")
        DAL.init_db()
    
    def teardown_method(self):
        """Clean up after each test"""
        self.temp_dir.cleanup()
    
    def test_projects_table_structure(self):
        """Test that projects table has correct structure"""
        conn = DAL.get_connection()
        cursor = conn.execute("PRAGMA table_info(projects)")
        columns = cursor.fetchall()
        
        # Check that required columns exist
        column_names = [col[1] for col in columns]
        assert 'id' in column_names
        assert 'Title' in column_names
        assert 'Description' in column_names
        assert 'ImageFileName' in column_names
        assert 'CreatedAt' in column_names
        
        conn.close()
    
    def test_list_projects_returns_list(self):
        """Test that list_projects returns a list"""
        projects = DAL.list_projects()
        assert isinstance(projects, list)
    
    def test_list_projects_has_seed_data(self):
        """Test that seed data is inserted correctly"""
        projects = DAL.list_projects()
        assert len(projects) >= 2  # Should have at least 2 seed projects
        
        # Check that seed projects exist
        titles = [project['Title'] for project in projects]
        assert "Sign Language Recognition using Deep Learning" in titles
        assert "Decentro Vault: Decentralized Banking System" in titles
    
    def test_insert_project_success(self):
        """Test successful project insertion"""
        initial_count = len(DAL.list_projects())
        
        DAL.insert_project("Test Project", "Test Description", "test.jpg")
        
        projects = DAL.list_projects()
        assert len(projects) == initial_count + 1
        
        # Check that the new project was added
        new_project = next((p for p in projects if p['Title'] == "Test Project"), None)
        assert new_project is not None
        assert new_project['Description'] == "Test Description"
        assert new_project['ImageFileName'] == "test.jpg"
    
    def test_insert_project_validation(self):
        """Test project insertion validation"""
        # Test empty title
        with pytest.raises(ValueError, match="All fields.*are required"):
            DAL.insert_project("", "Description", "image.jpg")
        
        # Test empty description
        with pytest.raises(ValueError, match="All fields.*are required"):
            DAL.insert_project("Title", "", "image.jpg")
        
        # Test empty image file name
        with pytest.raises(ValueError, match="All fields.*are required"):
            DAL.insert_project("Title", "Description", "")
        
        # Test None values
        with pytest.raises(ValueError, match="All fields.*are required"):
            DAL.insert_project(None, "Description", "image.jpg")


class TestContactsDatabase:
    """Test contacts database operations"""
    
    def setup_method(self):
        """Set up test database before each test"""
        # Use temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        original_filename = contact_DAL.DB_FILENAME
        contact_DAL.DB_FILENAME = os.path.join(self.temp_dir.name, "test_contacts.db")
        contact_DAL.init_contact_db()
    
    def teardown_method(self):
        """Clean up after each test"""
        self.temp_dir.cleanup()
    
    def test_contacts_table_structure(self):
        """Test that contacts table has correct structure"""
        conn = contact_DAL.get_connection()
        cursor = conn.execute("PRAGMA table_info(contacts)")
        columns = cursor.fetchall()
        
        # Check that required columns exist
        column_names = [col[1] for col in columns]
        assert 'id' in column_names
        assert 'first_name' in column_names
        assert 'last_name' in column_names
        assert 'email' in column_names
        assert 'password' in column_names
        assert 'created_at' in column_names
        
        conn.close()
    
    def test_list_contacts_returns_list(self):
        """Test that list_contacts returns a list"""
        contacts = contact_DAL.list_contacts()
        assert isinstance(contacts, list)
    
    def test_insert_contact_success(self):
        """Test successful contact insertion"""
        initial_count = contact_DAL.get_contact_count()
        
        contact_DAL.insert_contact("John", "Doe", "john@example.com", "password123")
        
        assert contact_DAL.get_contact_count() == initial_count + 1
        
        # Check that the contact was added
        contacts = contact_DAL.list_contacts()
        new_contact = next((c for c in contacts if c['email'] == "john@example.com"), None)
        assert new_contact is not None
        assert new_contact['first_name'] == "John"
        assert new_contact['last_name'] == "Doe"
        assert new_contact['password'] == "password123"
    
    def test_insert_contact_validation(self):
        """Test contact insertion validation"""
        # Test empty first name
        with pytest.raises(ValueError, match="All fields.*are required"):
            contact_DAL.insert_contact("", "Doe", "john@example.com", "password123")
        
        # Test empty last name
        with pytest.raises(ValueError, match="All fields.*are required"):
            contact_DAL.insert_contact("John", "", "john@example.com", "password123")
        
        # Test empty email
        with pytest.raises(ValueError, match="All fields.*are required"):
            contact_DAL.insert_contact("John", "Doe", "", "password123")
        
        # Test empty password
        with pytest.raises(ValueError, match="All fields.*are required"):
            contact_DAL.insert_contact("John", "Doe", "john@example.com", "")
    
    def test_get_contact_count(self):
        """Test contact count functionality"""
        initial_count = contact_DAL.get_contact_count()
        
        # Add a contact
        contact_DAL.insert_contact("Jane", "Smith", "jane@example.com", "password456")
        
        assert contact_DAL.get_contact_count() == initial_count + 1
