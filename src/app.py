"""Main Textual application for TextuAnki."""
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer
from textual.screen import Screen

from src.screens.dashboard import DashboardScreen
from src.database.db import get_db


class TextuAnkiApp(App):
    """A Textual app for managing and studying Anki flashcards."""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    Header {
        background: $primary;
        color: $text;
    }
    
    Footer {
        background: $panel;
    }
    """
    
    TITLE = "TextuAnki"
    SUB_TITLE = "Your Terminal Flashcard Companion"
    
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", priority=True),
        Binding("ctrl+d", "toggle_dark", "Toggle Dark Mode"),
        Binding("ctrl+n", "new_card", "New Card"),
        Binding("ctrl+s", "study", "Study"),
        Binding("ctrl+b", "browse", "Browse"),
        Binding("ctrl+h", "home", "Home"),
    ]
    
    def on_mount(self) -> None:
        """Initialize the app when mounted."""
        # Initialize database
        get_db()
        
        # Push the dashboard screen
        self.push_screen(DashboardScreen())
    
    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.dark = not self.dark
    
    def action_new_card(self) -> None:
        """Navigate to create card screen."""
        from src.screens.create_card import CreateCardScreen
        self.push_screen(CreateCardScreen())
    
    def action_study(self) -> None:
        """Navigate to study screen."""
        from src.screens.study import StudyScreen
        self.push_screen(StudyScreen())
    
    def action_browse(self) -> None:
        """Navigate to browse screen."""
        from src.screens.browse import BrowseScreen
        self.push_screen(BrowseScreen())
    
    def action_home(self) -> None:
        """Return to dashboard."""
        # Pop all screens except dashboard
        while len(self.screen_stack) > 2:  # Keep base screen + dashboard
            self.pop_screen()
