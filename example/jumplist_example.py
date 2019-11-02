from fortools import *

file = JumpList.file_open('path')

# show information from destlist
access_cnt = file.access_count()
recent_time = file.recent_time()
print("cnt: " + str(access_cnt))
print("last access time: " + str(recent_time))

# show information about jumplist lnk
file.show_info()
