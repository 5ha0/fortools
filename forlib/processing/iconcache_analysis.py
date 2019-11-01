import struct
import json

class IconcacheAnalysis:
    def __init__(self, file):
        self.file = file
        self.size
        self.signature
        
    def file_version():
        self.file.seek(12)
        build_num = self.file.read(4)
        if build_num == b'\xB1\x1D\x01\x06':
            print('File Version is win 10')
            version = 'win10'
            return version
        elif build_num == b'\x5A\x29\x00\x00':
            print('File Version is win 10')
            version = 'win10'
            return version
        else:
            print('not supported version')
            return none

    def section_one():
        self.file.seek(0)
        self.size = struct.unpack_from('<I', self.file.read(4))[0]
        
        self.file.seek(size)
        path_num = struct.unpack_from('<i', self.file.read(4))[0]
        
        self.signature = self.file.read(2)
        
        path_length = self.file.read(2)
        b = (b'\x00\x00')
        path_length  = path_length + b
        path_length = struct.unpack('<i', path_length)[0]
        
        sig_chek_list = ['\x02' '\x22' '\x42']
        if self.signature == sig_chek_list:
            path_length = path_length
        else:
            path_length = path_length * 2
        
        i = 0
        while i != path_num:
            filepaths = self.file.read(path_length)
            filepaths = filepaths.decode('utf16', 'ignore')
            filepaths = filepaths.replace('\x00','')
            print(str(filepaths)+'\n')
            i += 1

        self.size = self.size + path_length * path_num + 12


    def section_two():
        self.file.seek(size)
        path_length = self.file.read(2)
        b = (b'\x00\x00')
        path_length  = path_length + b
        path_length = struct.unpack('<i', self.path_length)[0]
        
        sig_chek_list = ['\x02' '\x22' '\x42']
        if self.signature == sig_chek_list:
            path_length = path_length
        else:
            path_length = path_length * 2
        
        i = 0
        while i != path_num:
            filepaths = self.file.read(path_length)
            filepaths = filepaths.decode('utf-16', 'ignore')
            filepaths = filepaths.replace('\x00','')
            print(str(filepaths)+'\n')
            i += 1

        self.size = self.size + path_length * path_num + 14
    
    def section_three():
        self.file.seek(size)
        path_length = self.file.read(2)
        b = (b'\x00\x00')
        path_length  = path_length + b
        path_length = struct.unpack('<i', path_length)[0]
        
        sig_chek_list = ['\x02' '\x22' '\x42']
        if self.signature == sig_chek_list:
            path_length = path_length
        else:
            path_length = path_length * 2
        
        i = 0
        while i != path_num:
            filepaths = self.file.read(read_num)
            filepaths = filepaths.decode('utf-16', 'ignore')
            filepaths = filepaths.replace('\x00','')
            print(str(filepaths)+'\n')
            i += 1
