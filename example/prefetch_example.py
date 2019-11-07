from fortools import *

path = 'C:\\Windows\\Prefetch\\CHROME.EXE-5349D2D7.pf'
file = Prefetch.file_open(path)

# show information from prefetch file
name = file.file_name()
l_time = file.last_run_time()
c_time = file.create_time(path)
w_time = file.write_time(path)
launch = file.num_launch()
file_list = file.file_list()