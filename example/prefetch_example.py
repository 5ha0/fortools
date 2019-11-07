from fortools import *

file = Prefetch.file_open(r'C:\Windows\Prefetch\IEXPLORE.EXE-A033F7A2.pf')
# Or you ca use this
# path = 'path'
# file = file_open(path)

# show information about prefetch file
name = file.file_name()
l_time = file.last_run_time()
c_time = file.create_time()
w_time = file.write_time()
launch = file.num_launch()
file_list = file.file_list()

# show information from show_all_info()
file_list = file.file_list()
