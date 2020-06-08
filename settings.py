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

# Cache Settings
cache_path = 'cache'

# Other Settings
refresh_after_seconds = 30