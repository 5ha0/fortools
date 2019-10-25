from fortools import *


event_log_file = file_open('C:\\Windows\\System32\\winevt\\Logs\\Security.evtx')
# event_log_file.show_all_record()
# event_log_file.date('2019-10-21')
event_log_file.favorite.logon()

'''
# file_open('.\\data\\IMG_0111.jpg')
file = file_open('.\\data\\1.hwp')
file.showlist()
'''
