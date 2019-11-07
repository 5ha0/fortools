from fortools import *

file = Prefetch.file_open('path')

# show information from prefetch file
name = file.file_name()
l_time = file.last_run_time()
c_time = file.create_time()
w_time = file.write_time()
launch = file.num_launch()
file_list = file.file_list()
