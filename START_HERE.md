# 🎉 Welcome to TextuAnki!

Your beautiful, terminal-based flashcard app is ready to use!

## ⚡ Quick Start (30 seconds)

```bash
# Just run this:
./run.sh
```

That's it! The app will launch with 24 sample flashcards ready to study.

## 📚 What You Can Do Right Now

1. **Study** - Press `S` to start reviewing cards
2. **Create** - Press `N` to add your own flashcards  
3. **Browse** - Press `B` to see all your cards
4. **Organize** - Press `D` to manage decks

## 🎯 First Steps

### Try the Sample Cards
We've loaded 24 flashcards across 3 decks:
- **Default** (4 cards) - General knowledge
- **Spanish Vocabulary** (10 cards) - Basic Spanish
- **Python Programming** (10 cards) - Python concepts

### Study Your First Card
1. Press `S` to start studying
2. Read the question
3. Press `Space` to see the answer
4. Rate yourself (1-4)
5. Repeat!

### Create Your First Card
1. Press `N` for new card
2. Select a deck
3. Write your question
4. Write your answer
5. Press `Ctrl+S` to save

## 📖 Documentation

- **QUICKSTART.md** - Detailed getting started guide
- **FEATURES.md** - Complete feature reference
- **DEMO.md** - Visual interface tour
- **README.md** - Full documentation
- **PROJECT_STATUS.md** - Technical overview

## ⌨️ Essential Shortcuts

```
Ctrl+Q  → Quit
Ctrl+H  → Home (Dashboard)
Ctrl+N  → New Card
Ctrl+S  → Study
Ctrl+B  → Browse
Esc     → Go Back
```

## 🧠 How Spaced Repetition Works

TextuAnki uses the proven SM-2 algorithm:

1. **New cards** start with short intervals (1 day)
2. **Easy cards** get longer intervals (exponentially)
3. **Hard cards** get shorter intervals
4. **Forgotten cards** restart from the beginning

The more you correctly recall a card, the less often you'll see it!

## 💡 Pro Tips

- **Study daily** - Even 5-10 minutes helps
- **Be honest** - Accurate ratings = better learning
- **Keep cards simple** - One fact per card
- **Use tags** - Organize your cards
- **Trust the system** - Don't manually review

## 🗂️ Your Data

All your flashcards are stored locally at:
```
~/.textuanki/cards.db
```

- 100% private (never leaves your computer)
- Easy to backup (just copy the file)
- Portable (copy to another machine)

## 🆘 Need Help?

### App won't start?
```bash
rm -rf venv
./run.sh
```

### Want fresh sample data?
```bash
source venv/bin/activate
python add_sample_data.py
```

### Want to reset everything?
```bash
rm -rf ~/.textuanki/
./run.sh
```

## 📊 Project Stats

```
✅ Complete & Working
- 5 screens fully functional
- Full CRUD for cards & decks
- Spaced repetition system
- Beautiful TUI interface
- Keyboard-first design
- 24 sample cards included
```

## 🎨 What Makes TextuAnki Special?

✨ **Clean & Simple** - No clutter, just cards  
⚡ **Fast** - Keyboard-driven workflow  
🧠 **Smart** - Spaced repetition built-in  
🔒 **Private** - All data stays local  
💻 **Terminal-Native** - Works over SSH  
🎯 **Focused** - Does one thing really well  

## 🚀 Your Learning Journey Starts Now

1. **Today**: Study the sample cards (10 minutes)
2. **Tomorrow**: Create your first deck
3. **This week**: Add 5-10 cards daily
4. **This month**: Build a study habit
5. **This year**: Master any topic!

## 📈 Success Tips

**Week 1**: Use sample cards, get comfortable with interface  
**Week 2**: Create your first custom deck (10-20 cards)  
**Week 3**: Study daily, add cards regularly  
**Week 4**: You're now a TextuAnki pro! 🎓  

## 🎮 Challenge Yourself

- [ ] Study all 24 sample cards
- [ ] Create your own deck
- [ ] Add 10 cards on a topic you're learning
- [ ] Study for 7 days in a row
- [ ] Reach 100 total cards
- [ ] Master a new skill!

## 🤝 Feedback & Contributions

Love TextuAnki? Have ideas? Found a bug?

This is a passion project built to help people learn better. Your feedback makes it better!

## 📜 The TextuAnki Promise

✅ Always free  
✅ Always open source  
✅ Always local-first  
✅ Always keyboard-friendly  
✅ Always focused on learning  

## 🎊 Ready? Let's Go!

```bash
./run.sh
```

Press `S` to start your learning journey!

---

**Remember**: Consistency beats intensity. Study a little every day! 📚

Happy learning! 🎉

---

*Built with ❤️ for learners everywhere*  
*Version 0.1.0 | November 2025*
