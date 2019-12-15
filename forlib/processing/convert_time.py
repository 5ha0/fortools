from datetime import datetime, timedelta

class TimeZone:

    def __init__(self,time_zone):
        self.__time_split = time_zone
        self.__time_split = self.__time_split.split(':')
        self.__time_split = int(self.__time_split)

    def __convert_time(self, int_time):
        if type(int_time) == int:
            int_time = int_time * 0.1
        else:
            int_time = '%016x' % int_time
            int_time = int(int_time, 16) * 0.1
            
        date_time = datetime(1601, 1, 1) + timedelta(microseconds=int_time + timedelta(hours=time_zone[0], minutes=time_split[1]))
        return date_time
