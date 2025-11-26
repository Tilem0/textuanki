"""Main Textual application for TextuAnki."""
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer
from textual.screen import Screen

from src.screens.dashboard import DashboardScreen
from src.database.db import get_db


class TextuAnkiApp(App):
    """A Textual app for managing and studying Anki flashcards."""
    
    # Modern colorful theme with soft gradients
    CSS = """
    Screen {
        background: $background;
    }
    
    Header {
        background: $primary;
        color: $text;
        text-style: bold;
    }
    
    Footer {
        background: $panel;
        color: $text;
    }
    
    /* Colorful modern palette */
    $background: #0a0e27;
    $surface: #1a1f3a;
    $panel: #252b48;
    $primary: #5b7cff;
    $secondary: #7b8cde;
    $accent: #ff6b9d;
    $text: #e8eaf6;
    $text-muted: #8b94c1;
    $error: #ff5555;
    $warning: #ffaa55;
    $success: #50fa7b;
    """
    
    TITLE = "TextuAnki"
    SUB_TITLE = "Smart Flashcards for Your Terminal"
    
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
