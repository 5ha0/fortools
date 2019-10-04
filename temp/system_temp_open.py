import os
from os import listdir

user_profile = os.environ['USERPROFILE']
temp_path = user_profile+'\Local Settings\Temp'     # 사용자 임시폴더 경로

files = [f for f in listdir(temp_path)]
for i in range(files.__len__()):
    print(files[i])

print("Success")
print(files.__len__())
print(files.__sizeof__())
print(temp_path)


#-------------------------------------------------------------#


windows = os.environ['SYSTEMROOT']
windows_temp_path = windows+'\TEMP'     # 윈도우 임시폴더 경로
print(windows_temp_path)

files = [f for f in listdir(windows_temp_path)]
for i in range(files.__len__()):
    print(files[i])

print(files.__len__())
print(files.__sizeof__())
print("Success")








