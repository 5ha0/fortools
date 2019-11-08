from fortools import *

file = Recycle.file_open('path')
# Or you ca use this
# path = 'path'
# file = file_open(path)

# show information about $I recycle file
header = file.header()
size = file.size()
time = file.time()
path = file.path()

# show information from show_all_info()
result = file.show_all_info()
