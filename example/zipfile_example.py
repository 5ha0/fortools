from fortools import *

# input zip path
path = r'C:\Users\sjms1\Desktop\와장창.zip'

# zip file open
file = Files.ZIP.file_open(path)

# zip file info print
file.show_info()

print('\n\n')

info = file.get_info()
fil = custom_filter(['FileName', r'\w+.jpg', 1], info)
for i in fil:
    print(i)




