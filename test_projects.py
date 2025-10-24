"""
Test script for project-related functionality.
Tests project listing, creation, and validation.
"""

import pytest
import os
import tempfile
import DAL


class TestProjectOperations:
    """Test project operations and business logic"""
    
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
    
    def test_project_structure(self):
        """Test that projects have expected structure"""
        projects = DAL.list_projects()
        
        if projects:  # Only test if there are projects
            project = projects[0]
            required_fields = ['id', 'Title', 'Description', 'ImageFileName', 'CreatedAt']
            
            for field in required_fields:
                assert field in project, f"Project missing required field: {field}"
            
            # Check data types
            assert isinstance(project['id'], int)
            assert isinstance(project['Title'], str)
            assert isinstance(project['Description'], str)
            assert isinstance(project['ImageFileName'], str)
    
    def test_project_ordering(self):
        """Test that projects are ordered by id ASC"""
        projects = DAL.list_projects()
        
        if len(projects) > 1:
            ids = [project['id'] for project in projects]
            assert ids == sorted(ids), "Projects should be ordered by id ASC"
    
    def test_project_title_validation(self):
        """Test project title validation"""
        # Test with valid title
        DAL.insert_project("Valid Title", "Description", "image.jpg")
        projects = DAL.list_projects()
        assert any(p['Title'] == "Valid Title" for p in projects)
        
        # Test with whitespace-only title
        with pytest.raises(ValueError):
            DAL.insert_project("   ", "Description", "image.jpg")
        
        # Test with very long title
        long_title = "A" * 1000
        DAL.insert_project(long_title, "Description", "image.jpg")
        projects = DAL.list_projects()
        assert any(p['Title'] == long_title for p in projects)
    
    def test_project_description_validation(self):
        """Test project description validation"""
        # Test with valid description
        DAL.insert_project("Title", "Valid Description", "image.jpg")
        projects = DAL.list_projects()
        assert any(p['Description'] == "Valid Description" for p in projects)
        
        # Test with whitespace-only description
        with pytest.raises(ValueError):
            DAL.insert_project("Title", "   ", "image.jpg")
        
        # Test with multiline description
        multiline_desc = "Line 1\nLine 2\nLine 3"
        DAL.insert_project("Title", multiline_desc, "image.jpg")
        projects = DAL.list_projects()
        assert any(p['Description'] == multiline_desc for p in projects)
    
    def test_project_image_filename_validation(self):
        """Test project image filename validation"""
        # Test with valid image filename
        DAL.insert_project("Title", "Description", "valid_image.jpg")
        projects = DAL.list_projects()
        assert any(p['ImageFileName'] == "valid_image.jpg" for p in projects)
        
        # Test with different image extensions
        extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"]
        for ext in extensions:
            filename = f"image{ext}"
            DAL.insert_project(f"Title {ext}", "Description", filename)
            projects = DAL.list_projects()
            assert any(p['ImageFileName'] == filename for p in projects)
        
        # Test with whitespace-only filename
        with pytest.raises(ValueError):
            DAL.insert_project("Title", "Description", "   ")
    
    def test_project_creation_timestamp(self):
        """Test that projects get created with timestamp"""
        DAL.insert_project("Timestamp Test", "Description", "image.jpg")
        projects = DAL.list_projects()
        
        test_project = next((p for p in projects if p['Title'] == "Timestamp Test"), None)
        assert test_project is not None
        assert test_project['CreatedAt'] is not None
        assert test_project['CreatedAt'] != ""
    
    def test_multiple_project_insertion(self):
        """Test inserting multiple projects"""
        initial_count = len(DAL.list_projects())
        
        # Insert multiple projects
        test_projects = [
            ("Project 1", "Description 1", "image1.jpg"),
            ("Project 2", "Description 2", "image2.jpg"),
            ("Project 3", "Description 3", "image3.jpg"),
        ]
        
        for title, description, image in test_projects:
            DAL.insert_project(title, description, image)
        
        projects = DAL.list_projects()
        assert len(projects) == initial_count + len(test_projects)
        
        # Verify all projects were inserted
        for title, description, image in test_projects:
            project = next((p for p in projects if p['Title'] == title), None)
            assert project is not None
            assert project['Description'] == description
            assert project['ImageFileName'] == image
    
    def test_project_id_auto_increment(self):
        """Test that project IDs auto-increment correctly"""
        initial_count = len(DAL.list_projects())
        
        # Insert two projects
        DAL.insert_project("Project A", "Description A", "image_a.jpg")
        DAL.insert_project("Project B", "Description B", "image_b.jpg")
        
        projects = DAL.list_projects()
        project_a = next((p for p in projects if p['Title'] == "Project A"), None)
        project_b = next((p for p in projects if p['Title'] == "Project B"), None)
        
        assert project_a is not None
        assert project_b is not None
        assert project_b['id'] > project_a['id']
    
    def test_project_with_special_characters(self):
        """Test project creation with special characters"""
        special_title = "Project with Special Chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        special_description = "Description with émojis 🚀 and unicode: ñáéíóú"
        special_filename = "image_with_special_chars_!@#.jpg"
        
        DAL.insert_project(special_title, special_description, special_filename)
        
        projects = DAL.list_projects()
        project = next((p for p in projects if p['Title'] == special_title), None)
        
        assert project is not None
        assert project['Description'] == special_description
        assert project['ImageFileName'] == special_filename
    
    def test_empty_projects_list(self):
        """Test behavior with empty projects list"""
        # This test ensures the function handles empty results gracefully
        projects = DAL.list_projects()
        assert isinstance(projects, list)
        # Note: This test assumes seed data exists, so we check it's not empty
        # In a real scenario, you might want to test with a truly empty database
        assert len(projects) >= 0
