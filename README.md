# TextuAnki 📚

A clean, easy-to-use terminal-based interface (TUI) for creating and studying Anki-style flashcards.

## Features

- **Beautiful TUI**: Clean, distraction-free interface built with Textual
- **Spaced Repetition**: Uses the SM-2 algorithm for optimal learning
- **Deck Management**: Organize your cards into multiple decks
- **Easy Card Creation**: Simple, keyboard-focused workflow
- **Study Mode**: Focus on what matters with an intuitive study interface
- **Browse & Edit**: Search and manage your entire card collection
- **Keyboard-First**: Everything accessible via keyboard shortcuts

## Installation

### Requirements

- Python 3.10 or higher

### Install

```bash
# Clone or navigate to the project directory
cd textuanki

# Install dependencies
pip install -e .
```

## Usage

### Running the App

```bash
# Run directly with Python
python -m src.main

# Or if installed
textuanki
```

### Keyboard Shortcuts

#### Global
- `Ctrl+Q` - Quit the application
- `Ctrl+D` - Toggle dark mode
- `Ctrl+H` - Return to dashboard
- `Ctrl+N` - Create new card
- `Ctrl+S` - Start studying
- `Ctrl+B` - Browse cards

#### Dashboard
- `S` - Study cards
- `N` - Create new card
- `B` - Browse cards
- `D` - Manage decks

#### Study Mode
- `Space` - Reveal answer
- `1` - Rate: Again (restart)
- `2` - Rate: Hard
- `3` - Rate: Good
- `4` - Rate: Easy
- `Esc` - Exit study mode

#### Browse/Manage
- Arrow keys - Navigate
- `D` - Delete selected item
- `Esc` - Go back

## Project Structure

```
textuanki/
├── src/
│   ├── main.py              # Entry point
│   ├── app.py               # Main Textual application
│   ├── screens/             # UI screens
│   │   ├── dashboard.py     # Main dashboard
│   │   ├── study.py         # Study mode
│   │   ├── create_card.py   # Card creation
│   │   ├── browse.py        # Browse cards
│   │   └── deck_manager.py  # Manage decks
│   ├── models/              # Data models
│   │   ├── card.py          # Card model
│   │   ├── deck.py          # Deck model
│   │   └── review.py        # Review/SRS logic
│   ├── database/            # Database layer
│   │   └── db.py            # SQLite connection & schema
│   └── anki/                # Anki integration (future)
└── tests/                   # Test suite
```

## How It Works

### Spaced Repetition

TextuAnki uses the SM-2 (SuperMemo 2) algorithm for spaced repetition:

- **Again (1)**: Card was forgotten, restart learning
- **Hard (2)**: Difficult recall, shorter interval
- **Good (3)**: Correct recall, standard interval
- **Easy (4)**: Perfect recall, longer interval

The algorithm automatically schedules reviews at optimal intervals to maximize retention.

### Data Storage

All data is stored locally in a SQLite database at `~/.textuanki/cards.db`. Your flashcards never leave your computer.

## Future Enhancements

- [ ] Export decks to Anki (.apkg format)
- [ ] Import existing Anki decks
- [ ] Statistics and progress tracking
- [ ] Card templates and formatting
- [ ] Image support
- [ ] Cloze deletion cards
- [ ] Multiple card types
- [ ] Custom study sessions

## Development

### Running Tests

```bash
pytest tests/
```

### Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

MIT License - feel free to use this project for your learning needs!

## Credits

Built with:
- [Textual](https://textual.textualize.io/) - Modern TUI framework
- [genanki](https://github.com/kerrickstaley/genanki) - Anki deck generation
- SQLite - Local database

Inspired by [Anki](https://apps.ankiweb.net/), the amazing spaced repetition software.
