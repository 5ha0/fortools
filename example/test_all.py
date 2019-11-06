from fortools import *


# file = file_open('.\\data\\1.hwp')
# file.get_info()
# file = file_open('C:\\Windows\\System32\\winevt\\Logs\\Security.evtx')
# file.show_all_record()
#log_file = EvtxLog.file_open('C:\\Windows\\System32\\winevt\\Logs\\Security.evtx')
#log_file.show_all_record()
# log_file.
# log_file = file_open('C:\\Windows\\System32\\winevt\\Logs\\Security.evtx')

'''
# event_log_file.show_all_record()
# event_log_file.date('2019-10-21')
# event_log_file.favorite.logon()
# event_log_file.get.eventid(5379)

syslog = file_open('.\\syslog')
syslog.date('Oct 22')
syslog1 = file_open('.\\data\\syslog')

# file_open('.\\data\\IMG_0111.jpg')
file = file_open('.\\data\\1.hwp')
file.showlist()
'''
'''

# recycle = file_open('C:\\$Recycle.Bin\\S-1-5-21-844977039-3560465159-1786394663-1001')

# file = file_open('.\\data\\1.pdf')
# print(file.pdf_info())

# linux_log = file_open('.\\auth.log')
# linux_log.show_all_record()

# file = file_open('.\\data\\result.evtx')
# file.get_string()
# letter = 'cABvAHcAZQByAHMAaABlAGwAbAAgAC0AYwAgAC0AbgBvAHAAIAAtAGMAIABpAGUAeAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAcwA6AC8ALwBuAGEAdgBlAHIALgBjAG8AbQAvAD8AaQBmAF8AdABoAGkAcwBfAGkAcwBfAHIAZQBhAGwAXwBtAGEAbAB3AGEAcgBlACwAXwB5AG8AdQByAF8AbgBvAHIAbQBhAGwAXwBhAGMAdABpAG8AbgBfAHMAdQBjAGgAXwBhAHMAXwByAHUAbgBfAHYAcwBjAG8AZABlAF8AYwBhAG4AXwBiAGUAXwB0AHIAaQBnAGcAZQByAF8AdABvAF8AcABlAHIAcwBpAHMAdABlAG4AYwBlAF8AbQBhAGwAdwBhAHIAZQAnACkA'
# print(base64.b64decode(letter).decode('utf-8'))

# file = file_open('.\\data\\1.hwp')
# print(file.return_list())

# file = LinuxLog.Apache.apache_access('.\\access_log')


# file = file_open('.\\data\\1.ppt')
# file.get_info()
# file2 = file_open('.\\data\\1.xls')
# file2.get_info()
# file3 = file_open('.\\data\\1.doc')
# file3.get_info()
'''
# file = file_open('.\\data\\1c7a9be1b15a03ba.automaticDestinations-ms')
'''

# file = file_open('.\\data\\result.evtx')
# file.get_string()
'''
#------------------------ Windows 10 -----------------------------#
#path = r'C:\Users\sjms1\AppData\Local\Microsoft\Windows\Explorer\thumbcache_96.db'
#path = r'C:\Users\sjms1\Desktop\win7_explorer\thumbcache_96.db'
#icon_path = r'C:\Users\sjms1\AppData\Local\Microsoft\Windows\Explorer\iconcache_48.db'
#thumbnail = Thumbnail.file_open(path)
#thumbnail.get_data(path)

#------------------------ Windows 7 -----------------------------#
# path = r'C:\Users\sjms1\Desktop\Explorer\thumbcache_96.db'
# thumbnail = Thumbnail.file_open(path)
# thumbnail.get_data(path)

#------------------------ filelist ------------------------------#
#path = r"C:\Users"
#files_analysis.file_list(path)

#------------------------ ZipFile -------------------------------#
path = r'C:\Users\sjms1\Desktop\Educate\cos.jar'
file = Files.ZIP.file_open(path)
file.get_info()