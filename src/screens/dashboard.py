"""Dashboard screen for TextuAnki - Brutalist E-ink Design."""
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal, VerticalScroll
from textual.screen import Screen
from textual.widgets import Static, Button, Label
from textual.binding import Binding

from src.models.deck import Deck
from src.models.card import Card
from src.banners import TEXTUANKI_BANNER, KANJI, smallcaps


class StatBlock(Static):
    """Brutalist statistics block."""
    
    DEFAULT_CSS = """
    StatBlock {
        width: 1fr;
        height: 9;
        border: heavy #FFFFFF;
        background: #000000;
        padding: 1 2;
        margin: 0 1;
    }
    
    StatBlock .kanji {
        text-align: center;
        text-style: bold;
        color: #FFFFFF;
        content-align: center middle;
        height: 3;
    }
    
    StatBlock .value {
        text-align: center;
        text-style: bold;
        color: #FFFFFF;
        content-align: center middle;
        height: 3;
    }
    
    StatBlock .label {
        text-align: center;
        color: #999999;
        content-align: center middle;
    }
    """
    
    def __init__(self, kanji: str, label: str, value: str, **kwargs):
        super().__init__(**kwargs)
        self.kanji_char = kanji
        self.label_text = label
        self.value_text = value
    
    def compose(self) -> ComposeResult:
        yield Label(self.kanji_char, classes="kanji")
        yield Label(self.value_text, classes="value")
        yield Label(smallcaps(self.label_text), classes="label")


class BrutalistButton(Button):
    """Brutalist menu button."""
    
    DEFAULT_CSS = """
    BrutalistButton {
        width: 100%;
        height: 5;
        margin: 1 0;
        border: heavy #FFFFFF;
        background: #000000;
        color: #FFFFFF;
        text-style: bold;
    }
    
    BrutalistButton:hover {
        background: #FFFFFF;
        color: #000000;
    }
    
    BrutalistButton:focus {
        background: #FFFFFF;
        color: #000000;
        border: heavy #FFFFFF;
    }
    """


class DashboardScreen(Screen):
    """Main dashboard screen - Brutalist design."""
    
    CSS = """
    Screen {
        background: #000000;
    }
    
    #dashboard-container {
        width: 100%;
        height: 100%;
        background: #000000;
        color: #FFFFFF;
    }
    
    #banner {
        width: 100%;
        height: auto;
        text-align: center;
        color: #FFFFFF;
        margin: 1 0;
        text-style: bold;
    }
    
    #stats-container {
        height: auto;
        width: 100%;
        margin: 2 0;
    }
    
    #menu-container {
        width: 70;
        height: auto;
        align: center top;
        margin: 2 0;
    }
    
    #shortcuts-help {
        text-align: center;
        color: #666666;
        margin: 2 0;
        width: 100%;
    }
    
    #divider {
        width: 100%;
        height: 1;
        text-align: center;
        color: #FFFFFF;
        margin: 1 0;
    }
    
    .divider {
        width: 100%;
        height: 1;
        text-align: center;
        color: #FFFFFF;
        margin: 1 0;
    }
    """
    
    BINDINGS = [
        Binding("s", "study", "ｓᴛᴜᴅʏ", show=True),
        Binding("n", "new_card", "ɴᴇᴡ", show=True),
        Binding("b", "browse", "ʙʀᴏᴡsᴇ", show=True),
        Binding("d", "manage_decks", "ᴅᴇᴄᴋs", show=True),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the dashboard."""
        with VerticalScroll(id="dashboard-container"):
            yield Static(TEXTUANKI_BANNER, id="banner")
            
            yield Static("━" * 70, classes="divider")
            
            # Statistics
            with Horizontal(id="stats-container"):
                # Get statistics
                decks = Deck.get_all()
                total_decks = len(decks)
                total_cards = sum(deck.get_card_count() for deck in decks)
                due_cards = len(Card.get_due_cards())
                
                yield StatBlock(KANJI["due"], "CARDS DUE", str(due_cards))
                yield StatBlock(KANJI["total"], "TOTAL CARDS", str(total_cards))
                yield StatBlock(KANJI["deck"], "DECKS", str(total_decks))
            
            yield Static("━" * 70, classes="divider")
            
            # Menu
            with Vertical(id="menu-container"):
                yield BrutalistButton(f"┃ {KANJI['study']} ┃ " + smallcaps("STUDY CARDS") + " ┃", id="study-btn")
                yield BrutalistButton(f"┃ {KANJI['new']} ┃ " + smallcaps("CREATE NEW CARD") + " ┃", id="new-card-btn")
                yield BrutalistButton(f"┃ {KANJI['card']} ┃ " + smallcaps("BROWSE CARDS") + " ┃", id="browse-btn")
                yield BrutalistButton(f"┃ {KANJI['deck']} ┃ " + smallcaps("MANAGE DECKS") + " ┃", id="decks-btn")
            
            yield Static("━" * 70, classes="divider")
            
            yield Static(
                smallcaps("[S]tudy | [N]ew | [B]rowse | [D]ecks | ^Q quit"),
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
