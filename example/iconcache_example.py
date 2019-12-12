from fortools import *

file = Iconcache.file_open(r'path')
# # Or you can use this
# path = r'path'
# file = file_open(path)

'''
Uncomment the comment you want to use.
'''

####### 1. It shows all the parsing provided by this library at once. #######
# file.show_all_info()

####### 2. It handles all parsing provided by this library at once. #######
# icon = file.get_all_info()
# # if you show 2, use print()
# print(icon)

####### 3. Used when you want to see only some of the information. #######
# icon = file.get_info(['key list'])
# # if you show 2. use print()
# print(icon)

####### 3. Used when you want to see only some of the information. #######
# icon = file.get_info_by_section(['section number list'])
# # if you show 2. use print()
# print(icon)

####### 4. Use when you want to return the hash value before and after analysis of a file #######
# icon = file.get_hash()
# # if you show 2. use print()
# print(icon)

####### 5.Allows you to find a specific extension file from all sections. #######
# extension = 'extension'
# icon = file.extension_filter(extension)
# # if you show 6. use print()
# print(icon)

####### 6.If You want to make a report, Use This. #######
# # !caution!Use the script above first
# # !caution!"5" does not provide the report.py function.
# # 6-1. Docx
# docx = DocxExport()
# docx.table_by_json(icon[i])
# docx.save('ICON')
# # 6-2. MD
# md = MdExport('ICON')
# md.add_table(info)
# md.save()
