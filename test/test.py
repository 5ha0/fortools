from forlib.fortools import Log
from forlib.fortools import Files
from forlib.fortools import Unknown
from forlib.fortools import Registry
from forlib.fortools import System_temp
import os, datetime
'''
zip_file = file.file_open('./zip_test.zip')
zip_info = zip_file.infolist()
file_info = []

for i in range(zip_info.__len__()):
    file_info.append(zip_info[i])
    print(file_info[i])

#evtx_file = log.file_open('C:\Windows\System32\winevt\Logs\Application.evtx')
#evtx_file.get_event_ID(10)
'''
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

reg_file = Registry.file_open("test/NTUSER.DAT")
print("==================[+]registry microsoft information==================\n")
reg_info = reg_file.get_find_key("Windows Mail")
reg_info2 = reg_file.get_find_key("microsoft")
# print("\n==================[+]registry recent file-----need decode modify==================\n")
#reg_recent = reg_file.recent_docs()
'''
evtx_file = log.file_open('C:\Windows\System32\winevt\Logs\Application.evtx')
#evtx_file.show_all_record()
evtx_file.eventID(15)
'''