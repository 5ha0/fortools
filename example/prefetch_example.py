from fortools import *

# file = Prefetch.file_open(r'path')
# # Or you can use this
path = r'path'
file = file_open(path)

'''
Uncomment the comment you want to use.
'''

####### 1. It shows all the parsing provided by this library at once. #######
# information = file.show_all_info()

####### 2. It handles all parsing provided by this library at once. #######
# information = file.get_all_info()
# # if you show 2, use print()
# print(information)

####### 3. You can parse only one value. #######
# information = file.file_list()
# #parse list [.file_name(), .last_launch_time(), .create_time(), .write_time(), .num_launch(), .file_list(), .metadata_info(), .cal_hash()]
# print(information)

####### 4. Allows you to find a specific extension file from file list. #######
# extension = '.extension'
# information = file.extension_filter_pf(extension)
# print(information)

####### 5.If You want to make a report, Use This. #######
# !caution!Use the script above first
# # #How to make a report
# docx = DocxExport()
# docx.add_table(information)
# docx.save('report_name')

