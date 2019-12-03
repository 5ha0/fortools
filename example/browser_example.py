from fortools import *
import time


# chrome_cookies = Browser.Chrome.Cookie.file_open(cookies_path)
# chrome_history = Browser.Chrome.History.file_open(history_path)
# chrome_download = Browser.Chrome.Download.file_open(download_path)
# chrome_cache=Browser.Chrome.Cache.file_open(cache_path)

# print(chrome_cookies.get_hash())
# print(chrome_history.get_hash())
# print(chrome_download.get_hash())

# print("history")
# for i in chrome_history.get_info():
#    print(i)
# print("cookies")
# for i in chrome_cookies.get_info():
#     print(i)
# print("download")
# for i in chrome_download.get_info():
#     print(i)
# print("cache")
# for i in chrome_cache.get_info():
#     print(i)


# path=WebCacheV01.dat path

# IE_Edge_cookies = Browser.Ie_Edge.Cookie.file_open(path)
# IE_Edge_history = Browser.Ie_Edge.History.file_open(path)
# IE_Edge_download=Browser.Ie_Edge.Download.file_open(path)
# IE_Edge_cache=Browser.Ie_Edge.Cache.file_open(path)

# print(IE_Edge_cookies.get_hash())
# print(IE_Edge_history.get_hash())
# print(IE_Edge_download.get_hash())
# print(IE_Edge_cache.get_hash())

# print("history")
# for i in IE_Edge_history.get_info():
#     print(i)
# print("cookie")
# for i in IE_Edge_cookies.get_info():
#     print(i)
# print("download")
# for i in IE_Edge_download.get_info():
#      print(i)
# print("cache")
# for i in IE_Edge_cache.get_info():
#      print(i)

# Firefox_cookies=Browser.Firefox.Cookie.file_open(cookies_path)
# Firefox_download=Browser.Firefox.Download.file_open(download_path)
# Firefox_history=Browser.Firefox.History.file_open(history_path)

# print(Firefox_cookies.get_hash())
# print(Firefox_history.get_hash())
# print(Firefox_download.get_hash())

# print("history")
# for i in Firefox_history.get_info():
#     print(i)
# print("cookie")
# for i in Firefox_cookies.get_info():
#     print(i)
# print("download")
# for i in Firefox_download.get_info():
#      print(i)



# #keyword_search
# keyword =chrome_history.keyword_search("keyword")
# for i in keyword:
#     print(i)
# keyword =IE_Edge_history.keyword_search("keyword")
# for i in keyword:
#     print(i)

# #cnt_sort
# cnt_list = IE_Edge_history.cnt_sort()
# for i in cnt_list:
#     print(i)
# cnt_list = chrome_history.cnt_sort()
# for i in cnt_list:
#     print(i)

# #make report
# get_docx = DocxExport()
# get_docx.add_table((ex)IE_Edge_cookies.get_info())
# get_docx.save("report_name")

