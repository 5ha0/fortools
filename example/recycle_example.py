from fortools import *

file = Recycle.file_open('D:\\CFReDS\\DiskImage\\$I30')
# Or you ca use this
# path = 'path'
# file = file_open(path)

# show each information about recycle $I file
name = file.i_name()
header = file.header()
size = file.size()
time = file.time()
path = file.path()

# show all information about recycle $I file
result = file.show_all_info()
