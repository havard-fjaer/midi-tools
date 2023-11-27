#!/bin/sh

# stop script
if [ "$1" = "stop" ]
then
    echo "Stopping script..."
    kill $(pgrep -f mix_es9_from_korg.py)
    exit 0
fi

if pgrep -f mix_es9_from_korg.py > /dev/null
then
    echo "Script already running with PID $(pgrep -f mix_es9_from_korg.py)"
else
    echo "Starting script..."
    python3 mix_es9_from_korg.py &
fi
