from fortools import *

file = Recycle.file_open(r'path')
# # Or you can use this
# path = r'path'
# file = file_open(path)

'''
Uncomment the comment you want to use.
'''

####### 1. It shows all the parsing provided by this library at once. #######
# file.show_info()

####### 2. It handles all parsing provided by this library at once. #######
# recycle = file.get_all_info()
# # if you show 2. use print()
# print(recycle)

####### 3. Use when you want to return the hash value before and after analysis of a file #######
# recycle = file.get_hash()
# # if you show 2. use print()
# print(recycle)

####### 4.If You want to make a report, Use This. #######
# # !caution!Use the script above first
# # 4-1. Docx
# docx = DocxExport()
# docx.add_table(recycle)
# docx.save('Recycle')
# # 4-2. MD
# md = MdExport('Recycle')
# md.add_table(recycle)
# md.save()
