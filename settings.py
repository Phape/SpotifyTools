import os
import redis

# Flask Settings
SECRET_KEY = os.urandom(64)
SESSION_TYPE = 'redis'

# Redis Settings
SESSION_REDIS = redis.Redis(
    host = os.environ.get('REDIS_HOST'),
    port=6380, 
    db=0,
    password = os.environ.get('REDIS_PASSWORD'),
    ssl=True)

# App Settings
scopes = 'user-read-currently-playing user-top-read'

cache_path = 'cache'
refresh_after_seconds = 30