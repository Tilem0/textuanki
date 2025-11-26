"""ASCII banners and typography for brutalist design."""

# Main logo banner
TEXTUANKI_BANNER = """
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║  ████████╗███████╗██╗  ██╗████████╗██╗   ██╗ █████╗ ███╗   ██╗██╗║
║  ╚══██╔══╝██╔════╝╚██╗██╔╝╚══██╔══╝██║   ██║██╔══██╗████╗  ██║██║║
║     ██║   █████╗   ╚███╔╝    ██║   ██║   ██║███████║██╔██╗ ██║██║║
║     ██║   ██╔══╝   ██╔██╗    ██║   ██║   ██║██╔══██║██║╚██╗██║██║║
║     ██║   ███████╗██╔╝ ██╗   ██║   ╚██████╔╝██║  ██║██║ ╚████║██║║
║     ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝║
║                                                                    ║
║                        記憶・学習・成長                              ║
║                    MEMORY・LEARNING・GROWTH                         ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
"""

STUDY_BANNER = """
╔══════════════════════════════════════════════════════════════════╗
║                         学習モード                                 ║
║                       STUDY  MODE                                ║
╚══════════════════════════════════════════════════════════════════╝
"""

CREATE_BANNER = """
╔══════════════════════════════════════════════════════════════════╗
║                         作成モード                                 ║
║                      CREATE  CARD                                ║
╚══════════════════════════════════════════════════════════════════╝
"""

BROWSE_BANNER = """
╔══════════════════════════════════════════════════════════════════╗
║                         閲覧モード                                 ║
║                      BROWSE  CARDS                               ║
╚══════════════════════════════════════════════════════════════════╝
"""

DECK_BANNER = """
╔══════════════════════════════════════════════════════════════════╗
║                         管理モード                                 ║
║                      DECK  MANAGER                               ║
╚══════════════════════════════════════════════════════════════════╝
"""

# Kanji decorations
KANJI = {
    "study": "学",
    "card": "札",
    "deck": "束",
    "new": "新",
    "review": "復",
    "memory": "記",
    "learn": "習",
    "knowledge": "識",
    "question": "問",
    "answer": "答",
    "due": "期",
    "total": "全",
}

# Box drawing characters for brutalist borders
BOX_HEAVY = {
    "tl": "┏", "tr": "┓", "bl": "┗", "br": "┛",
    "h": "━", "v": "┃", "cross": "╋",
    "t_down": "┳", "t_up": "┻", "t_right": "┣", "t_left": "┫"
}

BOX_DOUBLE = {
    "tl": "╔", "tr": "╗", "bl": "╚", "br": "╝",
    "h": "═", "v": "║", "cross": "╬",
    "t_down": "╦", "t_up": "╩", "t_right": "╠", "t_left": "╣"
}

BOX_LIGHT = {
    "tl": "┌", "tr": "┐", "bl": "└", "br": "┘",
    "h": "─", "v": "│", "cross": "┼",
    "t_down": "┬", "t_up": "┴", "t_right": "├", "t_left": "┤"
}

def create_box(text: str, width: int = 70, style: str = "double") -> str:
    """Create a bordered box with text."""
    box = BOX_DOUBLE if style == "double" else BOX_HEAVY if style == "heavy" else BOX_LIGHT
    
    lines = text.split("\n")
    result = []
    
    # Top border
    result.append(box["tl"] + box["h"] * (width - 2) + box["tr"])
    
    # Content
    for line in lines:
        padding = width - len(line) - 4
        result.append(box["v"] + " " + line + " " * padding + " " + box["v"])
    
    # Bottom border
    result.append(box["bl"] + box["h"] * (width - 2) + box["br"])
    
    return "\n".join(result)

def smallcaps(text: str) -> str:
    """Convert text to smallcaps aesthetic."""
    caps_map = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ',
        'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ',
        'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ',
        'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ'
    }
    return ''.join(caps_map.get(c.lower(), c) for c in text)
