"""Browse cards screen for TextuAnki."""
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Static, DataTable, Button
from textual.binding import Binding

from src.models.card import Card
from src.models.deck import Deck
from src.banners import BROWSE_BANNER, to_smallcaps


class BrowseScreen(Screen):
    """Screen for browsing and managing cards."""
    
    CSS = """
    BrowseScreen {
        background: #000000;
    }
    
    #browse-container {
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
    
    #instructions {
        text-align: center;
        color: #666666;
        margin: 1 0;
        background: #000000;
    }
    """
    
    BINDINGS = [
        Binding("escape", "back", "Back"),
        Binding("d", "delete", "Delete Card"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets for browsing."""
        with Container(id="browse-container"):
            yield Static(BROWSE_BANNER, id="banner")
            yield DataTable(id="cards-table")
            yield Static(
                to_smallcaps("arrow keys to navigate | d to delete | esc to go back"),
                id="instructions"
            )
    
    def on_mount(self) -> None:
        """Set up the data table when screen mounts."""
        table = self.query_one(DataTable)
        table.add_columns(
            to_smallcaps("id"),
            to_smallcaps("deck"),
            to_smallcaps("front"),
            to_smallcaps("back"),
            to_smallcaps("tags")
        )
        table.cursor_type = "row"
        
        # Load all cards
        decks = {deck.id: deck.name for deck in Deck.get_all()}
        
        for deck_id, deck_name in decks.items():
            if deck_id is None:
                continue
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
        
        if table.cursor_row is not None and table.cursor_row >= 0:
            row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
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
