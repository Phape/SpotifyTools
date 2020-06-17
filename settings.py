import os
import redis
import datetime

# Flask Settings
SECRET_KEY = os.urandom(64)
SESSION_TYPE = 'redis'
session_permanent = False
permanent_session_lifetime = datetime.timedelta(days=30) #becomes effective when session_permanent is True

# Redis Settings
SESSION_REDIS = redis.Redis(
    host = os.environ.get('REDIS_HOST'),
    port=6380, 
    db=0,
    password = os.environ.get('REDIS_PASSWORD'),
    ssl=True)

# App Settings
scopes = 'user-read-currently-playing user-top-read user-read-recently-played'

cache_path = 'cache'
refresh_after_seconds = 30