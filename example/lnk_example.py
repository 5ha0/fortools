from fortools import *

file = Lnk.file_open(r'path')
# # Or you can use this
# path = r'path'
# file = file_open(path)

'''
Uncomment the comment you want to use.
'''

####### 1. It shows all the parsing provided by this library at once. #######
# file.show_info()

####### 2. It handles all parsing provided by this library at once. #######
# lnk = file.get_all_info()
# # if you show 2. use print()
# print(lnk)

####### 3. Used when you want to see only some of the information. #######
# lnk = file.get_info(['key list'])
# # if you show 2. use print()
# print(lnk)

####### 4. Use when you want to return the hash value before and after analysis of a file #######
# lnk = file.get_hash()
# # if you show 2. use print()
# print(lnk)

####### 4.If You want to make a report, Use This. #######
# # !caution!Use the script above first
# # 5-1. Docx
# docx = DocxExport()
# docx.table_by_json(lnk[0])
# docx.save('Lnk')
# # 5-2. MD
# md = MdExport('Lnk')
# md.add_table(lnk)
# md.save()
