import os
import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), '.env'))

# Flask Settings
# generate one with os.urandom(24) and set as environment variable
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
SESSION_TYPE = 'filesystem'
session_permanent = False
# becomes effective when session_permanent is True
permanent_session_lifetime = datetime.timedelta(days=30)

# Genius Settings
GENIUS_ACCESS_TOKEN = os.environ.get('GENIUS_CLIENT_ACCESS_TOKEN')

# App Settings
scopes = 'user-read-currently-playing user-top-read user-read-recently-played'

cache_path = 'cache'
refresh_after_seconds = 30
