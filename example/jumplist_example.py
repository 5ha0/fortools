from fortools import *

# example of AutomaticDestinations
# jumplist(.AutomaticDestinations) open
path = r'your path'
jumplist = JumpList.file_open(path)


'''
Uncomment the comment you want to use.
'''

# # ------------------------1. Get data list from destlist.---------------------------
# # You need to input window_version 7 or 10 according your os
# # information: entry number of JumpList, count of add, delete, re-open event, netbios, last access time, access count, path
# summary = jumplist.get_summary(window_version)
# for i in summary:
# 	print(i)
#
# # ------------------------2. Get data list from destlist.---------------------------
# # You need to input window_version 7 or 10 according your os
# # information: MAC(new/birth), netbios, last access time, path, time(new/birth)
# # You can choose list of print like this. [jumplist.get_destlist_data(window_version,[key1, key2, key...])]
# dest_list = jumplist.get_destlist_data(window_version,'all')
# for i in dest_list:
#     print(i)
#
# # ------------------------3. Get information from streams.---------------------------
# # You need to input window_version 7 or 10 according your os
# # infomation: MAC(Modification, Access, Creation) time, file size, target file size, path, drive type, drive serial numbr, volume label
# info_list = jumplist.get_all_info
# for i in info_list:
# 	print(i)
#
# # ------------------------4. Print information from streams.---------------------------
# # You need to input window_version 7 or 10 according your os
# jumplist.show_all_info()
#
# # ------------------------5. Get hash value of jumplist file.---------------------------
# # You need to input window_version 7 or 10 according your os
# jump_hash = jumplist.get_hash()
# for i in jump_hash:
# 	print(i)
#
# # ------------------------6. Get specifin info.---------------------------
# # You need to input window_version 7 or 10 according your os
# jump_hash = jumplist.get_info(['key1', 'key2', ...])
# for i in jump_hash:
# 	print(i)


