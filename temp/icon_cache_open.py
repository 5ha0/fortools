import os

user_profile = os.environ['USERPROFILE']

icon_cache_path = user_profile + '\AppData\Local\IconCache.db'
file = open(icon_cache_path,'rb')
print("success")

while True:
    line = file.readline()
    if not line: break
    print(line)
