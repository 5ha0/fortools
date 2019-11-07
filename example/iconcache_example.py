from fortools import *

file = Iconcache.file_open('C:\\Users\\graci\\AppData\\Local\\IconCache.db')

# show information from IconCache.db
version = file.file_version()
list1 = file.section_one()
list2 = file.section_two()
list3 = file.section_three()

# show information from IconCache_##.db
