from fortools import *

path = r'C:\Users\sjms1\AppData\Local\Microsoft\Windows\Explorer\thumbcache_1280.db'
#path = r'C:\Users\sjms1\Desktop\thumbcache_256.db'
thumbnail = Thumbnail_Iconcache.file_open(path)
data = thumbnail.get_data(path)

# docu = DocxExport()
# print("Hi")
# docu.make_table(data) # [{key:value},{key:value}]
# docu.save('example')