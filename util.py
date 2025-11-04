import pytz
import datetime
import time
import uuid
import functools
import logging

log = logging.getLogger("util")

tz_hki = pytz.timezone("Europe/Helsinki")
tz_utc = pytz.utc

def utc2local(utc_dt, tz=tz_hki):
    if not utc_dt:
        return utc_dt
    d = utc_dt.replace(tzinfo=tz_utc)
    return d.astimezone(tz)

def local2utc(local_dt, tz=tz_hki):
    if not local_dt:
        return local_dt
    d = local_dt.replace(tzinfo=tz)
    return d.astimezone(tz_utc)

def utcnow():
    return datetime.datetime.utcnow()

def generate_token():
    return uuid.uuid4().hex

def timeit(f):
    @functools.wraps(f)
    def wrap(*args, **kw):
        t1 = time.time()
        result = f(*args, **kw)
        t2 = time.time()
        log.info("%r args:[%r, %r] took: %2.4f sec" % \
          (f.__name__, args, kw, t2-t1))
        return result
    return wrap