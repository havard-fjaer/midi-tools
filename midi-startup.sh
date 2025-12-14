#!/bin/sh

# stop script
if [ "$1" = "stop" ]
then
    echo "Stopping script..."
    kill $(pgrep -f mix_es9_from_korg.py)
    exit 0
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: python3 is not installed"
    exit 1
fi

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
    echo "Virtual environment created"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Check if required Python packages are installed
echo "Checking dependencies..."
if ! python -c "import mido" 2>/dev/null
then
    echo "Installing required Python packages..."
    pip install -r "$SCRIPT_DIR/requirements.txt"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
    echo "Dependencies installed successfully"
else
    echo "All dependencies are present"
fi

if pgrep -f mix_es9_from_korg.py > /dev/null
then
    echo "Script already running with PID $(pgrep -f mix_es9_from_korg.py)"
else
    echo "Starting script..."
    python "$SCRIPT_DIR/mix_es9_from_korg.py" &
fi
