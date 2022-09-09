"""
Filter functions/methods for date/time formatting
"""
import datetime

"""
Function to convert UNIX timestamps to Python date-time objects
"""
def unix2datetime(unix_time):
    return datetime.datetime.fromtimestamp(unix_time)

"""
Function to convert seconds to human-readable delta
"""
def seconds2delta(seconds):
    return datetime.timedelta(seconds=seconds)
