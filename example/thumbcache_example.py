from fortools import *

#input file path
path = r'..\thumbcache_32.db'

# thumbcache_xx.db, iconcache_xx.db file open
thumbnail = file_open(path)

for i in thumbnail.get_hash():
    print(i)
####### 1. It shows all the parsing provided by this library at once. #######
# thumbnail.show_info()

####### 2. It handles all parsing provided by this library at once. #######
information = thumbnail.get_info()

####### 3. It shows specific width, height file data by this library at once. #######
info = thumbnail.dimension(30, 30)

####### 4.If You want to make a report, Use This. #######
# docu = DocxExport()
# docu.add_table(info) # [{key:value},{key:value}]
# docu.save('example')

####### 5.If You want to specific search, Use This Filter. #######
# filter_info = custom_filter(['file_name', r'^.+[.]bmp$', 1], information)
# for i in filter_info:
#    print(i)

