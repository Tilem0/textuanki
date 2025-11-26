"""Deck manager screen for TextuAnki."""
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen, ModalScreen
from textual.widgets import Static, DataTable, Button, Input, Label
from textual.binding import Binding

from src.models.deck import Deck


class CreateDeckModal(ModalScreen):
    """Modal for creating a new deck."""
    
    CSS = """
    CreateDeckModal {
        align: center middle;
    }
    
    #modal-container {
        width: 60;
        height: auto;
        border: thick $accent;
        background: $surface;
        padding: 2;
    }
    
    Label {
        margin: 1 0 0 0;
    }
    
    Input {
        margin: 0 0 1 0;
    }
    
    Button {
        margin: 0 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        with Container(id="modal-container"):
            yield Static("Create New Deck", classes="modal-title")
            yield Label("Deck Name:")
            yield Input(placeholder="e.g., Spanish Vocabulary", id="deck-name")
            yield Label("Description (optional):")
            yield Input(placeholder="Description", id="deck-description")
            
            with Horizontal():
                yield Button("Create", variant="success", id="create-btn")
                yield Button("Cancel", variant="default", id="cancel-btn")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "create-btn":
            name_input = self.query_one("#deck-name", Input)
            desc_input = self.query_one("#deck-description", Input)
            
            name = name_input.value.strip()
            description = desc_input.value.strip()
            
            if not name:
                self.app.notify("Deck name is required", severity="error")
                return
            
            try:
                Deck.create(name=name, description=description)
                self.app.notify(f"Deck '{name}' created!", severity="information")
                self.dismiss(True)
            except Exception as e:
                self.app.notify(f"Error: {str(e)}", severity="error")
        else:
            self.dismiss(False)


class DeckManagerScreen(Screen):
    """Screen for managing decks."""
    
    CSS = """
    #deck-manager-container {
        width: 100%;
        height: 100%;
        padding: 2 4;
    }
    
    #title {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin: 1 0 2 0;
    }
    
    DataTable {
        height: 1fr;
        margin: 1 0;
    }
    
    #button-container {
        height: auto;
        margin: 1 0;
    }
    """
    
    BINDINGS = [
        Binding("escape", "back", "Back"),
        Binding("n", "new_deck", "New Deck"),
        Binding("d", "delete", "Delete Deck"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets for deck management."""
        with Container(id="deck-manager-container"):
            yield Static("📂 Manage Decks", id="title")
            yield DataTable(id="decks-table")
            
            with Horizontal(id="button-container"):
                yield Button("New Deck [N]", variant="success", id="new-btn")
                yield Button("Delete [D]", variant="error", id="delete-btn")
            
            yield Static(
                "Use arrow keys to navigate | [N]ew Deck | [D]elete | ESC to go back",
                classes="help-text"
            )
    
    def on_mount(self) -> None:
        """Set up the data table when screen mounts."""
        self.load_decks()
    
    def load_decks(self) -> None:
        """Load decks into the table."""
        table = self.query_one(DataTable)
        table.clear(columns=True)
        table.add_columns("ID", "Name", "Description", "Cards")
        table.cursor_type = "row"
        
        decks = Deck.get_all()
        for deck in decks:
            table.add_row(
                str(deck.id),
                deck.name,
                deck.description or "",
                str(deck.get_card_count())
            )
    
    def action_new_deck(self) -> None:
        """Show modal to create a new deck."""
        def check_result(created: bool) -> None:
            if created:
                self.load_decks()
        
        self.app.push_screen(CreateDeckModal(), check_result)
    
    def action_delete(self) -> None:
        """Delete the selected deck."""
        table = self.query_one(DataTable)
        
        if table.cursor_row is not None:
            row_key = table.coordinate_to_cell_key((table.cursor_row, 0)).row_key
            row = table.get_row(row_key)
            deck_id = int(row[0])
            deck_name = row[1]
            
            # Prevent deleting default deck
            if deck_name == "Default":
                self.notify("Cannot delete the default deck", severity="error")
                return
            
            deck = Deck.get_by_id(deck_id)
            if deck:
                deck.delete()
                table.remove_row(row_key)
                self.notify(f"Deck '{deck_name}' deleted", severity="information")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "new-btn":
            self.action_new_deck()
        elif event.button.id == "delete-btn":
            self.action_delete()
    
    def action_back(self) -> None:
        """Return to dashboard."""
        self.app.pop_screen()
