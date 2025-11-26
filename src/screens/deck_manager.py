"""Deck manager screen for TextuAnki."""
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen, ModalScreen
from textual.widgets import Static, DataTable, Button, Input, Label
from textual.binding import Binding

from src.models.deck import Deck
from src.banners import DECK_BANNER, to_smallcaps


class CreateDeckModal(ModalScreen):
    """Modal for creating a new deck."""
    
    CSS = """
    CreateDeckModal {
        align: center middle;
        background: #00000099;
    }
    
    #modal-container {
        width: 60;
        height: auto;
        border: heavy #FFFFFF;
        background: #000000;
        padding: 2 3;
    }
    
    #modal-title {
        text-align: center;
        text-style: bold;
        color: #FFFFFF;
        margin: 0 0 1 0;
        background: #000000;
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
    
    #button-row {
        align: center middle;
        height: auto;
        margin: 1 0 0 0;
        background: #000000;
    }
    
    Button {
        min-width: 12;
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
    """
    
    def compose(self) -> ComposeResult:
        with Container(id="modal-container"):
            yield Static("【 " + to_smallcaps("create new deck") + " 】", id="modal-title")
            yield Label(to_smallcaps("deck name:"))
            yield Input(placeholder="e.g., Spanish Vocabulary", id="deck-name")
            yield Label(to_smallcaps("description (optional):"))
            yield Input(placeholder="Description", id="deck-description")
            
            with Horizontal(id="button-row"):
                yield Button("✓ CREATE", id="create-btn")
                yield Button("✗ CANCEL", id="cancel-btn")
    
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
    DeckManagerScreen {
        background: #000000;
    }
    
    #deck-manager-container {
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
    
    DataTable {
        height: 1fr;
        margin: 1 0;
        border: heavy #FFFFFF;
        background: #000000;
        color: #FFFFFF;
    }
    
    DataTable > .datatable--header {
        background: #000000;
        color: #FFFFFF;
        text-style: bold;
    }
    
    DataTable > .datatable--cursor {
        background: #FFFFFF;
        color: #000000;
    }
    
    DataTable > .datatable--odd-row {
        background: #000000;
    }
    
    DataTable > .datatable--even-row {
        background: #000000;
    }
    
    #button-container {
        height: auto;
        margin: 1 0;
        align: center middle;
        background: #000000;
    }
    
    Button {
        min-width: 16;
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
        Binding("escape", "back", "Back"),
        Binding("n", "new_deck", "New Deck"),
        Binding("d", "delete", "Delete Deck"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets for deck management."""
        with Container(id="deck-manager-container"):
            yield Static(DECK_BANNER, id="banner")
            yield DataTable(id="decks-table")
            
            with Horizontal(id="button-container"):
                yield Button("✚ NEW DECK [N]", id="new-btn")
                yield Button("✗ DELETE [D]", id="delete-btn")
            
            yield Static(
                to_smallcaps("arrow keys to navigate | n for new deck | d to delete | esc to go back"),
                id="instructions"
            )
    
    def on_mount(self) -> None:
        """Set up the data table when screen mounts."""
        self.load_decks()
    
    def load_decks(self) -> None:
        """Load decks into the table."""
        table = self.query_one(DataTable)
        table.clear(columns=True)
        table.add_columns(
            to_smallcaps("id"),
            to_smallcaps("name"),
            to_smallcaps("description"),
            to_smallcaps("cards")
        )
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
        
        if table.cursor_row is not None and table.cursor_row >= 0:
            row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
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
