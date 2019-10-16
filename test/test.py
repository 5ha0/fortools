from forlib.fortools import Registry
from forlib.fortools import FileSystem

reg_file = Registry.file_open("test/Users/forensic/NTUSER.DAT")
result = reg_file.get_userassist()
for i in range(len(result)):
    print(result[i])

# pre_file = Prefetch.file_open("test/Prefetch/FTK IMAGER.EXE-9AAD2C05.pf")
# pre_file.pf_file_list()
