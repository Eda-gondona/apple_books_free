import os
import time

# Базовые настройки
IS_PRODUCTION = False
IS_LOCAL_DEV = True
IS_SQLITE = False

# Database
DATABASE_HOST = "localhost"
DATABASE_PORT = 5432
DATABASE_NAME = "booklibrary"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "password"

# Redis
redishost = "localhost"

# Flask config
flask_config = {
    'SECRET_KEY': 'dev-secret-key-123',
    'SESSION_COOKIE_NAME': 'mycookie',
    'SESSION_COOKIE_HTTPONLY': True,
    'PERMANENT_SESSION_LIFETIME': 60*60*24*30
}

CORS_ALLOW_ORIGIN = '*'
PYSRV_LOG_SQL = False

START_TIME = int(time.time())

def started_ago(as_string=False):
    ago = int(time.time()) - START_TIME
    if as_string:
        return "{}d {:02d}:{:02d}:{:02d}".format(int(ago/60/60/24),
                int(ago/60/60)%24, int(ago/60)%60, ago%60)
    else:
        return ago