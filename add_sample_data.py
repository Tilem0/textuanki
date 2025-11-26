"""Add sample flashcards for testing."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.database.db import get_db
from src.models.deck import Deck
from src.models.card import Card

def add_sample_data():
    """Add sample decks and cards."""
    db = get_db()
    
    # Create additional decks
    print("Creating sample decks...")
    
    try:
        spanish = Deck.create(
            name="Spanish Vocabulary",
            description="Basic Spanish words and phrases"
        )
        print(f"✓ Created deck: {spanish.name}")
    except:
        spanish = [d for d in Deck.get_all() if d.name == "Spanish Vocabulary"][0]
    
    try:
        python_deck = Deck.create(
            name="Python Programming",
            description="Python concepts and syntax"
        )
        print(f"✓ Created deck: {python_deck.name}")
    except:
        python_deck = [d for d in Deck.get_all() if d.name == "Python Programming"][0]
    
    # Add Spanish vocabulary cards
    print("\nAdding Spanish vocabulary cards...")
    spanish_cards = [
        ("Hola", "Hello", "greetings, basic"),
        ("Adiós", "Goodbye", "greetings, basic"),
        ("Por favor", "Please", "politeness, basic"),
        ("Gracias", "Thank you", "politeness, basic"),
        ("¿Cómo estás?", "How are you?", "questions, basic"),
        ("Me llamo...", "My name is...", "introductions, basic"),
        ("¿Dónde está...?", "Where is...?", "questions, travel"),
        ("El agua", "The water", "nouns, food"),
        ("La comida", "The food", "nouns, food"),
        ("Buenas noches", "Good night", "greetings, time"),
    ]
    
    for front, back, tags in spanish_cards:
        Card.create(deck_id=spanish.id, front=front, back=back, tags=tags)
        print(f"  ✓ {front}")
    
    # Add Python programming cards
    print("\nAdding Python programming cards...")
    python_cards = [
        ("What is a list comprehension?", 
         "A concise way to create lists: [x for x in iterable if condition]",
         "syntax, intermediate"),
        ("What does 'self' represent in a class?",
         "The instance of the class itself",
         "oop, basics"),
        ("What is the difference between '==' and 'is'?",
         "'==' compares values, 'is' compares identity (memory location)",
         "operators, basics"),
        ("What is a decorator?",
         "A function that modifies the behavior of another function, uses @syntax",
         "advanced, functions"),
        ("What is the GIL?",
         "Global Interpreter Lock - prevents multiple threads from executing Python bytecode simultaneously",
         "advanced, concurrency"),
        ("How do you open a file safely?",
         "Use 'with open(filename) as f:' context manager",
         "io, best-practices"),
        ("What is a lambda function?",
         "An anonymous function defined with: lambda args: expression",
         "functions, basics"),
        ("What does '*args' mean?",
         "Variable number of positional arguments passed to a function",
         "functions, arguments"),
        ("What does '**kwargs' mean?",
         "Variable number of keyword arguments passed to a function",
         "functions, arguments"),
        ("What is pip?",
         "Python package installer - installs packages from PyPI",
         "tools, basics"),
    ]
    
    for front, back, tags in python_cards:
        Card.create(deck_id=python_deck.id, front=front, back=back, tags=tags)
        print(f"  ✓ {front[:50]}...")
    
    # Add some cards to default deck
    default_deck = [d for d in Deck.get_all() if d.name == "Default"][0]
    print("\nAdding general knowledge cards to Default deck...")
    general_cards = [
        ("What is the capital of France?", "Paris", "geography"),
        ("Who wrote 'Romeo and Juliet'?", "William Shakespeare", "literature"),
        ("What is 2^10?", "1024", "math"),
    ]
    
    for front, back, tags in general_cards:
        Card.create(deck_id=default_deck.id, front=front, back=back, tags=tags)
        print(f"  ✓ {front}")
    
    print("\n" + "="*50)
    print("Sample data added successfully!")
    print("="*50)
    
    # Print summary
    decks = Deck.get_all()
    print(f"\nTotal decks: {len(decks)}")
    for deck in decks:
        count = deck.get_card_count()
        print(f"  - {deck.name}: {count} cards")
    
    total_cards = sum(deck.get_card_count() for deck in decks)
    print(f"\nTotal cards: {total_cards}")
    print("\nRun './run.sh' or 'python src/main.py' to start studying!")


if __name__ == "__main__":
    add_sample_data()
