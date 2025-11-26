"""Review model and spaced repetition logic for TextuAnki."""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional
from src.database.db import get_db


@dataclass
class Review:
    """Represents review data for a card (SM-2 algorithm)."""
    id: Optional[int]
    card_id: int
    ease_factor: float = 2.5
    interval: int = 0
    repetitions: int = 0
    due_date: datetime = None
    last_review: Optional[datetime] = None
    
    def __post_init__(self):
        if self.due_date is None:
            self.due_date = datetime.now()
    
    @classmethod
    def get_by_card_id(cls, card_id: int) -> Optional["Review"]:
        """Retrieve review data for a card."""
        db = get_db()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reviews WHERE card_id = ?", (card_id,))
            row = cursor.fetchone()
            
            if row:
                return cls(
                    id=row["id"],
                    card_id=row["card_id"],
                    ease_factor=row["ease_factor"],
                    interval=row["interval"],
                    repetitions=row["repetitions"],
                    due_date=datetime.fromisoformat(row["due_date"]),
                    last_review=datetime.fromisoformat(row["last_review"]) if row["last_review"] else None
                )
        return None
    
    def record_review(self, rating: int) -> None:
        """
        Record a review and update spaced repetition data.
        
        Args:
            rating: Quality of recall (0-4)
                0 = Complete blackout
                1 = Incorrect, but familiar
                2 = Incorrect, but easy to recall
                3 = Correct, but difficult
                4 = Correct, with hesitation
                5 = Perfect recall
        """
        # SM-2 Algorithm
        if rating < 3:
            # Failed recall - reset
            self.repetitions = 0
            self.interval = 1
        else:
            if self.repetitions == 0:
                self.interval = 1
            elif self.repetitions == 1:
                self.interval = 6
            else:
                self.interval = int(self.interval * self.ease_factor)
            
            self.repetitions += 1
        
        # Update ease factor
        self.ease_factor = max(1.3, self.ease_factor + (0.1 - (5 - rating) * (0.08 + (5 - rating) * 0.02)))
        
        # Set new due date
        self.due_date = datetime.now() + timedelta(days=self.interval)
        self.last_review = datetime.now()
        
        # Save to database
        db = get_db()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Update review data
            cursor.execute(
                """UPDATE reviews 
                   SET ease_factor = ?, interval = ?, repetitions = ?,
                       due_date = ?, last_review = ?
                   WHERE card_id = ?""",
                (self.ease_factor, self.interval, self.repetitions,
                 self.due_date.isoformat(), self.last_review.isoformat(), self.card_id)
            )
            
            # Record study session
            cursor.execute(
                "INSERT INTO study_sessions (card_id, rating, reviewed_at) VALUES (?, ?, ?)",
                (self.card_id, rating, datetime.now().isoformat())
            )
            
            conn.commit()
