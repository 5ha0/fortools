from forlib.fortools import Log
from forlib.fortools import Files
from forlib.fortools import Unknown
from forlib.fortools import System_temp
from forlib.fortools import Registry
from forlib.fortools import System_temp
from forlib.fortools import Icon_cache
from forlib.fortools import FileSystem

zip_file = Files.file_open('./zip_test.zip')
zip_info = zip_file.infolist()
file_info = []

for i in range(zip_info.__len__()):
    file_info.append(zip_info[i])
    print(file_info[i])

#reg_file = Registry.file_open("test/NTUSER.DAT")
#print("==================[+]registry microsoft information==================\n")
#reg_info = reg_file.get_find_key("microsoft")
#reg_info = reg_file.get_recent_excel()
#reg_info = reg_file.get_recent_ppt()
#print("\n==================[+]registry recent file-----need decode modify==================\n")
#reg_recent = reg_file.get_recent_docs()
        
# user_profile = os.environ['USERPROFILE']
# systemp_file = system_temp.file_open(user_profile+'\Local Settings\Temp')
# for i in range(systemp_file.__len__()):
#   print(systemp_file[i])

# zip_file = file.file_open('./zip_test.zip')
# zip_info = zip_file.infolist()
# file_info = []
#
# for i in range(zip_info.__len__()):
#     file_info.append(zip_info[i])
#     print(file_info[i])

#evtx_file = Log.file_open('C:\Windows\System32\winevt\Logs\Application.evtx')
#evtx_file.show_all_record()
#evtx_file.eventID(6003)

user_temp_path = r'C:\Users\sjms1\AppData\Local\Temp'
user_temp = System_temp.file_open(user_temp_path)
print("\n==================[+]User Temp Folder information=====================\n")
user_temp.get_temp(user_temp_path)


windows_temp_path = r'C:\Windows\Temp'
windows_temp = System_temp.file_open(windows_temp_path)
print("\n==================[+]Windows Temp Folder information==================\n")
windows_temp.get_temp(windows_temp_path)

icon_cache_path = r'C:\Users\sjms1\AppData\Local\IconCache.db'
icon_cache = Icon_cache.file_open(icon_cache_path)

reg_ms = Registry.file_open("test/NTUSER.DAT")
print("\n========================[+]registry find key========================\n")
print(reg_file.find_key("microsoft"))
print("\n==================[+]registry micosoft information==================\n")
res = reg_file.get_ms_offic()
for i in range(len(res)):
    print(res[i])
    
reg_file = Registry.file_open("test/Users/forensic/NTUSER.DAT")
print("\n==================[+]registry userassist information==================\n")
result = reg_file.get_userassist()
for i in range(len(result)):
    print(result[i])

fs_file = FileSystem.file_open("../test/ntfs.dd")
fs_file.fslog_extract()    
    
# evtx_file = Log.file_open('C:\Windows\System32\winevt\Logs\Application.evtx')
# evtx_file.show_all_record()
# evtx_file.xml_with_num(104)
# evtx_file.eventID(1000)
# evtx_file.level(4)


#webLog_file = Log.file_open('C:\\inetpub\\logs\\LogFiles\\W3SVC1\\u_ex191007.log')
# webLog_file.show_all_record()
#webLog_file.date('2019-10-07')
