from fortools import *

path = r'C:\Users\sjms1\AppData\Local\Microsoft\Windows\Explorer\thumbcache_32.db'

thumbnail = Thumbnail_Iconcache.file_open(path)
#thumbnail.thumb_print()
#data = thumbnail.get_data(path)
thumbnail.dimension(32, 8)




# filter_info = custom_filter(['file_name', r'^.+[.]bmp$', 1], data)
# for i in filter_info:
#    print(i)

# docu = DocxExport()
# print("Hi")
# docu.make_table(data) # [{key:value},{key:value}]
# docu.save('example')