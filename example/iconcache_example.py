from fortools import *

file = Iconcache.file_open(r'C:\Users\graci\Desktop\cfreds_11\IconCache.db')
# Or you ca use this
# path = 'path'
# file = file_open(path)

# show information about IconCache.db
information = file.all_info()

# Allows you to check whether the drive delete program is used.
file.drive_delete_exe()

# Allows you to find a specific extension file.
extension = '.extension'
file.extension_filter(extension)

# if you want to look time stamp for filepath, use this
filepath = r'enter the file path you want to check the time of'
file.show_time(filepath)
