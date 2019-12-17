from fortools import *

# example of filesystem log

path = r'your path'
filesys_log = FileSystemLog.file_open(path)

'''
Uncomment the comment you want to use.
'''

# # ------------------------1. Get information of filesystem log.---------------------------
# file_syslog_info = filesys_log.get_all_info()
# for i in file_syslog_info:
# 	print(i)
#
# # ------------------------2. Get hash value of filesystem log.---------------------------
# file_syslog_hash = filesys_log.get_hash()
# for i in file_syslog_hash:
# 	print(i)
#
# # ------------------------3. Print information of filesystem log.---------------------------
# filesys_log.show_all_info()

