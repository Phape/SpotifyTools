# Phapes Spotify Tools

A Website that uses the Spotify API to get additional information for your favourite songs on Spotify.

## Links

These Links should help you understandig this project and help you to get to relevant websites quickly.

### Project Links

* [Website](https://spotifytools.azurewebsites.net/)
* [Azure Portal](https://portal.azure.com/)
* [GitHub Repo](https://github.com/Phape/SpotifyTools)

### Read The Docs

* [Flask](https://flask.palletsprojects.com)
* [spotipy](https://spotipy.readthedocs.io)
* [Flask-Session](https://flask-session.readthedocs.io)

## How to set up the project locally

1. Clone the repository from GitHub
2. Create a virtual environment with `python -m venv venv`
3. From that environment, install the requirements from [requirements.txt](requirements.txt)
   1. Example in VS Code: after step 2, in the bottom left corner or via VS Code Command, change your python interpreter to the one with 'venv' in its name
   2. with the VS Code Command 'Terminal: Create New Integrated Terminal', create a new terminal for your virtual environment
   3. Install the requirements from that terminal
4. Set the environment Variables: If you chose to work with VS Code and use PowerShell as your Terminal, you can set the environment variables by modifying the [Activate.ps1](venv/Scripts/Activate.ps1) Skript. If you don't use PS, just adapt the [activate (bash)](venv/Scripts/activate) or [activate.bat (cmd)](venv/Scripts/activate.bat). I suggest setting the environment variables after the "VIRTUAL_ENV" Variable has been set (l. 215). It could look like this:

    ```powershell
    # Environment Variables for the SpotifyTools app
    $env:SPOTIPY_CLIENT_ID = "your_client_id_here"
    $env:SPOTIPY_CLIENT_SECRET = "your_client_secret_here"
    $env:SPOTIPY_REDIRECT_URI = "http://127.0.0.1:5000"
    $env:REDIS_HOST = "your.redis.host.here"
    $env:REDIS_PASSWORD = "your_redis_password_here"
    ```
