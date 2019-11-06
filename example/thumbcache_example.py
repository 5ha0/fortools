from fortools import *

path = r'C:\Users\sjms1\AppData\Local\Microsoft\Windows\Explorer\thumbcache_256.db'
thumbnail = Thumbnail.file_open(path)
thumbnail.get_data(path)