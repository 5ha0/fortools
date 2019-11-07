from fortools import *

file = Recycle.file_open('path')

# show information from $I recycle file
header = file.r_header()
size = file.r_size()
time = file.r_time()
path = file.r_path()
