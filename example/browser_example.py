from fortools import *
import time
start_time = time.time()

chrome_cookies = Browser.Chrome.Cookie.file_open(cookies_path)
chrome_history = Browser.Chrome.History.file_open(history_path)
chrome_download = Browser.Chrome.Download.file_open(download_path)
chrome_cache=Browser.Chrome.Cache.file_open(cache_path)

print("history")
for i in chrome_history.get_info():
   print(i)
print("cookies")
for i in chrome_cookies.get_info():
    print(i)
print("download")
for i in chrome_download.get_info():
    print(i)
print("cache")
for i in chrome_cache.get_info():
    print(i)


#get hash
print(chrome_cookies.get_hash())
print(chrome_history.get_hash())
print(chrome_download.get_hash())

# path= path of WebCacheV01.dat

IE_Edge_cookies = Browser.Ie_Edge.Cookie.file_open(path)
IE_Edge_history = Browser.Ie_Edge.History.file_open(path)
IE_Edge_download=Browser.Ie_Edge.Download.file_open(path)
IE_Edge_cache=Browser.Ie_Edge.Cache.file_open(path)

print("history")
for i in IE_Edge_history.get_info():
    print(i)
print("cookie")
for i in IE_Edge_cookies.get_info():
    print(i)
print("download")
for i in IE_Edge_download.get_info():
     print(i)
print("cache")
for i in IE_Edge_cache.get_info():
     print(i)

#get hash
print(IE_Edge_cookies.get_hash())
print(IE_Edge_history.get_hash())
print(IE_Edge_download.get_hash())
print(IE_Edge_cache.get_hash())


print("---{}s seconds---".format(time.time()-start_time))
