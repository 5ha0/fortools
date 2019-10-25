import os.path
from struct import unpack
import struct
import binascii
##from datetime import datetime as dt
from datetime import datetime
from datetime import timedelta
import string
import sys

global file

def file_open(path):
    global file
    file_extension_recycle = path.split('\\')[-1]
    if '$R' in file_extension_recycle:
        file_extension = path.split('.')[1]
        file = file_open.extension_file_open(file_extension,path)
        return file
    elif '$I' in file_extension_recycle:
        file = open(path,'rb')
        return file

##def r_header():
##    global file
##    file.seek(0)
##    fileheader = file.read(8)
##    fileheader = binascii.hexlify(fileheader).decode('ascii')
##    print("File Header (not needed): " + fileheader)

def r_size():
    global file
    filesize1 = file.read(4)
    filesize2 = file.read(4)
    filesize1 = unpack("<I", filesize1)[0]
    filesize2 = unpack("<I", filesize2)[0]
    filesize = filesize1 + filesize2
    print('File Size: ' + str(filesize) + ' bytes')

def r_time():
    global file
    file.seek(16)
    filedatetime = struct.unpack_from('<q', file.read(8))[0]
    filedatetime = '%016x' %filedatetime
    filedatetime = int(filedatetime,16)/10.
    filedatetime =  datetime(1601, 1, 1) + timedelta(microseconds=filedatetime)+timedelta(hours=9)  
    print('File Time: ' + iledatetime + '+ UTC-9')


def r_path():
    global file
    file.seek(24)
    path = str(file.read(), 'cp1252')
    path = path.replace('\x00','').encode('', 'ignore').decode('cp949')
    print(path)
