import os
import redis
import datetime

# Flask Settings
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') # generate one with os.urandom(24) and set as environment variable
SESSION_TYPE = 'filesystem' # redis would be preferred
session_permanent = False
permanent_session_lifetime = datetime.timedelta(days=30) #becomes effective when session_permanent is True

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

# Dicts
time_range_dict = {
    "short_term": "last 4 weeks",
    "medium_term": "last 6 months",
    "long_term": "total"
}