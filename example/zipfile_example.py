from fortools import *

# input zip path
# path = r'..\open_test.zip'

# zip file open
zip = file_open(r'..\open_test.zip')
# Or you can use this
# path = 'path'
# file = file_open(path)

# ####### 1. It shows all the parsing provided by this library at once. #######
# zip.show_all_info()

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

####### 6.If You want to extract data, Use This. #######
# zip.extract()

