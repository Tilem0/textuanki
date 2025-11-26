# TextuAnki - AI Agent Project Description

## Project Overview

**TextuAnki** is a modern, terminal-based flashcard application built with Python and Textual. It provides a clean, keyboard-driven interface for creating and studying flashcards using proven spaced repetition algorithms.

## Purpose & Vision

The goal of TextuAnki is to create a distraction-free, efficient learning tool that:
- Works entirely in the terminal (perfect for developers and CLI enthusiasts)
- Respects user privacy with 100% local data storage
- Implements effective spaced repetition for optimal learning
- Offers a beautiful, intuitive user interface despite being text-based
- Requires zero configuration to get started

## Technical Stack

### Core Technologies
- **Python 3.10+** - Modern Python features and type hints
- **Textual 6.6.0** - Modern TUI framework for rich terminal interfaces
- **SQLite3** - Lightweight, embedded database for local storage
- **genanki** - Library for future Anki deck import/export functionality

### Architecture
- **MVC-style separation** - Clean separation of data models, UI screens, and database layer
- **Screen-based navigation** - Intuitive multi-screen TUI with proper state management
- **Event-driven UI** - Reactive interface responding to keyboard and button events
- **Dataclass models** - Type-safe data models with clear interfaces

## Key Features

### Core Functionality
1. **Flashcard Management**
   - Create cards with front (question) and back (answer)
   - Organize cards into multiple decks
   - Tag cards for easy categorization
   - Browse and search through card collection
   - Delete unwanted cards

2. **Spaced Repetition System**
   - SM-2 algorithm implementation
   - Automatic scheduling based on recall difficulty
   - Four rating levels (Again, Hard, Good, Easy)
   - Tracks review history and statistics
   - Optimizes learning intervals for long-term retention

3. **User Interface**
   - Dashboard with live statistics
   - Study mode with clean card presentation
   - Card creation form with validation
   - Deck management interface
   - Browse/search functionality

4. **Keyboard-First Design**
   - All features accessible via keyboard
   - Intuitive shortcuts (Ctrl+N, Ctrl+S, etc.)
   - Vim-style navigation where appropriate
   - Help text on every screen

## Project Structure

```
textuanki/
├── src/
│   ├── main.py              # Application entry point
│   ├── app.py               # Main Textual application class
│   ├── screens/             # UI screens
│   │   ├── dashboard.py     # Main dashboard with statistics
│   │   ├── study.py         # Study mode with SRS
│   │   ├── create_card.py   # Card creation form
│   │   ├── browse.py        # Browse/search cards
│   │   └── deck_manager.py  # Deck management
│   ├── models/              # Data models
│   │   ├── card.py          # Card CRUD operations
│   │   ├── deck.py          # Deck CRUD operations
│   │   └── review.py        # SRS algorithm & review tracking
│   ├── database/            # Database layer
│   │   └── db.py            # SQLite schema & connection management
│   ├── widgets/             # Custom Textual widgets (future)
│   └── anki/                # Anki import/export (future)
├── tests/                   # Test suite (future)
├── docs/                    # Documentation
│   ├── START_HERE.md        # Quick start guide
│   ├── QUICKSTART.md        # Installation & first steps
│   ├── FEATURES.md          # Detailed feature documentation
│   └── DEMO.md              # Visual interface tour
├── run.sh                   # Convenience launcher script
├── test_basic.py            # Basic functionality tests
├── add_sample_data.py       # Sample data generator
├── pyproject.toml           # Project configuration
└── README.md                # Main documentation

Data Storage:
~/.textuanki/cards.db        # SQLite database (auto-created)
```

## Implementation Details

### Database Schema

**decks table:**
- id (PRIMARY KEY)
- name (UNIQUE)
- description
- created_at, updated_at (timestamps)

**cards table:**
- id (PRIMARY KEY)
- deck_id (FOREIGN KEY → decks)
- front (question text)
- back (answer text)
- tags (comma-separated)
- created_at, updated_at (timestamps)

**reviews table:**
- id (PRIMARY KEY)
- card_id (FOREIGN KEY → cards)
- ease_factor (SM-2 algorithm parameter)
- interval (days until next review)
- repetitions (successful review count)
- due_date (next scheduled review)
- last_review (timestamp)

