from fortools import *

import time
start_time=time.time()

#close chrome browser
cookies_path="C://Users//JH//AppData//Local//Google//Chrome//User Data//Default//Cookies"
history_path="C://Users//JH//AppData//Local//Google//Chrome//User Data//Default//History"
download_path="C://Users//JH//AppData//Local//Google//Chrome//User Data//Default//History"
print("cookies")
Browser.Chrome.file_open(cookies_path).cookies()
print("history")
Browser.Chrome.file_open(history_path).history()
print("downloads")
result =Browser.Chrome.file_open(download_path).downloads()

cookies_path="C://Users//JH//AppData//Roaming//Mozilla//Firefox//Profiles//8tu3vaet.default-release//cookies.sqlite"
history_path="C://Users//JH//AppData//Roaming//Mozilla//Firefox//Profiles//8tu3vaet.default-release//places.sqlite"
download_path="C://Users//JH//AppData//Roaming//Mozilla//Firefox//Profiles//8tu3vaet.default-release//places.sqlite"
print("cookies")
Browser.Firefox.file_open(cookies_path).cookies()
print("history")
Browser.Firefox.file_open(history_path).history()
print("downloads")
Browser.Firefox.file_open(download_path).downloads()

path="C:\\Users\\JH\\Desktop\\프젝\\WebCacheV01.dat" #extract WebCacheV01.dat
print("cookies")
result=Browser.Ie_Edge.file_open(path).cookies()
print("history")
Browser.Ie_Edge.file_open(path).history()
print("downloads")
result=Browser.Ie_Edge.file_open(path).downloads()
print("cache")
result=Browser.Ie_Edge.file_open(path).cache()


print("---{}s seconds---".format(time.time()-start_time))