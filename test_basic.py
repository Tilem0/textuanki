"""Basic test script for TextuAnki."""
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Test imports
print("Testing imports...")
try:
    from src.database.db import Database, get_db
    print("✓ Database module imported")
    
    from src.models.deck import Deck
    print("✓ Deck model imported")
    
    from src.models.card import Card
    print("✓ Card model imported")
    
    from src.models.review import Review
    print("✓ Review model imported")
    
    from src.app import TextuAnkiApp
    print("✓ App imported")
    
    print("\nAll imports successful!")
    
    # Test database creation
    print("\nTesting database...")
    db = get_db()
    print("✓ Database initialized")
    
    # Test deck operations
    print("\nTesting deck operations...")
    decks = Deck.get_all()
    print(f"✓ Found {len(decks)} deck(s)")
    if decks:
        print(f"  - Default deck: {decks[0].name}")
    
    # Test card creation
    print("\nTesting card creation...")
    default_deck = decks[0]
    test_card = Card.create(
        deck_id=default_deck.id,
        front="What is 2+2?",
        back="4",
        tags="math, test"
    )
    print(f"✓ Created test card (ID: {test_card.id})")
    
    # Test card retrieval
    cards = Card.get_by_deck(default_deck.id)
    print(f"✓ Retrieved {len(cards)} card(s) from default deck")
    
    print("\n🎉 All tests passed!")
    print("\nYou can now run the app with:")
    print("  source venv/bin/activate")
    print("  python src/main.py")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
