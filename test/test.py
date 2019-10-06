from forlib.fortools import log
from forlib.fortools import file
from forlib.fortools import unknown

zip_file = file.file_open('./zip_test.zip')
zip_info = zip_file.infolist()
file_info = []

for i in range(zip_info.__len__()):
    file_info.append(zip_info[i])
    print(file_info[i])

#evtx_file = log.file_open('C:\Windows\System32\winevt\Logs\Application.evtx')
#evtx_file.get_event_ID(10)
=======
from forlib.fortools import registry
from forlib.fortools import unknown
from forlib.fortools import system_temp
import os, datetime

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

'''
reg_file = registry.file_open("test/NTUSER.DAT")
print("==================[+]registry microsoft information==================\n")
reg_info = reg_file.get_find_key("microsoft")
print("\n==================[+]registry recent file-----need decode modify==================\n")
reg_recent = reg_file.recent_docs()
'''

evtx_file = log.file_open('C:\Windows\System32\winevt\Logs\Application.evtx')
#evtx_file.show_all_record()
evtx_file.eventID(15)
