from datetime import datetime, timedelta, timezone


def set_timezone(timezone):
    time_split = timezone.split(':')
    minutestime=int(time_split[0])*60+int(time_split[1])
    global mintz
    mintz = minutestime


def __convert_time(int_time):
    if type(int_time) == int:
        int_time = int_time * 0.1
    else:
        int_time = '%016x' % int_time
        int_time = int(int_time, 16) * 0.1

    date_time = datetime(1601, 1, 1, tzinfo=timezone(timedelta(minutes=mintz))) + timedelta(microseconds=int_time) + timedelta(minutes=mintz)
    return date_time


def convert_time_ie_edge_chrome(int_time):
    try:
        int_time = int_time / 10.
        int_time = datetime(1601, 1, 1, tzinfo=timezone(timedelta(minutes=mintz))) + timedelta(microseconds=int_time) + timedelta(minutes=mintz)
        return int_time
    except:
        return 0
