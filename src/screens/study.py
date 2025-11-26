"""Study screen for TextuAnki - Colorful Design."""
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Static, Button, Label
from textual.binding import Binding

from src.models.card import Card
from src.models.review import Review


class StudyScreen(Screen):
    """Screen for studying flashcards."""
    
    CSS = """
    StudyScreen {
        background: $background;
    }
    
    #study-container {
        width: 100%;
        height: 100%;
        padding: 2 4;
        background: $background;
    }
    
    #title {
        text-align: center;
        text-style: bold;
        color: $primary;
        margin: 1 0 2 0;
    }
    
    #progress {
        text-align: center;
        color: $text-muted;
        margin: 1 0;
        background: $background;
    }
    
    #card-container {
        width: 100%;
        height: auto;
        border: round $primary;
        background: $surface;
        padding: 3 4;
        margin: 2 0;
    }
    
    #card-content {
        min-height: 15;
        text-align: center;
        content-align: center middle;
        color: $text;
        background: $surface;
    }
    
    #rating-buttons {
        height: auto;
        margin: 2 0;
        align: center middle;
        background: $background;
    }
    
    .rating-btn {
        min-width: 16;
        height: 3;
        margin: 0 1;
        border: round $primary;
        background: $surface;
        color: $text;
    }
    
    .rating-btn:hover {
        background: $primary;
        color: $background;
    }
    
    .rating-btn:disabled {
        border: round $panel;
        color: $text-muted;
        background: $panel;
    }
    
    .rating-again {
        border: round $error;
    }
    
    .rating-again:hover {
        background: $error;
    }
    
    .rating-hard {
        border: round $warning;
    }
    
    .rating-hard:hover {
        background: $warning;
    }
    
    .rating-good {
        border: round $success;
    }
    
    .rating-good:hover {
        background: $success;
    }
    
    .rating-easy {
        border: round $accent;
    }
    
    .rating-easy:hover {
        background: $accent;
    }
    
    #instructions {
        text-align: center;
        color: $text-muted;
        margin: 1 0;
        background: $background;
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
            yield Static("📝 Study Session", id="title")
            yield Static("", id="progress")
            
            with Vertical(id="card-container"):
                yield Static("", id="card-content")
            
            with Horizontal(id="rating-buttons"):
                yield Button("Again [1]", classes="rating-btn rating-again", id="again-btn")
                yield Button("Hard [2]", classes="rating-btn rating-hard", id="hard-btn")
                yield Button("Good [3]", classes="rating-btn rating-good", id="good-btn")
                yield Button("Easy [4]", classes="rating-btn rating-easy", id="easy-btn")
            
            yield Static(
                "Press SPACE to reveal • 1-4 to rate • ESC to exit",
                id="instructions"
            )
    
    def refresh_display(self) -> None:
        """Refresh the card display."""
        content_widget = self.query_one("#card-content", Static)
        progress_widget = self.query_one("#progress", Static)
        
        if not self.cards:
            content_widget.update("🎉 No cards due! Great work!")
            progress_widget.update("")
            self.query_one("#rating-buttons").display = False
            return
        
        self.query_one("#rating-buttons").display = True
        card = self.cards[self.current_index]
        
        # Update progress
        progress_widget.update(f"Card {self.current_index + 1} of {len(self.cards)}")
        
        # Update content
        if self.show_answer:
            content_widget.update(
                f"[bold cyan]Question:[/bold cyan]\n\n{card.front}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"[bold green]Answer:[/bold green]\n\n{card.back}"
            )
            # Show rating buttons
            for btn in self.query(Button):
                btn.disabled = False
        else:
            content_widget.update(f"[bold cyan]Question:[/bold cyan]\n\n{card.front}")
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
