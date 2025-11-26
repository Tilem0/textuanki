"""Browse cards screen for TextuAnki."""
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Static, DataTable, Button
from textual.binding import Binding

from src.models.card import Card
from src.models.deck import Deck


class BrowseScreen(Screen):
    """Screen for browsing and managing cards."""
    
    CSS = """
    #browse-container {
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
    """
    
    BINDINGS = [
        Binding("escape", "back", "Back"),
        Binding("d", "delete", "Delete Card"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets for browsing."""
        with Container(id="browse-container"):
            yield Static("🔍 Browse Cards", id="title")
            yield DataTable(id="cards-table")
            yield Static(
                "Use arrow keys to navigate | [D]elete | ESC to go back",
                classes="help-text"
            )
    
    def on_mount(self) -> None:
        """Set up the data table when screen mounts."""
        table = self.query_one(DataTable)
        table.add_columns("ID", "Deck", "Front", "Back", "Tags")
        table.cursor_type = "row"
        
        # Load all cards
        decks = {deck.id: deck.name for deck in Deck.get_all()}
        
        for deck_id, deck_name in decks.items():
            cards = Card.get_by_deck(deck_id)
            for card in cards:
                # Truncate long text
                front = card.front[:50] + "..." if len(card.front) > 50 else card.front
                back = card.back[:50] + "..." if len(card.back) > 50 else card.back
                
                table.add_row(
                    str(card.id),
                    deck_name,
                    front,
                    back,
                    card.tags or ""
                )
    
    def action_delete(self) -> None:
        """Delete the selected card."""
        table = self.query_one(DataTable)
        
        if table.cursor_row is not None:
            row_key = table.coordinate_to_cell_key((table.cursor_row, 0)).row_key
            row = table.get_row(row_key)
            card_id = int(row[0])
            
            # Confirm deletion
            card = Card.get_by_id(card_id)
            if card:
                card.delete()
                table.remove_row(row_key)
                self.notify(f"Card deleted", severity="information")
    
    def action_back(self) -> None:
        """Return to dashboard."""
        self.app.pop_screen()
