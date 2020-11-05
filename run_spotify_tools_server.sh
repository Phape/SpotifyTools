#!/bin/bash
# make executable with: chmod +x run_spotify_tools_server.sh

echo 'starting SpotifyTools'
git pull
source venv/bin/activate
pip3 install -r requirements.txt

# start gunicorn if not already running
SERVICE="gunicorn"
if pgrep -x "$SERVICE" >/dev/null
then
    echo "$SERVICE is already running, stopping, then restarting it"
    pkill $service
    $SERVICE -b localhost:8000 -w 4 run:app
else
    echo "starting $SERVICE"
    $SERVICE -b localhost:8000 -w 4 run:app
fi