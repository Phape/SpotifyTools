#!/bin/sh
# make executable with: chmod +x run_spotify_tools_server.sh

echo 'starting SpotifyTools'
git pull
source venv/bin/activate
pip3 install -r requirements.txt
gunicorn -b localhost:8000 -w 4 app:app
