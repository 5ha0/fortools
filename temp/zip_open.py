# -*- coding: euc-kr -*-
import zipfile

path = input("input zip path : ")
file = open(path, 'rb')
z = zipfile.ZipFile(file, 'r')

zipInfo = z.infolist()
file_info = []

for i in range(zipInfo.__len__()):
    file_info.append(zipInfo[i])
    print(file_info[i])

file.close()
print("success")

