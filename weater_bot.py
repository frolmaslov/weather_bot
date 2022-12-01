import pytz
import datetime
from timezonefinder import TimezoneFinder


def time_now(ln, lt):
    tf = TimezoneFinder(in_memory=True)
    timezone = tf.timezone_at(lng=ln, lat=lt)
    now_t = datetime.datetime.now(pytz.timezone(timezone))
    return [timezone, now_t.strftime('%H:%M')]










