##This only analyzes the Iconcache.db
import struct
import json

class Iconcache:
    global file
    global size
def file_open(path):
    global file
    global size
    file = open(path,'rb')
    size = struct.unpack_from('I',file.read(4))[0]
    print(str(size))
##    for i in file
    
def file_version():
    global file
    file.seek(12)
    build_num = file.read(4)
    if build_num == b'\xB1\x1D\x01\x06':
        print('file version is win 10')
        version = 'win10'
        return version
    elif build_num == b'\x5A\x29\x00\x00':
        print('file version is win 10')
        version = 'win10'
        return version
    else:
        print('not supported version')
        return none

def section_one():
    global file
    global size
    global signature
    file.seek(size)
    path_num = struct.unpack_from('I',file.read(4))[0]
    print(str(path_num))
    signature = file.read(2)
    print(signature)
    path_length = file.read(2)
    b = (b'\x00\x00')
    path_length  = path_length + b
    path_length = struct.unpack('<i', path_length)[0]
    print(path_length)
    print(str(path_length))
    sig_chek_list = ['\x02' '\x22' '\x42']
    if signature == sig_chek_list:
        path_length = path_length
        read_num = path_length * path_num
    else:
        path_length = path_length * 2
        read_num = path_length * path_num
    i = 0
    while i != path_num:
        filepaths = file.read(read_num)
        filepaths = filepaths.decode('utf-16')
        filepaths = filepaths.replace('\x00','')
        print(str(filepaths)+'\n')
        i += 1

    size = read_num*path_num + 4


def section_two():
    global file
    global size
    global signature
    file.seek(size)
    path_length = file.read(2)
    b = (b'\x00\x00')
    path_length  = path_length + b
    path_length = struct.unpack('<i', path_length)[0]
    sig_chek_list = ['\x02' '\x22' '\x42']
    if signature == sig_chek_list:
        path_length = path_length
        read_num = path_length * path_num
    else:
        path_length = path_length * 2
        read_num = path_length * path_num
    i = 0
    while i != path_num:
        filepaths = file.read(read_num)
        filepaths = filepaths.decode('utf-16')
        filepaths = filepaths.replace('\x00','')
        print(str(filepaths)+'\n')
        i += 1

    size = read_num*path_num + 4
    
def section_three():
    global file
    global size
    global signature
    file.seek(size)
    path_length = file.read(2)
    b = (b'\x00\x00')
    path_length  = path_length + b
    path_length = struct.unpack('<i', path_length)[0]
    sig_chek_list = ['\x02' '\x22' '\x42']
    if signature == sig_chek_list:
        path_length = path_length
        read_num = path_length * path_num
    else:
        path_length = path_length * 2
        read_num = path_length * path_num
    i = 0
    while i != path_num:
        filepaths = file.read(read_num)
        filepaths = filepaths.decode('utf-16')
        filepaths = filepaths.replace('\x00','')
        print(str(filepaths)+'\n')
        i += 1

    size = read_num*path_num + 4
    
## 함수로 빼기, 함수끼리 연결
    
