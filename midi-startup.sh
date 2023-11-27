#!/bin/sh
if pgrep -f mix_es9_from_korg.py > /dev/null
then
    echo "Script already running."
else
    echo "Starting script..."
    python3 mix_es9_from_korg.py
fi
