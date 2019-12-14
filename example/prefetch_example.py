from fortools import *

file = Prefetch.file_open(r'file path')
# # Or you can use this
# path = r'path'
# file = file_open(path)

# #Use this when you want to analyze files in a folder
# info = Prefetch.file_open(r'folder path')
# # if you want to show this, use print()
# print(info)
# # if You want to make a report, Use This
# docx = DocxExport()
# for i in range(0, len(info)):
#     docx.table_by_json(info[i])
# docx.save('PF')

'''
Uncomment the comment you want to use.
'''

####### 1. It shows all the parsing provided by this library at once. #######
# file.show_all_info()

####### 2. It handles all parsing provided by this library at once. #######
# prefetch = file.get_all_info()
# # if you show 2, use print()
# print(prefetch)

####### 3. Used when you want to see only some of the information. #######
# prefetch = file.get_info(['key list'])
# # if you show 2. use print()
# print(prefetch)

####### 4. Use when you want to return the hash value before and after analysis of a file #######
# prefetch = file.get_hash()
# # if you show 2. use print()
# print(prefetch)

####### 5. Allows you to find a specific extension file from file list. #######
# extension = 'extension'
# prefetch = file.extension_filter(extension)
# # if you show 6. use print()
# print(prefetch)

####### 6.If You want to make a report, Use This. #######
# # !caution!Use the script above first
# # How to make a report
# # 6-1. Docx
# docx = DocxExport()
# docx.table_by_json(prefetch[0])
# docx.save('PF')
# # 6-2. MD
# md = MdExport('PF')
# md.add_table(prefetch)
# md.save()

