"""Entry point for TextuAnki application."""
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.app import TextuAnkiApp


def main():
    """Run the TextuAnki application."""
    app = TextuAnkiApp()
    app.run()


if __name__ == "__main__":
    main()
