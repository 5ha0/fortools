from fortools import *

# input zip path
path = r'C:\Users\sjms1\Desktop\Desktop.zip'

# zip file open
zip = file_open(path)
# Or you can use this
# path = 'path'
# file = file_open(path)

####### 1. It shows all the parsing provided by this library at once. #######
zip.show_info()

####### 2. It handles all parsing provided by this library at once. #######
# information = zip.get_all_info()
# print(information)

####### 3.If You want to make a report, Use This. #######
# docx = DocxExport()
# docx.add_table(information)
# docx.save('zipfile')

####### 4.If You want to specific search, Use This Filter. #######
# fil = custom_filter(['FileName', r'\w+.jpg', 1], information)
# for i in fil:
#     print(i)

####### 5.If You want to get hash data, Use This. #######
# for i in zip.get_hash():
#     print(i)

####### 6. Used when you want to see only some of the information. #######
# for i in zip.get_info(['num','FileName']):
#     print(i)

####### 7.If You want to extract data, Use This. #######
# zip.extract()

