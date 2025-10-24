"""
Test script for Flask application routes and behavior.
Tests all Flask routes, form submissions, and application functionality.
"""

import pytest
import os
import tempfile
from flask import Flask
import DAL
import contact_DAL

# Import the app after setting up test databases
from app import app


class TestFlaskApp:
    """Test Flask application routes and behavior"""
    
    def setup_method(self):
        """Set up test databases before each test"""
        # Use temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Set up test databases
        original_projects_filename = DAL.DB_FILENAME
        original_contacts_filename = contact_DAL.DB_FILENAME
        
        DAL.DB_FILENAME = os.path.join(self.temp_dir.name, "test_projects.db")
        contact_DAL.DB_FILENAME = os.path.join(self.temp_dir.name, "test_contacts.db")
        
        # Initialize test databases
        DAL.init_db()
        contact_DAL.init_contact_db()
        
        # Configure Flask app for testing
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.client = app.test_client()
    
    def teardown_method(self):
        """Clean up after each test"""
        self.temp_dir.cleanup()
    
    def test_home_route(self):
        """Test home page route"""
        response = self.client.get('/')
        assert response.status_code == 200
        assert b'active_page' in response.data or b'home' in response.data
    
    def test_about_route(self):
        """Test about page route"""
        response = self.client.get('/about')
        assert response.status_code == 200
        assert b'active_page' in response.data or b'about' in response.data
    
    def test_resume_route(self):
        """Test resume page route"""
        response = self.client.get('/resume')
        assert response.status_code == 200
        assert b'active_page' in response.data or b'resume' in response.data
    
    def test_projects_route_get(self):
        """Test projects page GET request"""
        response = self.client.get('/projects')
        assert response.status_code == 200
        assert b'active_page' in response.data or b'projects' in response.data
        
        # Check that projects data is passed to template
        # This assumes the template renders project titles
        projects = DAL.list_projects()
        if projects:
            assert projects[0]['Title'].encode() in response.data
    
    def test_projects_new_route_get(self):
        """Test new project form GET request"""
        response = self.client.get('/projects/new')
        assert response.status_code == 200
        assert b'active_page' in response.data or b'projects' in response.data
    
    def test_projects_new_route_post_success(self):
        """Test new project form POST request with valid data"""
        data = {
            'title': 'Test Project',
            'description': 'Test Description',
            'image_file_name': 'test.jpg'
        }
        
        response = self.client.post('/projects/new', data=data, follow_redirects=True)
        assert response.status_code == 200
        
        # Check that project was added to database
        projects = DAL.list_projects()
        assert any(p['Title'] == 'Test Project' for p in projects)
    
    def test_projects_new_route_post_missing_title(self):
        """Test new project form POST with missing title"""
        data = {
            'title': '',
            'description': 'Test Description',
            'image_file_name': 'test.jpg'
        }
        
        response = self.client.post('/projects/new', data=data, follow_redirects=True)
        assert response.status_code == 200
        
        # Should redirect back to form (not add project)
        projects = DAL.list_projects()
        assert not any(p['Title'] == '' for p in projects)
    
    def test_projects_new_route_post_missing_description(self):
        """Test new project form POST with missing description"""
        data = {
            'title': 'Test Project',
            'description': '',
            'image_file_name': 'test.jpg'
        }
        
        response = self.client.post('/projects/new', data=data, follow_redirects=True)
        assert response.status_code == 200
        
        # Should redirect back to form (not add project)
        projects = DAL.list_projects()
        assert not any(p['Description'] == '' for p in projects)
    
    def test_projects_new_route_post_missing_image(self):
        """Test new project form POST with missing image filename"""
        data = {
            'title': 'Test Project',
            'description': 'Test Description',
            'image_file_name': ''
        }
        
        response = self.client.post('/projects/new', data=data, follow_redirects=True)
        assert response.status_code == 200
        
        # Should redirect back to form (not add project)
        projects = DAL.list_projects()
        assert not any(p['ImageFileName'] == '' for p in projects)
    
    def test_contact_route_get(self):
        """Test contact page GET request"""
        response = self.client.get('/contact')
        assert response.status_code == 200
        assert b'active_page' in response.data or b'contact' in response.data
    
    def test_contact_route_post_success(self):
        """Test contact form POST with valid data"""
        data = {
            'first-name': 'John',
            'last-name': 'Doe',
            'email': 'john@example.com',
            'password': 'password123',
            'confirm-password': 'password123'
        }
        
        response = self.client.post('/contact', data=data, follow_redirects=True)
        assert response.status_code == 200
        
        # Check that contact was added to database
        contacts = contact_DAL.list_contacts()
        assert any(c['email'] == 'john@example.com' for c in contacts)
    
    def test_contact_route_post_missing_fields(self):
        """Test contact form POST with missing fields"""
        data = {
            'first-name': 'John',
            'last-name': '',
            'email': 'john@example.com',
            'password': 'password123',
            'confirm-password': 'password123'
        }
        
        response = self.client.post('/contact', data=data, follow_redirects=True)
        assert response.status_code == 200
        
        # Should redirect back to form (not add contact)
        contacts = contact_DAL.list_contacts()
        assert not any(c['first_name'] == 'John' and c['last_name'] == '' for c in contacts)
    
    def test_contact_route_post_password_mismatch(self):
        """Test contact form POST with password mismatch"""
        data = {
            'first-name': 'John',
            'last-name': 'Doe',
            'email': 'john@example.com',
            'password': 'password123',
            'confirm-password': 'differentpassword'
        }
        
        response = self.client.post('/contact', data=data, follow_redirects=True)
        assert response.status_code == 200
        
        # Should redirect back to form (not add contact)
        contacts = contact_DAL.list_contacts()
        assert not any(c['email'] == 'john@example.com' for c in contacts)
    
    def test_contact_route_post_short_password(self):
        """Test contact form POST with short password"""
        data = {
            'first-name': 'John',
            'last-name': 'Doe',
            'email': 'john@example.com',
            'password': '123',
            'confirm-password': '123'
        }
        
        response = self.client.post('/contact', data=data, follow_redirects=True)
        assert response.status_code == 200
        
        # Should redirect back to form (not add contact)
        contacts = contact_DAL.list_contacts()
        assert not any(c['email'] == 'john@example.com' for c in contacts)
    
    def test_contact_route_post_valid_password(self):
        """Test contact form POST with valid password length"""
        data = {
            'first-name': 'John',
            'last-name': 'Doe',
            'email': 'john@example.com',
            'password': 'password123',
            'confirm-password': 'password123'
        }
        
        response = self.client.post('/contact', data=data, follow_redirects=True)
        assert response.status_code == 200
        
        # Should add contact to database
        contacts = contact_DAL.list_contacts()
        assert any(c['email'] == 'john@example.com' for c in contacts)
    
    def test_thank_you_route(self):
        """Test thank you page route"""
        response = self.client.get('/thank-you')
        assert response.status_code == 200
        assert b'active_page' in response.data or b'contact' in response.data
    
    def test_nonexistent_route(self):
        """Test accessing a non-existent route"""
        response = self.client.get('/nonexistent')
        assert response.status_code == 404
    
    def test_app_secret_key(self):
        """Test that app has secret key configured"""
        assert app.secret_key is not None
        assert app.secret_key != ''
    
    def test_app_configuration(self):
        """Test app configuration"""
        assert app.config['TESTING'] is True
    
    def test_flash_messages_in_projects(self):
        """Test that flash messages work in project creation"""
        # Test successful project creation flash message
        data = {
            'title': 'Flash Test Project',
            'description': 'Test Description',
            'image_file_name': 'test.jpg'
        }
        
        response = self.client.post('/projects/new', data=data, follow_redirects=True)
        assert response.status_code == 200
        
        # Check for success message in response
        assert b'success' in response.data.lower() or b'added successfully' in response.data.lower()
    
    def test_flash_messages_in_contact(self):
        """Test that flash messages work in contact form"""
        # Test successful contact submission flash message
        data = {
            'first-name': 'Flash',
            'last-name': 'Test',
            'email': 'flash@example.com',
            'password': 'password123',
            'confirm-password': 'password123'
        }
        
        response = self.client.post('/contact', data=data, follow_redirects=True)
        assert response.status_code == 200
        
        # Check for success message in response
        assert b'success' in response.data.lower() or b'thank you' in response.data.lower()
    
    def test_multiple_project_submissions(self):
        """Test multiple project submissions"""
        projects_data = [
            {'title': 'Project 1', 'description': 'Description 1', 'image_file_name': 'img1.jpg'},
            {'title': 'Project 2', 'description': 'Description 2', 'image_file_name': 'img2.jpg'},
            {'title': 'Project 3', 'description': 'Description 3', 'image_file_name': 'img3.jpg'},
        ]
        
        for data in projects_data:
            response = self.client.post('/projects/new', data=data, follow_redirects=True)
            assert response.status_code == 200
        
        # Check that all projects were added
        projects = DAL.list_projects()
        for data in projects_data:
            assert any(p['Title'] == data['title'] for p in projects)
    
    def test_multiple_contact_submissions(self):
        """Test multiple contact submissions"""
        contacts_data = [
            {'first-name': 'Alice', 'last-name': 'Smith', 'email': 'alice@example.com', 'password': 'pass1', 'confirm-password': 'pass1'},
            {'first-name': 'Bob', 'last-name': 'Johnson', 'email': 'bob@example.com', 'password': 'pass2', 'confirm-password': 'pass2'},
            {'first-name': 'Charlie', 'last-name': 'Brown', 'email': 'charlie@example.com', 'password': 'pass3', 'confirm-password': 'pass3'},
        ]
        
        for data in contacts_data:
            response = self.client.post('/contact', data=data, follow_redirects=True)
            assert response.status_code == 200
        
        # Check that all contacts were added
        contacts = contact_DAL.list_contacts()
        for data in contacts_data:
            assert any(c['email'] == data['email'] for c in contacts)
