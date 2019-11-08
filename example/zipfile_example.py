from fortools import *

# input zip path
path = r'C:\Users\sjms1\Desktop\Educate\cos.jar'

# zip file open
file = Files.ZIP.file_open(path)

# zip file info print
file.get_info()


