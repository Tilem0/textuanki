"""Database management for TextuAnki."""
import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager


class Database:
    """SQLite database manager for TextuAnki."""
    
    def __init__(self, db_path: Optional[Path] = None):
        """Initialize database connection.
        
        Args:
            db_path: Path to database file. Defaults to ~/.textuanki/cards.db
        """
        if db_path is None:
            db_path = Path.home() / ".textuanki" / "cards.db"
        
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def init_db(self):
        """Initialize database schema."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create decks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS decks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create cards table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    deck_id INTEGER NOT NULL,
                    front TEXT NOT NULL,
                    back TEXT NOT NULL,
                    tags TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (deck_id) REFERENCES decks (id) ON DELETE CASCADE
                )
            """)
            
            # Create reviews table for spaced repetition
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    card_id INTEGER NOT NULL,
                    ease_factor REAL DEFAULT 2.5,
                    interval INTEGER DEFAULT 0,
                    repetitions INTEGER DEFAULT 0,
                    due_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_review TIMESTAMP,
                    FOREIGN KEY (card_id) REFERENCES cards (id) ON DELETE CASCADE
                )
            """)
            
            # Create study_sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS study_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    card_id INTEGER NOT NULL,
                    rating INTEGER NOT NULL,
                    duration INTEGER,
                    reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (card_id) REFERENCES cards (id) ON DELETE CASCADE
                )
            """)
            
            # Create default deck if none exists
            cursor.execute("SELECT COUNT(*) FROM decks")
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO decks (name, description) VALUES (?, ?)",
                    ("Default", "Default deck for new cards")
                )
            
            conn.commit()


# Global database instance
_db_instance: Optional[Database] = None


def get_db() -> Database:
    """Get or create the global database instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance
