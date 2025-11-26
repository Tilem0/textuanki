"""Study screen for TextuAnki."""
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Static, Button, Label
from textual.binding import Binding

from src.models.card import Card
from src.models.review import Review
from src.banners import STUDY_BANNER, to_smallcaps


class StudyScreen(Screen):
    """Screen for studying flashcards."""
    
    CSS = """
    StudyScreen {
        background: #000000;
    }
    
    #study-container {
        width: 100%;
        height: 100%;
        padding: 1 2;
        background: #000000;
    }
    
    #banner {
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 1;
        background: #000000;
    }
    
    #progress {
        text-align: center;
        color: #999999;
        margin: 1 0;
        background: #000000;
    }
    
    #card-container {
        width: 100%;
        height: auto;
        border: heavy #FFFFFF;
        background: #000000;
        padding: 2 4;
        margin: 1 0;
    }
    
    #card-content {
        min-height: 12;
        text-align: center;
        content-align: center middle;
        color: #FFFFFF;
        background: #000000;
    }
    
    #divider {
        color: #FFFFFF;
        text-align: center;
        margin: 1 0;
        background: #000000;
    }
    
    #rating-buttons {
        height: auto;
        margin: 1 0;
        align: center middle;
        background: #000000;
    }
    
    .rating-btn {
        min-width: 15;
        height: 3;
        margin: 0 1;
        border: heavy #FFFFFF;
        background: #000000;
        color: #FFFFFF;
    }
    
    .rating-btn:hover {
        background: #FFFFFF;
        color: #000000;
    }
    
    .rating-btn:disabled {
        border: heavy #333333;
        color: #333333;
        background: #000000;
    }
    
    #instructions {
        text-align: center;
        color: #666666;
        margin: 1 0;
        background: #000000;
    }
    """
    
    BINDINGS = [
        Binding("escape", "back", "Back to Dashboard"),
        Binding("space", "reveal", "Reveal Answer"),
        Binding("1", "rate_again", "Again"),
        Binding("2", "rate_hard", "Hard"),
        Binding("3", "rate_good", "Good"),
        Binding("4", "rate_easy", "Easy"),
    ]
    
    def __init__(self):
        super().__init__()
        self.cards = []
        self.current_index = 0
        self.show_answer = False
    
    def on_mount(self) -> None:
        """Load cards when screen mounts."""
        self.cards = Card.get_due_cards()
        self.current_index = 0
        self.show_answer = False
        self.refresh_display()
    
    def compose(self) -> ComposeResult:
        """Create child widgets for study mode."""
        with Container(id="study-container"):
            yield Static(STUDY_BANNER, id="banner")
            yield Static("", id="progress")
            
            with Vertical(id="card-container"):
                yield Static("", id="card-content")
            
            yield Static("━" * 80, id="divider")
            
            with Horizontal(id="rating-buttons"):
                yield Button("✗ AGAIN [1]", classes="rating-btn", id="again-btn")
                yield Button("△ HARD [2]", classes="rating-btn", id="hard-btn")
                yield Button("◯ GOOD [3]", classes="rating-btn", id="good-btn")
                yield Button("◎ EASY [4]", classes="rating-btn", id="easy-btn")
            
            yield Static(
                to_smallcaps("press space to reveal | use 1-4 to rate | esc to exit"),
                id="instructions"
            )
    
    def refresh_display(self) -> None:
        """Refresh the card display."""
        content_widget = self.query_one("#card-content", Static)
        progress_widget = self.query_one("#progress", Static)
        
        if not self.cards:
            content_widget.update("╔═══════════════════════════════╗\n║  NO CARDS DUE - GREAT WORK!   ║\n╚═══════════════════════════════╝")
            progress_widget.update("")
            self.query_one("#rating-buttons").display = False
            return
        
        self.query_one("#rating-buttons").display = True
        card = self.cards[self.current_index]
        
        # Update progress
        progress_text = to_smallcaps(f"card {self.current_index + 1} of {len(self.cards)}")
        progress_widget.update(f"【 {progress_text} 】")
        
        # Update content
        if self.show_answer:
            content_widget.update(
                f"[bold]【 QUESTION 】[/bold]\n\n{card.front}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"[bold]【 ANSWER 】[/bold]\n\n{card.back}"
            )
            # Show rating buttons
            for btn in self.query(Button):
                btn.disabled = False
        else:
            content_widget.update(f"[bold]【 QUESTION 】[/bold]\n\n{card.front}")
            # Hide rating buttons
            for btn in self.query(Button):
                btn.disabled = True
    
    def action_reveal(self) -> None:
        """Reveal the answer."""
        if self.cards and not self.show_answer:
            self.show_answer = True
            self.refresh_display()
    
    def rate_card(self, rating: int) -> None:
        """Rate the current card and move to next."""
        if not self.cards or not self.show_answer:
            return
        
        card = self.cards[self.current_index]
        if card.id is not None:
            review = Review.get_by_card_id(card.id)
            
            if review:
                review.record_review(rating)
        
        # Move to next card
        self.cards.pop(self.current_index)
        
        if self.current_index >= len(self.cards) and self.cards:
            self.current_index = len(self.cards) - 1
        
        self.show_answer = False
        self.refresh_display()
    
    def action_rate_again(self) -> None:
        """Rate card as 'Again' (difficulty 0)."""
        self.rate_card(0)
    
    def action_rate_hard(self) -> None:
        """Rate card as 'Hard' (difficulty 2)."""
        self.rate_card(2)
    
    def action_rate_good(self) -> None:
        """Rate card as 'Good' (difficulty 3)."""
        self.rate_card(3)
    
    def action_rate_easy(self) -> None:
        """Rate card as 'Easy' (difficulty 4)."""
        self.rate_card(4)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.disabled:
            return
        
        button_id = event.button.id
        if button_id == "again-btn":
            self.action_rate_again()
        elif button_id == "hard-btn":
            self.action_rate_hard()
        elif button_id == "good-btn":
            self.action_rate_good()
        elif button_id == "easy-btn":
            self.action_rate_easy()
    
    def action_back(self) -> None:
        """Return to dashboard."""
        self.app.pop_screen()
