import logging

log = logging.getLogger("cache")

# Временная заглушка для Redis
cache = {}

def set_keyval(key, val, expiration_secs=0):
    try:
        cache[key] = val
    except:
        log.error("cache set_keyval %s", key)

def get_keyval(key, default=None):
    try:
        return cache.get(key, default)
    except:
        log.error("cache get_keyval %s")
        return default

def delete_key(key):
    try:
        if key in cache:
            del cache[key]
    except:
        log.error("cache del %s", key)

def incr(name, num=1):
    current = cache.get(name, 0)
    new_value = current + num
    cache[name] = new_value
    return new_value

# Остальные функции можно временно оставить пустыми
def list_append(name, item, max_size=None):
    pass

def list_pop(name, timeout=None):
    return None

def list_peek(name):
    return None

def list_fetch(name):
    return []

def list_length(name):
    return 0

def get_set(key, val):
    old = cache.get(key)
    cache[key] = val
    return old