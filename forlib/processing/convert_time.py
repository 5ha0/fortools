from datetime import datetime, timedelta, timezone

mintz = 0

def set_timezone(timezone):
    time_split = timezone.split(':')
    minutestime=int(time_split[0])*60+int(time_split[1])
    global mintz
    mintz = minutestime
    
    
def get_timezone():
    return mintz


def convert_time(int_time):
    if type(int_time) == int:
        int_time = int_time * 0.1
    else:
        int_time = '%016x' % int_time
        int_time = int(int_time, 16) * 0.1

    if int_time ==0:
        date_time = datetime(1601, 1, 1, tzinfo=timezone(timedelta(minutes=mintz)))
    else:
        date_time = datetime(1601, 1, 1, tzinfo=timezone(timedelta(minutes=mintz))) + timedelta(microseconds=int_time) + timedelta(minutes=mintz)
    return date_time


def convert_time_chrome(int_time):
    if int_time == 0:
        date_time = datetime(1601, 1, 1, tzinfo=timezone(timedelta(minutes=mintz)))
    else:
        date_time = datetime(1601, 1, 1, tzinfo=timezone(timedelta(minutes=mintz))) + timedelta(microseconds=int_time) + timedelta(minutes=mintz)
    return date_time


def convert_time_firefox1(int_time):
    int_time = datetime.fromtimestamp(int_time / 1000000)
    date_time = int_time.replace(tzinfo=timezone(timedelta(minutes=mintz))) + timedelta(minutes=mintz)
    return date_time


def convert_time_firefox2(int_time):
    int_time = datetime.fromtimestamp(int_time/1000)
    date_time = int_time.replace(tzinfo=timezone(timedelta(minutes=mintz))) + timedelta(minutes=mintz)
    return date_time


def convert_time_firefox3(int_time):
    int_time = datetime.fromtimestamp(int_time)
    date_time = int_time.replace(tzinfo=timezone(timedelta(minutes=mintz))) + timedelta(minutes=mintz)
    return date_time


def convert_replace_time(int_time):
    int_time = int_time.replace(tzinfo=timezone(timedelta(minutes=mintz)))
    int_time = int_time + timedelta(minutes=mintz)
    return int_time
