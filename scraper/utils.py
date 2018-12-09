from functools import singledispatch
from datetime import datetime

@singledispatch
def to_serializable(val):
    return str(val)

@to_serializable.register(datetime)
def ts_datetime(val):
    return val.isoformat() + "Z"
