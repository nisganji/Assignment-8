import sqlite3
import os


DB_FILENAME = os.path.join(os.path.dirname(__file__), "projects.db")


def get_connection():
    return sqlite3.connect(DB_FILENAME)


def init_db():
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT NOT NULL,
                Description TEXT NOT NULL,
                ImageFileName TEXT NOT NULL,
                CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()

        cursor = conn.execute("SELECT COUNT(*) FROM projects")
        count = cursor.fetchone()[0]
        if count == 0:
            seed_projects = [
                (
                    "Sign Language Recognition using Deep Learning",
                    "Real-time translator using Python, OpenCV, Mediapipe, TensorFlow, scikit-learn, CNN; achieved 99% accuracy; Springer published.",
                    "sign.webp",
                ),
                (
                    "Decentro Vault: Decentralized Banking System",
                    "Decentralized banking with MetaMask wallet integration and secure transaction protocols for crypto management.",
                    "block.webp",
                ),
            ]
            conn.executemany(
                "INSERT INTO projects (Title, Description, ImageFileName) VALUES (?, ?, ?)",
                seed_projects,
            )
            conn.commit()


def list_projects():
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, Title, Description, ImageFileName, CreatedAt FROM projects ORDER BY id ASC"
        ).fetchall()
        return [dict(row) for row in rows]


def insert_project(title, description, image_file_name):
    # Normalize and validate inputs to prevent whitespace-only values
    title = (title or "").strip()
    description = (description or "").strip()
    image_file_name = (image_file_name or "").strip()
    if not title or not description or not image_file_name:
        raise ValueError("All fields (title, description, image_file_name) are required")
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO projects (Title, Description, ImageFileName) VALUES (?, ?, ?)",
            (title, description, image_file_name),
        )
        conn.commit()



