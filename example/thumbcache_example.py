from fortools import *

#input file path
path = r'C:\Users\sjms1\AppData\Local\Microsoft\Windows\Explorer\thumbcache_32.db'

# thumbcache_xx.db, iconcache_xx.db file open
thumbnail = file_open(path)
#thumbnail.thumb_print()

####### 1. It shows all the parsing provided by this library at once. #######
# thumbnail.thumb_print()

####### 2. It handles all parsing provided by this library at once. #######
information = thumbnail.get_info()

# thumbnail.dimension(32, 8)




# filter_info = custom_filter(['file_name', r'^.+[.]bmp$', 1], data)
# for i in filter_info:
#    print(i)

# docu = DocxExport()
# print("Hi")
# docu.make_table(data) # [{key:value},{key:value}]
# docu.save('example')