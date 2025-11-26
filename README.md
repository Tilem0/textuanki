# TextuAnki 📚

A clean, easy-to-use terminal-based interface (TUI) for creating and studying Anki-style flashcards.

[![GitHub](https://img.shields.io/badge/github-textuanki-blue?logo=github)](https://github.com/Tilem0/textuanki)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

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
# Clone the repository
git clone https://github.com/Tilem0/textuanki.git
cd textuanki

# Run the app (auto-creates venv and installs dependencies)
./run.sh
```

Or manually:

Or manually:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install textual genanki
```

## Quick Start

```bash
# Run the app
./run.sh

# Or manually
source venv/bin/activate
python src/main.py
```

The app comes with 24 sample flashcards to get you started!

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
source venv/bin/activate
python test_basic.py
```

### Adding Sample Data

```bash
source venv/bin/activate
python add_sample_data.py
```

### Contributing

Contributions are welcome! Feel free to:
- Report bugs via [GitHub Issues](https://github.com/Tilem0/textuanki/issues)
- Submit feature requests
- Create pull requests

See [agent.md](agent.md) for detailed project documentation.

## Documentation

- **[START_HERE.md](START_HERE.md)** - Welcome guide for new users
- **[QUICKSTART.md](QUICKSTART.md)** - Quick installation and usage
- **[FEATURES.md](FEATURES.md)** - Complete feature reference
- **[DEMO.md](DEMO.md)** - Visual interface tour
- **[agent.md](agent.md)** - Comprehensive project documentation

## License

MIT License - feel free to use this project for your learning needs!

## Credits

Built with:
- [Textual](https://textual.textualize.io/) - Modern TUI framework
- [genanki](https://github.com/kerrickstaley/genanki) - Anki deck generation
- SQLite - Local database

Inspired by [Anki](https://apps.ankiweb.net/), the amazing spaced repetition software.
