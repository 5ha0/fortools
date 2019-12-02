from datetime import datetime, timedelta


def convert_time(time):
    time = '%016x' % time
    time = int(time, 16) / 10.
    time = datetime(1601, 1, 1) + timedelta(microseconds=time)
    return time
