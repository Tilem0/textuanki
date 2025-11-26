"""Deck model for TextuAnki."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from src.database.db import get_db


@dataclass
class Deck:
    """Represents a deck of flashcards."""
    id: Optional[int]
    name: str
    description: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def create(cls, name: str, description: str = "") -> "Deck":
        """Create a new deck in the database."""
        db = get_db()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO decks (name, description) VALUES (?, ?)",
                (name, description)
            )
            conn.commit()
            deck_id = cursor.lastrowid
        
        return cls.get_by_id(deck_id)
    
    @classmethod
    def get_by_id(cls, deck_id: int) -> Optional["Deck"]:
        """Retrieve a deck by ID."""
        db = get_db()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM decks WHERE id = ?", (deck_id,))
            row = cursor.fetchone()
            
            if row:
                return cls(
                    id=row["id"],
                    name=row["name"],
                    description=row["description"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    updated_at=datetime.fromisoformat(row["updated_at"])
                )
        return None
    
    @classmethod
    def get_all(cls) -> List["Deck"]:
        """Retrieve all decks."""
        db = get_db()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM decks ORDER BY name")
            rows = cursor.fetchall()
            
            return [
                cls(
                    id=row["id"],
                    name=row["name"],
                    description=row["description"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    updated_at=datetime.fromisoformat(row["updated_at"])
                )
                for row in rows
            ]
    
    def update(self) -> None:
        """Update the deck in the database."""
        db = get_db()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE decks 
                   SET name = ?, description = ?, updated_at = CURRENT_TIMESTAMP
                   WHERE id = ?""",
                (self.name, self.description, self.id)
            )
            conn.commit()
    
    def delete(self) -> None:
        """Delete the deck from the database."""
        db = get_db()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM decks WHERE id = ?", (self.id,))
            conn.commit()
    
    def get_card_count(self) -> int:
        """Get the number of cards in this deck."""
        db = get_db()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM cards WHERE deck_id = ?", (self.id,))
            return cursor.fetchone()[0]
