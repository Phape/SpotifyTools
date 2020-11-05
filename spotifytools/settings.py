import os
import redis
import datetime

# Flask Settings
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') # generate one with os.urandom(24) and set as environment variable
SESSION_TYPE = 'filesystem' # redis would be preferred
SQLALCHEMY_DATABASE_URI = 'sqlite:///spotifytools.db'
session_permanent = False
permanent_session_lifetime = datetime.timedelta(days=30) #becomes effective when session_permanent is True

# Genius Settings
GENIUS_ACCESS_TOKEN = os.environ.get('GENIUS_CLIENT_ACCESS_TOKEN')

# Redis Settings (currently not used)
SESSION_REDIS = redis.Redis(
    host = os.environ.get('REDIS_HOST'),
    port=6379, 
    db=0,
    password = os.environ.get('REDIS_PASSWORD'),
    ssl=True)

# App Settings
scopes = 'user-read-currently-playing user-top-read user-read-recently-played'

cache_path = 'cache'
refresh_after_seconds = 30