**study_sessions table:**
- id (PRIMARY KEY)
- card_id (FOREIGN KEY → cards)
- rating (0-4, user's recall difficulty)
- duration (session length)
- reviewed_at (timestamp)

### Spaced Repetition Algorithm (SM-2)

The SM-2 algorithm adjusts review intervals based on recall quality:

```python
# Rating system:
# 0 = Complete blackout (Again)
# 2 = Incorrect but familiar (Hard)
# 3 = Correct with effort (Good)
# 4 = Perfect recall (Easy)

# Interval calculation:
if rating < 3:
    interval = 1  # Reset to start
else:
    if repetitions == 0:
        interval = 1
    elif repetitions == 1:
        interval = 6
    else:
        interval = previous_interval * ease_factor

# Ease factor adjustment:
ease_factor = max(1.3, ease_factor + (0.1 - (5 - rating) * (0.08 + (5 - rating) * 0.02)))
```

### UI/UX Design Principles

1. **Clarity** - Clear labels, helpful hints, obvious actions
2. **Consistency** - Same patterns throughout the app
3. **Feedback** - Immediate visual response to all actions
4. **Efficiency** - Keyboard shortcuts for power users
5. **Forgiveness** - Easy to undo mistakes, clear confirmations

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guide
- Use type hints for all function signatures
- Document all public methods and classes
- Keep functions focused and single-purpose
- Prefer composition over inheritance

### Testing Strategy
- Unit tests for data models
- Integration tests for database operations
- UI tests for screen interactions (future)
- Manual testing for user workflows

### Git Workflow
- `main` branch for stable releases
- Feature branches for new development
- Descriptive commit messages
- Tag releases with semantic versioning

## Future Enhancements

### Planned Features
1. **Anki Integration**
   - Export decks to .apkg format
   - Import existing Anki decks
   - Maintain compatibility with Anki ecosystem

2. **Advanced Study Features**
   - Custom study sessions (by tag, deck, date range)
   - Multiple card types (basic, cloze, image)
   - Card templates for consistent formatting
   - Bulk card operations

3. **Statistics & Analytics**
   - Study streak tracking
   - Retention rate graphs
   - Time spent studying
   - Card difficulty analysis
   - Deck performance comparison

4. **Enhanced UI**
   - Card preview in browse mode
   - In-line card editing
   - Search with filters
   - Custom themes
   - Keyboard shortcut customization

5. **Synchronization**
   - Cloud backup option
   - Multi-device sync
   - Deck sharing with other users
   - Collaborative deck building

### Technical Improvements
- Comprehensive test suite (pytest)
- CI/CD pipeline (GitHub Actions)
- Performance optimization for large decks (10k+ cards)
- Plugin system for extensibility
- CLI commands for automation

## Use Cases

### Students
- Memorize vocabulary for language learning
- Study concepts for exams
- Review lecture notes
- Prepare for standardized tests

### Professionals
- Learn programming languages and frameworks
- Memorize industry terminology
- Prepare for certifications
- Study for job interviews

### Lifelong Learners
- Build general knowledge
- Learn new hobbies
- Memorize quotes or poetry
- Practice trivia

## Success Metrics

The project is successful when:
- ✅ Users can create and study cards immediately without configuration
- ✅ Spaced repetition effectively improves long-term retention
- ✅ Interface is intuitive enough to not need extensive documentation
- ✅ App works reliably over SSH and on all major platforms
- ✅ Data remains private and portable
- ✅ Community finds it useful and contributes improvements

## Contributing

Contributions are welcome! Areas where help is especially appreciated:
- **Testing** - Write tests, report bugs, test on different platforms
- **Features** - Implement planned features or suggest new ones
- **Documentation** - Improve guides, add tutorials, create screencasts
- **UI/UX** - Design improvements, accessibility enhancements
- **Localization** - Translate interface to other languages

## License

MIT License - Free to use, modify, and distribute.

## Contact & Support

- **GitHub Issues** - Bug reports and feature requests
- **Discussions** - Questions and general discussion
- **Pull Requests** - Code contributions

## Project Status

**Current Version:** 0.1.0 (Initial Release)
**Status:** Production Ready ✅
**Maintenance:** Actively maintained
**Stability:** Stable

## Acknowledgments

- **Textual** - Amazing TUI framework by Textualize
- **Anki** - Inspiration for spaced repetition implementation
- **SuperMemo** - Original SM-2 algorithm research
- **Python Community** - Excellent tools and libraries

---

*Built with ❤️ for learners everywhere*
*Last Updated: November 2025*
