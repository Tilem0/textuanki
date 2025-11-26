# TextuAnki - Quick Start Guide

Welcome to TextuAnki! Here's how to get started in 60 seconds.

## Installation

```bash
# 1. Make sure you're in the project directory
cd textuanki

# 2. Run the setup (creates venv and installs dependencies automatically)
./run.sh
```

That's it! The app will launch.

## First Time Setup

The app comes with sample flashcards to help you get started:
- **Default** - General knowledge (4 cards)
- **Spanish Vocabulary** - Basic Spanish (10 cards)
- **Python Programming** - Python concepts (10 cards)

## Quick Tour

### Main Screen
When you launch TextuAnki, you'll see:
- **Statistics** at the top (cards due, total cards, total decks)
- **Menu buttons** in the center
- **Keyboard shortcuts** at the bottom

### Creating Your First Card

1. Press `N` or click "Create New Card"
2. Select a deck (or use Default)
3. Fill in the question (front)
4. Fill in the answer (back)
5. Optionally add tags
6. Press `Ctrl+S` or click "Save Card"

### Studying Cards

1. Press `S` or click "Study Cards"
2. Read the question
3. Press `Space` to reveal the answer
4. Rate your recall:
   - `1` - Again (forgot it)
   - `2` - Hard (difficult to remember)
   - `3` - Good (remembered correctly)
   - `4` - Easy (very easy to remember)

The app uses spaced repetition to schedule reviews optimally!

### Managing Decks

1. Press `D` or click "Manage Decks"
2. Press `N` to create a new deck
3. Select a deck and press `D` to delete it
4. Press `Esc` to go back

### Browsing Cards

1. Press `B` or click "Browse Cards"
2. Use arrow keys to navigate
3. Press `D` to delete a card
4. Press `Esc` to go back

## Essential Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Q` | Quit application |
| `Ctrl+H` | Return to dashboard |
| `Ctrl+N` | Create new card |
| `Ctrl+S` | Start studying |
| `Ctrl+B` | Browse cards |
| `Ctrl+D` | Toggle dark mode |
| `Esc` | Go back / Cancel |

## Tips for Effective Study

1. **Study daily** - Even 5 minutes helps with retention
2. **Be honest** - Rate your recall accurately
3. **Make good cards** - Clear questions, specific answers
4. **Use tags** - Organize cards by topic
5. **Start small** - Add a few cards at a time

## Data Location

Your flashcards are stored at: `~/.textuanki/cards.db`

This is a SQLite database you can backup or transfer to other machines.

## Troubleshooting

### App won't start?
```bash
# Recreate virtual environment
rm -rf venv
./run.sh
```

### Want to reset all data?
```bash
# Remove database
rm -rf ~/.textuanki/

# Run the app - it will create a fresh database
./run.sh
```

### Need more sample data?
```bash
source venv/bin/activate
python add_sample_data.py
```

## Next Steps

1. Try studying the sample cards
2. Create your own deck
3. Add cards for something you're learning
4. Build a daily study habit!

## Getting Help

- Check the main README.md for detailed documentation
- All screens show keyboard shortcuts at the bottom
- Press `?` or check the footer for available commands

Happy studying! 📚
