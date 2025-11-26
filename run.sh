#!/bin/bash
# Convenience script to run TextuAnki

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip setuptools wheel
    pip install textual genanki
else
    source venv/bin/activate
fi

python src/main.py "$@"
