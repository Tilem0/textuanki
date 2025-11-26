"""Create card screen for TextuAnki."""
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Static, Input, TextArea, Button, Select, Label
from textual.binding import Binding
from typing import cast

from src.models.deck import Deck
from src.models.card import Card
from src.banners import CREATE_BANNER, to_smallcaps


class CreateCardScreen(Screen):
    """Screen for creating a new flashcard."""
    
    CSS = """
    CreateCardScreen {
        background: #000000;
    }
    
    #create-card-container {
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
    
    #form-container {
        width: 100%;
        height: auto;
        border: heavy #FFFFFF;
        padding: 2 3;
        background: #000000;
        margin: 1 0;
    }
    
    Label {
        margin: 1 0 0 0;
        color: #FFFFFF;
        background: #000000;
    }
    
    Input {
        margin: 0 0 1 0;
        border: heavy #FFFFFF;
        background: #000000;
        color: #FFFFFF;
    }
    
    Input:focus {
        border: heavy #FFFFFF;
        background: #000000;
    }
    
    TextArea {
        height: 6;
        margin: 0 0 1 0;
        border: heavy #FFFFFF;
        background: #000000;
        color: #FFFFFF;
    }
    
    TextArea:focus {
        border: heavy #FFFFFF;
        background: #000000;
    }
    
    Select {
        margin: 0 0 1 0;
        border: heavy #FFFFFF;
        background: #000000;
        color: #FFFFFF;
    }
    
    Select:focus {
        border: heavy #FFFFFF;
    }
    
    #divider {
        color: #FFFFFF;
        text-align: center;
        margin: 1 0;
        background: #000000;
    }
    
    #button-container {
        height: auto;
        margin: 1 0;
        align: center middle;
        background: #000000;
    }
    
    Button {
        min-width: 18;
        height: 3;
        margin: 0 1;
        border: heavy #FFFFFF;
        background: #000000;
        color: #FFFFFF;
    }
    
    Button:hover {
        background: #FFFFFF;
        color: #000000;
    }
    
    #instructions {
        text-align: center;
        color: #666666;
        margin: 1 0;
        background: #000000;
    }
    """
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("ctrl+s", "save", "Save Card"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the form."""
        with Container(id="create-card-container"):
            yield Static(CREATE_BANNER, id="banner")
            
            with Vertical(id="form-container"):
                yield Label("【 " + to_smallcaps("deck") + " 】")
                
                # Get available decks
                decks = Deck.get_all()
                deck_options = [(deck.name, deck.id) for deck in decks]
                yield Select(deck_options, id="deck-select", prompt="Select a deck")
                
                yield Label("【 " + to_smallcaps("front (question)") + " 】")
                yield TextArea(id="front-input")
                
                yield Label("【 " + to_smallcaps("back (answer)") + " 】")
                yield TextArea(id="back-input")
                
                yield Label("【 " + to_smallcaps("tags (optional)") + " 】")
                yield Input(placeholder="e.g., vocabulary, chapter1", id="tags-input")
                
                yield Static("━" * 80, id="divider")
                
                with Horizontal(id="button-container"):
                    yield Button("✓ SAVE CARD", id="save-btn")
                    yield Button("✗ CANCEL", id="cancel-btn")
            
            yield Static(
                to_smallcaps("ctrl+s to save | esc to cancel"),
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
