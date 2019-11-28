from fortools import *

file = Recycle.file_open(r'path')
# Or you can use this
# path = 'path'
# file = file_open(path)

# #Uncomment the comment you want to use.# #

# #1. It shows all the parsing provided by this library at once
# information = file.show_all_info()
# #How to make a report
# docx = DocxExport()
# docx.make_table(information)
# docx.save('report_name')

# #2. It handles all parsing provided by this library at once.
# information = file.get_all_info()
# # if you show 2, use print()
# print(information)
# #How to make a report
# docx = DocxExport()
# docx.make_table(information)
# docx.save('report_name')
