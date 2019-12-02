from fortools import *

file = Lnk.file_open(r'path')
# Or you ca use this
# path = 'path'
# file = file_open(path)

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
# information = file.lnk_creation_time()
# parse list [.file_attribute, .creation_time(), .access_time(), .write_time(), .lnk_creation_time(), .lnk_access_time(), .lnk_write_time(), .file_size(), icon_indes(), .show_command(), .volume(), .localbase_path(), .netbios(), .machine_id, .show_all_info(), get_all_info()]
# print(information)

####### 4.If You want to make a report, Use This. #######
# !caution!Use the script above first
# #How to make a report
# docx = DocxExport()
# docx.make_table(information)
# docx.save('report_name')

