from fortools import RegistryHive

#NTUSER.DAT file analysis
reg_file = RegistryHive.file_open("C:\\Users\\liber\\Desktop\\reg\\SAM")

# # recent docs read
# result = reg_file.get_recent_docs()
# for i in range(len(result)):
#     print(result[i])
#
# # ms office file
# result2 = reg_file.get_ms_office()
# for i in range(len(result2)):
#     print(result2[i])

# result = reg_file.get_network_info()
# for i in range(len(result)):
#     print(result[i])
result = reg_file.user_info()
for i in range(len(result)):
    print(result[i])
# result3 = reg_file.get_network_info()
# for i in range(len(result3)):
#     print(result3[i])
