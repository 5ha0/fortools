from fortools import *

file = Recycle.file_open(r'path')
# # Or you can use this
# path = r'path'
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

####### 3.If You want to make a report, Use This. #######
# # !caution!Use the script above first
# docx = DocxExport()
# docx.add_table(information)
# docx.save('report_name')
