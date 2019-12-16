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

####### 3. Use when you want to return the hash value before and after analysis of a file #######
# icon = file.get_hash()
# # if you show 2. use print()
# print(icon)

####### 4. For the convenience of users, only the information of the desired section is displayed. #######
# icon = file.Favorite.show_info_by_section(['section number list'])

####### 5.Shows the extension information for all sections of the path information and the number of each extension. #######
# icon = file.Favorite.show_kind_of_extension()

####### 6.The path information in all sections shows the drive type information and the number of each drive type. #######
# icon = file.Favorite.show_kind_of_drivetype()

####### 7.If You want to make a report, Use This. #######
# # !caution!Use the script above first
# # 7-1. Docx
# docx = DocxExport()
# docx.table_by_json(icon[i])
# docx.save('ICON')
# # 7-2. MD
# md = MdExport('ICON')
# md.add_table(info)
# md.save()
