from datetime import datetime, timedelta


def convert_time(int_time):
    int_time = '%016x' % int_time
    int_time = int(int_time, 16) *0.1
    int_time = datetime(1601, 1, 1) + timedelta(microseconds=int_time)
    return int_time

def convert_bin_time(int_time):
    int_time = int_time*0.1
    if int_time == 0:
        date_time = 'Never'
    else:
        date_time = datetime(1601, 1, 1) + timedelta(microseconds=int_time)
        date_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
    return date_time
    
    
