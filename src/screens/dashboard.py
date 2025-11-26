"""Dashboard screen for TextuAnki."""
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Static, Button, Label
from textual.binding import Binding

from src.models.deck import Deck
from src.models.card import Card


class StatsCard(Static):
    """A card displaying a statistic."""
    
    DEFAULT_CSS = """
    StatsCard {
        width: 1fr;
        height: 7;
        border: solid $primary;
        background: $panel;
        padding: 1 2;
        margin: 0 1;
    }
    
    StatsCard .stat-value {
        text-align: center;
        text-style: bold;
        color: $accent;
        content-align: center middle;
    }
    
    StatsCard .stat-label {
        text-align: center;
        color: $text-muted;
        content-align: center middle;
    }
    """
    
    def __init__(self, label: str, value: str, **kwargs):
        super().__init__(**kwargs)
        self.label_text = label
        self.value_text = value
    
    def compose(self) -> ComposeResult:
        yield Label(self.value_text, classes="stat-value")
        yield Label(self.label_text, classes="stat-label")


class MenuButton(Button):
    """A styled menu button."""
    
    DEFAULT_CSS = """
    MenuButton {
        width: 100%;
        height: 3;
        margin: 1 0;
        border: solid $primary;
    }
    
    MenuButton:hover {
        background: $primary;
    }
    
    MenuButton:focus {
        background: $accent;
    }
    """


class DashboardScreen(Screen):
    """Main dashboard screen."""
    
    CSS = """
    #dashboard-container {
        width: 100%;
        height: 100%;
        padding: 2 4;
    }
    
    #welcome {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin: 1 0 2 0;
        width: 100%;
    }
    
    #stats-container {
        height: auto;
        width: 100%;
        margin: 2 0;
    }
    
    #menu-container {
        width: 60;
        height: auto;
        margin: 1;
    }
    
    #shortcuts-help {
        text-align: center;
        color: $text-muted;
        margin: 2 0;
        width: 100%;
    }
    """
    
    BINDINGS = [
        Binding("s", "study", "Study"),
        Binding("n", "new_card", "New Card"),
        Binding("b", "browse", "Browse Cards"),
        Binding("d", "manage_decks", "Manage Decks"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the dashboard."""
        with Container(id="dashboard-container"):
            yield Static("📚 Welcome to TextuAnki", id="welcome")
            
            # Statistics
            with Horizontal(id="stats-container"):
                # Get statistics
                decks = Deck.get_all()
                total_decks = len(decks)
                total_cards = sum(deck.get_card_count() for deck in decks)
                due_cards = len(Card.get_due_cards())
                
                yield StatsCard("Cards Due", str(due_cards))
                yield StatsCard("Total Cards", str(total_cards))
                yield StatsCard("Total Decks", str(total_decks))
            
            # Menu
            with Vertical(id="menu-container"):
                yield MenuButton("📖 Study Cards", id="study-btn")
                yield MenuButton("➕ Create New Card", id="new-card-btn")
                yield MenuButton("🔍 Browse Cards", id="browse-btn")
                yield MenuButton("📂 Manage Decks", id="decks-btn")
            
            yield Static(
                "Keyboard shortcuts: [S]tudy | [N]ew Card | [B]rowse | [D]ecks | Ctrl+Q to quit",
                id="shortcuts-help"
            )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id
        
        if button_id == "study-btn":
            self.action_study()
        elif button_id == "new-card-btn":
            self.action_new_card()
        elif button_id == "browse-btn":
            self.action_browse()
        elif button_id == "decks-btn":
            self.action_manage_decks()
    
    def action_study(self) -> None:
        """Navigate to study screen."""
        from src.screens.study import StudyScreen
        self.app.push_screen(StudyScreen())
    
    def action_new_card(self) -> None:
        """Navigate to create card screen."""
        from src.screens.create_card import CreateCardScreen
        self.app.push_screen(CreateCardScreen())
    
    def action_browse(self) -> None:
        """Navigate to browse screen."""
        from src.screens.browse import BrowseScreen
        self.app.push_screen(BrowseScreen())
    
    def action_manage_decks(self) -> None:
        """Navigate to deck manager screen."""
        from src.screens.deck_manager import DeckManagerScreen
        self.app.push_screen(DeckManagerScreen())
