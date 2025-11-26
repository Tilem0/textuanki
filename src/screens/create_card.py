"""Create card screen for TextuAnki - Colorful Design."""
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Static, Input, TextArea, Button, Select, Label
from textual.binding import Binding
from typing import cast

from src.models.deck import Deck
from src.models.card import Card


class CreateCardScreen(Screen):
    """Screen for creating a new flashcard."""
    
    CSS = """
    CreateCardScreen {
        background: $background;
    }
    
    #create-card-container {
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
    
    #form-container {
        width: 80;
        height: auto;
        border: round $primary;
        padding: 2 3;
        background: $surface;
        margin: 1 auto;
    }
    
    Label {
        margin: 1 0 0 0;
        color: $text;
        background: $surface;
    }
    
    Input {
        margin: 0 0 1 0;
        border: round $secondary;
        background: $panel;
        color: $text;
    }
    
    Input:focus {
        border: round $accent;
        background: $surface;
    }
    
    TextArea {
        height: 7;
        margin: 0 0 1 0;
        border: round $secondary;
        background: $panel;
        color: $text;
    }
    
    TextArea:focus {
        border: round $accent;
        background: $surface;
    }
    
    Select {
        margin: 0 0 1 0;
        border: round $secondary;
        background: $panel;
        color: $text;
    }
    
    Select:focus {
        border: round $accent;
    }
    
    #button-container {
        height: auto;
        margin: 2 0;
        align: center middle;
        background: $surface;
    }
    
    Button {
        min-width: 18;
        height: 3;
        margin: 0 1;
        border: round $primary;
        background: $panel;
        color: $text;
    }
    
    Button:hover {
        background: $primary;
        color: $background;
    }
    
    #instructions {
        text-align: center;
        color: $text-muted;
        margin: 1 0;
        background: $background;
    }
    """
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("ctrl+s", "save", "Save Card"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the form."""
        with Container(id="create-card-container"):
            yield Static("➕ Create New Card", id="title")
            
            with Vertical(id="form-container"):
                yield Label("Deck:")
                
                # Get available decks
                decks = Deck.get_all()
                deck_options = [(deck.name, deck.id) for deck in decks]
                yield Select(deck_options, id="deck-select", prompt="Select a deck")
                
                yield Label("Front (Question):")
                yield TextArea(id="front-input")
                
                yield Label("Back (Answer):")
                yield TextArea(id="back-input")
                
                yield Label("Tags (optional, comma-separated):")
                yield Input(placeholder="e.g., vocabulary, chapter1", id="tags-input")
                
                with Horizontal(id="button-container"):
                    yield Button("💾 Save Card", id="save-btn")
                    yield Button("✗ Cancel", id="cancel-btn")
            
            yield Static(
                "Ctrl+S to save • ESC to cancel",
                id="instructions"
            )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "save-btn":
            self.action_save()
        elif event.button.id == "cancel-btn":
            self.action_cancel()
    
    def action_save(self) -> None:
        """Save the new card."""
        deck_select = self.query_one("#deck-select", Select)
        front_input = self.query_one("#front-input", TextArea)
        back_input = self.query_one("#back-input", TextArea)
        tags_input = self.query_one("#tags-input", Input)
        
        deck_id = deck_select.value
        front = front_input.text.strip()
        back = back_input.text.strip()
        tags = tags_input.value.strip()
        
        if not isinstance(deck_id, int):
            self.notify("Please select a deck", severity="error")
            return
        
        if not front or not back:
            self.notify("Front and back fields are required", severity="error")
            return
        
        # Create the card
        Card.create(deck_id=cast(int, deck_id), front=front, back=back, tags=tags)
        self.notify("Card created successfully!", severity="information")
        
        # Clear form
        front_input.clear()
        back_input.clear()
        tags_input.value = ""
        front_input.focus()
    
    def action_cancel(self) -> None:
        """Cancel and return to previous screen."""
        self.app.pop_screen()
