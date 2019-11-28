from fortools import *

file = Prefetch.file_open(r'C:\Windows\Prefetch\DLLHOST.EXE-6F6F0336.pf')
# # Or you can use this
# path = 'path'
# file = file_open(path)

# #Uncomment the comment you want to use.# #

#1. It shows all the parsing provided by this library at once
information = file.show_all_info()
#How to make a report
docx = DocxExport()
docx.make_table(information)
docx.save('report_name')

# #2. It handles all parsing provided by this library at once.
# information = file.get_all_info()
# # if you show 2, use print()
# print(information)
# #How to make a report
# docx = DocxExport()
# docx.make_table(information)
# docx.save('report_name')

# #3. You can parse only one value
# value = file.file_list()
# #parse list [.file_name(), .last_launch_time(), .create_time(), .write_time(), .num_launch(), .file_list(), .metadata_info()]
# print(value)
# #How to make a report
# docx = DocxExport()
# docx.make_table(value)
# docx.save('report_name')

# #4. Allows you to find a specific extension file from file list
# extension = '.extension'
# exe_file = file.extension_filter_pf(extension)
# print(exe_file)
# #How to make a report
# docx = DocxExport()
# docx.make_table(exe_file)
# docx.save('report_name')

