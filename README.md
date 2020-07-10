# Phapes Spotify Tools

A Website that uses the Spotify API to get additional information for your favorite songs on Spotify.

## Links

These Links should help you understandig this project and help you to get to relevant websites quickly.

### Project Links

* [Website](https://spotifytools.phape.de/)
* [Azure Portal](https://portal.azure.com/)
* [GitHub Repo](https://github.com/Phape/SpotifyTools)

### Docs & CheatSheets

* [Flask](https://flask.palletsprojects.com)
* [spotipy](https://spotipy.readthedocs.io)
* [Flask-Session](https://flask-session.readthedocs.io)
* [redis in python](https://docs.redislabs.com/latest/rs/references/client_references/client_python/)
* [markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

## How to set up the project locally

If you're using VS Code and new to Flask, I recommend reading the [Flask Tutorial in Visual Studio Code](https://code.visualstudio.com/docs/python/tutorial-flask). It can help with step 2 and 3 of the following list.

1. Clone the repository from GitHub
2. Create a virtual environment with `python -m venv venv`
3. From that environment, install the requirements from [requirements.txt](requirements.txt)
   1. Example in VS Code: after step 2, in the bottom left corner or via VS Code Command, change your python interpreter to the one with 'venv' in its name
   2. with the VS Code Command 'Terminal: Create New Integrated Terminal', create a new terminal for your virtual environment
   3. Install the requirements from that terminal
4. Set the environment Variables: If you chose to work with VS Code and use PowerShell as your Terminal, you can set the environment variables by modifying the [Activate.ps1](venv/Scripts/Activate.ps1) Skript. If you don't use PS, just adapt the [activate (bash)](venv/Scripts/activate) or [activate.bat (cmd)](venv/Scripts/activate.bat). I suggest setting the environment variables after the "VIRTUAL_ENV" Variable has been set (l. 215). It could look like this:

    ```powershell
    # Environment Variables for the SpotifyTools app
    $env:FLASK_SECRET_KEY="your_secret_key_generated_with_os.urandom(24)"
    $env:SPOTIPY_CLIENT_ID="your_spotify_client_id_here"
    $env:SPOTIPY_CLIENT_SECRET="your_spotify_client_secret_here"
    $env:SPOTIPY_REDIRECT_URI="http://127.0.0.1:5000"
    $env:REDIS_HOST="your.redis.host.here"
    $env:REDIS_PASSWORD="your_redis_password_here"
    # The following lines are only for the development environment (debugging)
    $env:FLASK_ENV="development"
    $env:FLASK_DEBUG="True"
    ```
