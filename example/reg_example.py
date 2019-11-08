from fortools import RegistryHive

# # SYSTEM File Analysis
# reg_file = RegistryHive.file_open("C:\\Users\\liber\\Desktop\\reg\\SYSTEM")
#
# # network inforamtion
# net_info = reg_file.get_network_info()
#
# for i in range(len(net_info)):
#     print(net_info[i])

# #SAM File Analysis
# reg_file2 = RegistryHive.file_open("C:\\Users\\liber\\Desktop\\reg\\SAM")
#
# #etwork inforamtion
# user_info = reg_file2.user_info()
#
# for i in range(len(user_info)):
#     print(user_info[i])
#
## NTUSER.DAT Analysis
reg_file3 = RegistryHive.file_open("C:\\Users\\sjms1\\Desktop\\fortools\\dataset\\Users\\forensic\\NTUSER.DAT")

#ms office information
ms_office = reg_file3.get_recent_docs()

for i in range(len(ms_office)):
    print(ms_office[i])

#user assist information
# user_assist = reg_file3.get_userassist()
#
# for i in range(len(user_assist)):
#     print(user_assist[i])

#SOFTWARE File Analysis
# reg_file4 = RegistryHive.file_open("C:\\Users\\liber\\Desktop\\reg\\SOFTWARE")
#
# #os information
# os_info = reg_file4.get_info()
#
# for i in range(len(os_info)):
#     print(os_info[i])
