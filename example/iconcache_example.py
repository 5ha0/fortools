from fortools import *

# file = Iconcache.file_open('C:\\Users\\graci\\AppData\\Local\\IconCache.db')
file = Iconcache.file_open(r'C:\Users\graci\Desktop\IconCache\IconCache.db')
# Or you ca use this
# path = 'path'
# file = file_open(path)

# show information about IconCache.db
version = file.file_version()
path_information1 = file.section_one()
path_information2 = file.section_two()
path_information3 = file.section_three()

# show information from show_all_info()
doc = file.show_all_info()
