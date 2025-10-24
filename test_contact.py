"""
Test script for contact form functionality.
Tests contact form submission, validation, and data handling.
"""

import pytest
import os
import tempfile
import contact_DAL


class TestContactFormOperations:
    """Test contact form operations and business logic"""
    
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
    
    def test_contact_structure(self):
        """Test that contacts have expected structure"""
        # Insert a test contact first
        contact_DAL.insert_contact("John", "Doe", "john@example.com", "password123")
        contacts = contact_DAL.list_contacts()
        
        if contacts:  # Only test if there are contacts
            contact = contacts[0]
            required_fields = ['id', 'first_name', 'last_name', 'email', 'password', 'created_at']
            
            for field in required_fields:
                assert field in contact, f"Contact missing required field: {field}"
            
            # Check data types
            assert isinstance(contact['id'], int)
            assert isinstance(contact['first_name'], str)
            assert isinstance(contact['last_name'], str)
            assert isinstance(contact['email'], str)
            assert isinstance(contact['password'], str)
    
    def test_contact_ordering(self):
        """Test that contacts are ordered by created_at DESC"""
        # Insert multiple contacts
        contact_DAL.insert_contact("Alice", "Smith", "alice@example.com", "password1")
        contact_DAL.insert_contact("Bob", "Johnson", "bob@example.com", "password2")
        contact_DAL.insert_contact("Charlie", "Brown", "charlie@example.com", "password3")
        
        contacts = contact_DAL.list_contacts()
        
        if len(contacts) >= 2:
            # Check that contacts are ordered by created_at DESC (newest first)
            created_times = [contact['created_at'] for contact in contacts]
            assert created_times == sorted(created_times, reverse=True), "Contacts should be ordered by created_at DESC"
    
    def test_first_name_validation(self):
        """Test first name validation"""
        # Test with valid first name
        contact_DAL.insert_contact("ValidName", "Doe", "test@example.com", "password123")
        contacts = contact_DAL.list_contacts()
        assert any(c['first_name'] == "ValidName" for c in contacts)
        
        # Test with empty first name
        with pytest.raises(ValueError, match="All fields.*are required"):
            contact_DAL.insert_contact("", "Doe", "test@example.com", "password123")
        
        # Test with whitespace-only first name
        with pytest.raises(ValueError, match="All fields.*are required"):
            contact_DAL.insert_contact("   ", "Doe", "test@example.com", "password123")
        
        # Test with None first name
        with pytest.raises(ValueError, match="All fields.*are required"):
            contact_DAL.insert_contact(None, "Doe", "test@example.com", "password123")
    
    def test_last_name_validation(self):
        """Test last name validation"""
        # Test with valid last name
        contact_DAL.insert_contact("John", "ValidLastName", "test@example.com", "password123")
        contacts = contact_DAL.list_contacts()
        assert any(c['last_name'] == "ValidLastName" for c in contacts)
        
        # Test with empty last name
        with pytest.raises(ValueError, match="All fields.*are required"):
            contact_DAL.insert_contact("John", "", "test@example.com", "password123")
        
        # Test with whitespace-only last name
        with pytest.raises(ValueError, match="All fields.*are required"):
            contact_DAL.insert_contact("John", "   ", "test@example.com", "password123")
    
    def test_email_validation(self):
        """Test email validation"""
        # Test with valid email
        contact_DAL.insert_contact("John", "Doe", "valid@example.com", "password123")
        contacts = contact_DAL.list_contacts()
        assert any(c['email'] == "valid@example.com" for c in contacts)
        
        # Test with empty email
        with pytest.raises(ValueError, match="All fields.*are required"):
            contact_DAL.insert_contact("John", "Doe", "", "password123")
        
        # Test with whitespace-only email
        with pytest.raises(ValueError, match="All fields.*are required"):
            contact_DAL.insert_contact("John", "Doe", "   ", "password123")
        
        # Test with various email formats (these should all be accepted by the basic validation)
        email_formats = [
            "user@domain.com",
            "user.name@domain.com",
            "user+tag@domain.co.uk",
            "user123@subdomain.domain.org"
        ]
        
        for i, email in enumerate(email_formats):
            contact_DAL.insert_contact(f"User{i}", "Test", email, "password123")
            contacts = contact_DAL.list_contacts()
            assert any(c['email'] == email for c in contacts)
    
    def test_password_validation(self):
        """Test password validation"""
        # Test with valid password
        contact_DAL.insert_contact("John", "Doe", "test@example.com", "validpassword123")
        contacts = contact_DAL.list_contacts()
        assert any(c['password'] == "validpassword123" for c in contacts)
        
        # Test with empty password
        with pytest.raises(ValueError, match="All fields.*are required"):
            contact_DAL.insert_contact("John", "Doe", "test@example.com", "")
        
        # Test with whitespace-only password
        with pytest.raises(ValueError, match="All fields.*are required"):
            contact_DAL.insert_contact("John", "Doe", "test@example.com", "   ")
        
        # Test with various password formats
        password_formats = [
            "simplepassword",
            "password123",
            "Password123",
            "P@ssw0rd!",
            "verylongpasswordwithspecialchars!@#$%^&*()"
        ]
        
        for i, password in enumerate(password_formats):
            contact_DAL.insert_contact(f"User{i}", "Test", f"user{i}@example.com", password)
            contacts = contact_DAL.list_contacts()
            assert any(c['password'] == password for c in contacts)
    
    def test_contact_creation_timestamp(self):
        """Test that contacts get created with timestamp"""
        contact_DAL.insert_contact("Timestamp", "Test", "timestamp@example.com", "password123")
        contacts = contact_DAL.list_contacts()
        
        test_contact = next((c for c in contacts if c['email'] == "timestamp@example.com"), None)
        assert test_contact is not None
        assert test_contact['created_at'] is not None
        assert test_contact['created_at'] != ""
    
    def test_multiple_contact_insertion(self):
        """Test inserting multiple contacts"""
        initial_count = contact_DAL.get_contact_count()
        
        # Insert multiple contacts
        test_contacts = [
            ("Alice", "Smith", "alice@example.com", "password1"),
            ("Bob", "Johnson", "bob@example.com", "password2"),
            ("Charlie", "Brown", "charlie@example.com", "password3"),
        ]
        
        for first_name, last_name, email, password in test_contacts:
            contact_DAL.insert_contact(first_name, last_name, email, password)
        
        assert contact_DAL.get_contact_count() == initial_count + len(test_contacts)
        
        # Verify all contacts were inserted
        contacts = contact_DAL.list_contacts()
        for first_name, last_name, email, password in test_contacts:
            contact = next((c for c in contacts if c['email'] == email), None)
            assert contact is not None
            assert contact['first_name'] == first_name
            assert contact['last_name'] == last_name
            assert contact['password'] == password
    
    def test_contact_id_auto_increment(self):
        """Test that contact IDs auto-increment correctly"""
        initial_count = contact_DAL.get_contact_count()
        
        # Insert two contacts
        contact_DAL.insert_contact("Alice", "Smith", "alice@example.com", "password1")
        contact_DAL.insert_contact("Bob", "Johnson", "bob@example.com", "password2")
        
        contacts = contact_DAL.list_contacts()
        alice_contact = next((c for c in contacts if c['email'] == "alice@example.com"), None)
        bob_contact = next((c for c in contacts if c['email'] == "bob@example.com"), None)
        
        assert alice_contact is not None
        assert bob_contact is not None
        assert bob_contact['id'] > alice_contact['id']
    
    def test_contact_with_special_characters(self):
        """Test contact creation with special characters"""
        special_first_name = "José"
        special_last_name = "O'Connor-Smith"
        special_email = "josé.o'connor-smith@example.com"
        special_password = "P@ssw0rd!@#$%^&*()"
        
        contact_DAL.insert_contact(special_first_name, special_last_name, special_email, special_password)
        
        contacts = contact_DAL.list_contacts()
        contact = next((c for c in contacts if c['email'] == special_email), None)
        
        assert contact is not None
        assert contact['first_name'] == special_first_name
        assert contact['last_name'] == special_last_name
        assert contact['password'] == special_password
    
    def test_get_contact_count_accuracy(self):
        """Test that get_contact_count returns accurate count"""
        initial_count = contact_DAL.get_contact_count()
        
        # Insert 5 contacts
        for i in range(5):
            contact_DAL.insert_contact(f"User{i}", "Test", f"user{i}@example.com", f"password{i}")
        
        assert contact_DAL.get_contact_count() == initial_count + 5
        
        # Verify by checking list length
        contacts = contact_DAL.list_contacts()
        assert len(contacts) == contact_DAL.get_contact_count()
    
    def test_empty_contacts_list(self):
        """Test behavior with empty contacts list"""
        # This test ensures the function handles empty results gracefully
        contacts = contact_DAL.list_contacts()
        assert isinstance(contacts, list)
        assert len(contacts) >= 0
        
        count = contact_DAL.get_contact_count()
        assert isinstance(count, int)
        assert count >= 0
