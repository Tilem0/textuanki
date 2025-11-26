# TextuAnki - Feature Overview

A comprehensive guide to all features in TextuAnki.

## Dashboard

The main hub of TextuAnki showing:

### Statistics Display
- **Cards Due**: Number of cards ready to review right now
- **Total Cards**: Your complete collection size
- **Total Decks**: Number of decks you've created

### Quick Actions
- Study Cards
- Create New Card  
- Browse Cards
- Manage Decks

### Keyboard Shortcuts
- `S` - Start studying
- `N` - Create new card
- `B` - Browse all cards
- `D` - Manage decks
- `Ctrl+Q` - Quit application

---

## Study Mode

The heart of TextuAnki - where learning happens!

### How It Works
1. Shows you the front of a card (question)
2. Press `Space` to reveal the answer
3. Rate how well you remembered:
   - **1 - Again**: Completely forgot, see it again soon
   - **2 - Hard**: Struggled to remember
   - **3 - Good**: Remembered correctly
   - **4 - Easy**: Very easy, can wait longer

### Spaced Repetition (SM-2 Algorithm)
- **New cards**: Start with 1-day intervals
- **Easy cards**: Intervals grow exponentially
- **Difficult cards**: Intervals shrink
- **Forgotten cards**: Reset to learning phase

### Features
- Progress indicator (Card X of Y)
- Clean, distraction-free interface
- Keyboard-only operation
- Automatic due date calculation
- Review history tracking

### Tips
- Be honest with ratings - it helps the algorithm
- Don't overthink - quick ratings work best
- Study daily for best results
- Short sessions (5-15 min) are effective

---

## Card Creation

Simple, keyboard-focused form for adding flashcards.

### Fields
1. **Deck**: Select which deck to add to (required)
2. **Front**: The question or prompt (required)
3. **Back**: The answer or content (required)
4. **Tags**: Comma-separated keywords (optional)

### Keyboard Navigation
- `Tab` - Move between fields
- `Ctrl+S` - Save card
- `Esc` - Cancel and return

### Best Practices
- **Keep it simple**: One fact per card
- **Be specific**: Clear, unambiguous questions
- **Use tags**: Organize by topic or chapter
- **Front first**: Write the question before the answer

### Examples of Good Cards

**Good**:
```
Front: What is the capital of France?
Back: Paris
Tags: geography, europe, capitals
```

**Better** (more specific):
```
Front: In Python, what does the len() function return?
Back: The number of items in an object (like a list or string)
Tags: python, functions, basics
```

---

## Browse Cards

View and manage your entire card collection.

### Features
- Table view with all cards
- Shows: ID, Deck, Front, Back, Tags
- Arrow key navigation
- Quick delete functionality

### Keyboard Shortcuts
- `↑`/`↓` - Navigate rows
- `D` - Delete selected card
- `Esc` - Return to dashboard

### Use Cases
- Find specific cards
- Review your collection
- Delete outdated cards
- Check for duplicates

---

## Deck Manager

Organize your cards into collections.

### Features
- View all decks with card counts
- Create new decks
- Delete decks (except Default)
- See deck statistics

### Creating a Deck
1. Press `N` or click "New Deck"
2. Enter deck name (required)
3. Enter description (optional)
4. Press "Create"

### Keyboard Shortcuts
- `N` - Create new deck
- `D` - Delete selected deck
- `↑`/`↓` - Navigate decks
- `Esc` - Return to dashboard

### Deck Ideas
- **By Subject**: Spanish, Python, History
- **By Level**: Beginner, Intermediate, Advanced
- **By Source**: Textbook Ch1, Course Week 3
- **By Goal**: Exam Prep, Daily Practice

---

## Tag System

Organize cards with flexible keyword tags.

### How to Use Tags
- Add during card creation
- Comma-separated list
- Use for filtering (future feature)
- Multiple tags per card

### Tag Examples
- **Level**: `basics`, `intermediate`, `advanced`
- **Topic**: `vocabulary`, `grammar`, `pronunciation`
- **Priority**: `important`, `exam`, `review`
- **Source**: `chapter1`, `lecture3`, `textbook`

### Best Practices
- Use consistent naming
- Keep tags short
- Don't over-tag (3-5 per card)
- Plan your tag system early

---

## Keyboard Shortcuts Reference

