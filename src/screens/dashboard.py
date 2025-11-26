"""Dashboard screen for TextuAnki - Modern Colorful Design."""
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal, VerticalScroll
from textual.screen import Screen
from textual.widgets import Static, Button, Label
from textual.binding import Binding

from src.models.deck import Deck
from src.models.card import Card


class StatBlock(Static):
    """Colorful statistics block with gradient."""
    
    DEFAULT_CSS = """
    StatBlock {
        width: 1fr;
        height: 11;
        border: round $accent;
        background: $surface;
        padding: 1 2;
        margin: 0 1;
    }
    
    StatBlock .icon {
        text-align: center;
        text-style: bold;
        color: $accent;
        content-align: center middle;
        height: 3;
    }
    
    StatBlock .value {
        text-align: center;
        text-style: bold;
        color: $primary;
        content-align: center middle;
        height: 4;
    }
    
    StatBlock .label {
        text-align: center;
        color: $text-muted;
        content-align: center middle;
    }
    """
    
    def __init__(self, icon: str, label: str, value: str, **kwargs):
        super().__init__(**kwargs)
        self.icon_char = icon
        self.label_text = label
        self.value_text = value
    
    def compose(self) -> ComposeResult:
        yield Label(self.icon_char, classes="icon")
        yield Label(self.value_text, classes="value")
        yield Label(self.label_text, classes="label")


class MenuButton(Button):
    """Colorful menu button with hover effects."""
    
    DEFAULT_CSS = """
    MenuButton {
        width: 100%;
        height: 4;
        margin: 1 0;
        border: round $primary;
        background: $surface;
        color: $text;
        text-style: bold;
    }
    
    MenuButton:hover {
        background: $primary;
        color: $background;
        border: round $accent;
    }
    
    MenuButton:focus {
        background: $primary;
        color: $background;
        border: round $accent;
    }
    """


class DashboardScreen(Screen):
    """Main dashboard screen - Modern colorful design."""
    
    CSS = """
    DashboardScreen {
        background: $background;
    }
    
    #dashboard-container {
        width: 100%;
        height: 100%;
        background: $background;
        color: $text;
        padding: 2 4;
    }
    
    #title {
        text-align: center;
        text-style: bold;
        color: $primary;
        margin: 1 0 2 0;
        content-align: center middle;
        height: 5;
    }
    
    #subtitle {
        text-align: center;
        color: $text-muted;
        margin: 0 0 2 0;
    }
    
    #stats-container {
        width: 100%;
        height: auto;
        margin: 2 0;
    }
    
    #menu-container {
        width: 60;
        align: center top;
        margin: 2 0;
    }
    
    #shortcuts-help {
        text-align: center;
        color: $text-muted;
        margin: 2 0;
    }
    
    .divider {
        width: 100%;
        height: 1;
        text-align: center;
        color: $primary;
        margin: 1 0;
    }
    """
    
    BINDINGS = [
        Binding("s", "study", "Study", show=True),
        Binding("n", "new_card", "New", show=True),
        Binding("b", "browse", "Browse", show=True),
        Binding("d", "manage_decks", "Decks", show=True),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the dashboard."""
        with VerticalScroll(id="dashboard-container"):
            yield Static("📚 TextuAnki", id="title")
            yield Static("Smart Flashcards with Spaced Repetition", id="subtitle")
            
            yield Static("─" * 70, classes="divider")
            
            # Statistics
            with Horizontal(id="stats-container"):
                # Get statistics
                decks = Deck.get_all()
                total_decks = len(decks)
                total_cards = sum(deck.get_card_count() for deck in decks)
                due_cards = len(Card.get_due_cards())
                
                yield StatBlock("⏰", "Cards Due", str(due_cards))
                yield StatBlock("📖", "Total Cards", str(total_cards))
                yield StatBlock("🗂️", "Decks", str(total_decks))
            
            yield Static("─" * 70, classes="divider")
            
            # Menu
            with Vertical(id="menu-container"):
                yield MenuButton("📝 Study Cards", id="study-btn")
                yield MenuButton("➕ Create New Card", id="new-card-btn")
                yield MenuButton("🔍 Browse Cards", id="browse-btn")
                yield MenuButton("📂 Manage Decks", id="decks-btn")
            
            yield Static("─" * 70, classes="divider")
            
            yield Static(
                "[S]tudy • [N]ew Card • [B]rowse • [D]ecks • Ctrl+Q to quit",
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
