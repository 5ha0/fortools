from fortools import *

path = r'C:\Users\sjms1\AppData\Local\Microsoft\Windows\Explorer\thumbcache_32.db'
#path = r'C:\Users\sjms1\Desktop\thumbcache_256.db'
#path = r'D:\fortools_test_file\thumbcache_256.db'

thumbnail = Thumbnail_Iconcache.file_open(path)

#data = thumbnail.get_data(path)
for i in thumbnail.dimension(1):
     print(i)
#thumbnail.thumb_print(data)



# filter_info = custom_filter(['file_name', r'^.+[.]bmp$', 1], data)
# for i in filter_info:
#    print(i)

# docu = DocxExport()
# print("Hi")
# docu.make_table(data) # [{key:value},{key:value}]
# docu.save('example')