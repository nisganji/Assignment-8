import sqlite3
import os


DB_FILENAME = "contacts.db"


def get_connection():
    return sqlite3.connect(DB_FILENAME)


def init_contact_db():
    """Initialize the contact form database with contacts table"""
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def insert_contact(first_name, last_name, email, password):
    """Insert a new contact form submission into the database"""
    if not all([first_name, last_name, email, password]):
        raise ValueError("All fields (first_name, last_name, email, password) are required")
    
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO contacts (first_name, last_name, email, password) VALUES (?, ?, ?, ?)",
            (first_name, last_name, email, password),
        )
        conn.commit()


def list_contacts():
    """Retrieve all contact form submissions"""
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, first_name, last_name, email, password, created_at FROM contacts ORDER BY created_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def get_contact_count():
    """Get the total number of contact form submissions"""
    with get_connection() as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM contacts")
        return cursor.fetchone()[0]
