import datetime
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(
    dotenv_path=os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"
    )
)

# Flask Settings
# generate one with os.urandom(24) and set as environment variable
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
SESSION_TYPE = "filesystem"
SESSION_PERMANENT = False
# becomes effective when SESSION_PERMANENT is True
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)

# Flask Environment Settings
ENV = os.environ.get("FLASK_ENV", "production")
DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")
HOST = os.environ.get("FLASK_HOST", "127.0.0.1")
PORT = int(os.environ.get("FLASK_PORT", "5000"))

# Genius Settings
GENIUS_ACCESS_TOKEN = os.environ.get("GENIUS_CLIENT_ACCESS_TOKEN")

# App Settings
SCOPES = "user-read-currently-playing user-top-read user-read-recently-played"
CACHE_PATH = "cache"
REFRESH_AFTER_SECONDS = 30