### Global (Available Everywhere)
| Shortcut | Action |
|----------|--------|
| `Ctrl+Q` | Quit application |
| `Ctrl+D` | Toggle dark mode |
| `Ctrl+H` | Return to dashboard |
| `Ctrl+N` | Create new card |
| `Ctrl+S` | Start studying |
| `Ctrl+B` | Browse cards |
| `Esc` | Go back / Cancel |

### Dashboard
| Shortcut | Action |
|----------|--------|
| `S` | Study cards |
| `N` | New card |
| `B` | Browse cards |
| `D` | Manage decks |

### Study Mode
| Shortcut | Action |
|----------|--------|
| `Space` | Reveal answer |
| `1` | Rate: Again |
| `2` | Rate: Hard |
| `3` | Rate: Good |
| `4` | Rate: Easy |
| `Esc` | Exit study |

### Browse/Manage
| Shortcut | Action |
|----------|--------|
| `↑`/`↓` | Navigate |
| `D` | Delete |
| `N` | New (in deck manager) |
| `Esc` | Go back |

---

## Data & Privacy

### Storage
- **Location**: `~/.textuanki/cards.db`
- **Format**: SQLite database
- **Privacy**: 100% local, never leaves your computer

### Backup
```bash
# Backup your cards
cp ~/.textuanki/cards.db ~/backups/cards_$(date +%Y%m%d).db

# Restore from backup
cp ~/backups/cards_20231126.db ~/.textuanki/cards.db
```

### Export (Future)
- Coming soon: Export to Anki .apkg format
- Transfer between computers
- Share decks with others

---

## Study Tips

### Daily Practice
- **Consistency > Duration**: 10 min daily beats 1 hr weekly
- **Morning study**: When your mind is fresh
- **Before bed**: Good for memory consolidation

### Creating Good Cards
- **Atomic**: One concept per card
- **Clear**: No ambiguity in questions
- **Memorable**: Use mnemonics or stories
- **Connected**: Link to existing knowledge

### Using the System
- **Trust the algorithm**: Don't manually review
- **Be honest**: Accurate ratings = better scheduling
- **Don't cram**: Spaced repetition needs time
- **Regular reviews**: Check due cards daily

### Dealing with Difficult Cards
- **Break down**: Split complex cards into simpler ones
- **Add context**: More detail in the answer
- **Use mnemonics**: Create memory aids
- **Suspend**: Remove cards that aren't working

---

## Technical Details

### Spaced Repetition (SM-2)

The SM-2 algorithm adjusts card intervals based on your performance:

```
Initial interval: 1 day
Second interval: 6 days  
Subsequent: interval × ease_factor

Ease factor:
- Starts at 2.5
- Increases with "Easy" ratings
- Decreases with "Again" ratings
- Minimum: 1.3
```

### Rating Impact
- **Again (1)**: Reset to 1 day, reduce ease
- **Hard (2)**: Shorter interval, slightly reduce ease
- **Good (3)**: Standard interval, maintain ease
- **Easy (4)**: Longer interval, increase ease

### Database Schema
```sql
- decks: id, name, description
- cards: id, deck_id, front, back, tags
- reviews: card_id, ease_factor, interval, due_date
- study_sessions: card_id, rating, reviewed_at
```

---

## Workflow Examples

### Learning a New Language
1. Create deck: "Spanish - Basic Vocabulary"
2. Add 10 words per day
3. Study daily (10-15 minutes)
4. Add more as you progress
5. Use tags for word types

### Studying for an Exam
1. Create deck: "Biology 101 - Exam 2"
2. Add cards while studying
3. Tag by chapter or topic
4. Review cards before exam
5. Keep studying after exam for retention

### Professional Development
1. Create deck: "Python - Interview Prep"
2. Add common interview questions
3. Study during commute
4. Add real interview questions
5. Review before interviews

---

## Troubleshooting

### No Cards Due?
- Create new cards - they're immediately due
- Wait for existing cards to become due
- Check if you have any cards at all

### Can't Delete a Deck?
- Can't delete "Default" deck
- Must select a deck first
- Deck must exist

### App Crashes?
- Check database isn't corrupted
- Try: `rm ~/.textuanki/cards.db` and restart
- Report bugs with error message

### Keyboard Shortcuts Not Working?
- Make sure app has focus
- Some shortcuts are screen-specific
- Check footer for available shortcuts

---

## Future Features

### Planned
- [ ] Import/Export Anki decks
- [ ] Advanced statistics dashboard
- [ ] Card editing
- [ ] Search and filter
- [ ] Multiple card types
- [ ] Image support

### Ideas Welcome!
Have a feature request? Let us know!

---

*Happy studying! 📚*
