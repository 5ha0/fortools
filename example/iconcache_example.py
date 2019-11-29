from fortools import *

file = Iconcache.file_open(r'path')
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

# #3.Allows you to check whether the drive delete program is used
# file.drive_delete_exe()

# #4.Allows you to find a specific extension file from all sections
# extension = '.extension'
# information = file.extension_filter(extension)
# #How to make a report
# docx = DocxExport()
# docx.make_table(information)
# docx.save('report_name')
