"""Card model for TextuAnki."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from src.database.db import get_db


@dataclass
class Card:
    """Represents a flashcard."""
    id: Optional[int]
    deck_id: int
    front: str
    back: str
    tags: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def create(cls, deck_id: int, front: str, back: str, tags: str = "") -> "Card":
        """Create a new card in the database."""
        db = get_db()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO cards (deck_id, front, back, tags) VALUES (?, ?, ?, ?)",
                (deck_id, front, back, tags)
            )
            card_id = cursor.lastrowid
            
            # Create initial review record
            cursor.execute(
                "INSERT INTO reviews (card_id) VALUES (?)",
                (card_id,)
            )
            conn.commit()
        
        return cls.get_by_id(card_id)
    
    @classmethod
    def get_by_id(cls, card_id: int) -> Optional["Card"]:
        """Retrieve a card by ID."""
        db = get_db()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cards WHERE id = ?", (card_id,))
            row = cursor.fetchone()
            
            if row:
                return cls(
                    id=row["id"],
                    deck_id=row["deck_id"],
                    front=row["front"],
                    back=row["back"],
                    tags=row["tags"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    updated_at=datetime.fromisoformat(row["updated_at"])
                )
        return None
    
    @classmethod
    def get_by_deck(cls, deck_id: int) -> List["Card"]:
        """Retrieve all cards in a deck."""
        db = get_db()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM cards WHERE deck_id = ? ORDER BY created_at DESC",
                (deck_id,)
            )
            rows = cursor.fetchall()
            
            return [
                cls(
                    id=row["id"],
                    deck_id=row["deck_id"],
                    front=row["front"],
                    back=row["back"],
                    tags=row["tags"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    updated_at=datetime.fromisoformat(row["updated_at"])
                )
                for row in rows
            ]
    
    @classmethod
    def get_due_cards(cls, deck_id: Optional[int] = None) -> List["Card"]:
        """Get cards that are due for review."""
        db = get_db()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            if deck_id:
                cursor.execute("""
                    SELECT c.* FROM cards c
                    JOIN reviews r ON c.id = r.card_id
                    WHERE c.deck_id = ? AND r.due_date <= CURRENT_TIMESTAMP
                    ORDER BY r.due_date
                """, (deck_id,))
            else:
                cursor.execute("""
                    SELECT c.* FROM cards c
                    JOIN reviews r ON c.id = r.card_id
                    WHERE r.due_date <= CURRENT_TIMESTAMP
                    ORDER BY r.due_date
                """)
            
            rows = cursor.fetchall()
            
            return [
                cls(
                    id=row["id"],
                    deck_id=row["deck_id"],
                    front=row["front"],
                    back=row["back"],
                    tags=row["tags"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    updated_at=datetime.fromisoformat(row["updated_at"])
                )
                for row in rows
            ]
    
    def update(self) -> None:
        """Update the card in the database."""
        db = get_db()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE cards 
                   SET deck_id = ?, front = ?, back = ?, tags = ?, 
                       updated_at = CURRENT_TIMESTAMP
                   WHERE id = ?""",
                (self.deck_id, self.front, self.back, self.tags, self.id)
            )
            conn.commit()
    
    def delete(self) -> None:
        """Delete the card from the database."""
        db = get_db()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cards WHERE id = ?", (self.id,))
            conn.commit()
