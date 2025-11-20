#!/usr/bin/env bash

set -e

VENV_DIR="venv"

if [ ! -d "$VENV_DIR" ]; then
    echo ">>> Making virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

echo ">>> Activating environment..."
source "$VENV_DIR/bin/activate"

if [ -f "requirements.txt" ]; then
    echo ">>> Installing requirements..."
    pip install -r requirements.txt
fi

echo ">>> Running app..."
python run.py

echo ">>> Bye!"

deactivate 2>/dev/null || true

