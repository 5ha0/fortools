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
