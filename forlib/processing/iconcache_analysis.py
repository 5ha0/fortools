import struct
import json

class IconcacheAnalysis:
    def __init__(self, file):
        self.file = file
        self.size = None
        self.signature = None
        self.path_num = None
        
    def file_version(self):
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
            return -1

    def section_one(self):
        self.file.seek(0)
        self.size = struct.unpack_from('<I', self.file.read(4))[0]
        
        self.file.seek(self.size)
        self.path_num = struct.unpack_from('<i', self.file.read(4))[0]
        
        self.signature = self.file.read(2)
        
        path_length = self.file.read(2)
        b = (b'\x00\x00')
        path_length = path_length + b
        path_length = struct.unpack('<i', path_length)[0]
        
        sig_chek_list = ['\x02' '\x22' '\x42']
        if self.signature == sig_chek_list:
            path_length = path_length
        else:
            path_length = path_length * 2

        print('path information in section 1')
        i = 0
        while i != self.path_num:
            filepaths = self.file.read(path_length)
            filepaths = filepaths.decode('utf16', 'ignore')
            filepaths = filepaths.replace('\x00','')
            print(str(filepaths)+'\n')
            i += 1

        self.size = self.size + path_length * self.path_num + 12
        
        return filepaths


    def section_two(self):
        self.file.seek(self.size)
        path_length = self.file.read(2)
        b = (b'\x00\x00')
        path_length = path_length + b
        path_length = struct.unpack('<i', path_length)[0]
        
        sig_chek_list = ['\x02' '\x22' '\x42']
        if self.signature == sig_chek_list:
            path_length = path_length
        else:
            path_length = path_length * 2

        print('path information in section 2')
        i = 0
        while i != self.path_num:
            filepaths = self.file.read(path_length)
            filepaths = filepaths.decode('utf-16', 'ignore')
            filepaths = filepaths.replace('\x00','')
            print(str(filepaths)+'\n')
            i += 1

        self.size = self.size + path_length * self.path_num + 14
        
        return filepaths
    
    
    def section_three(self):
        self.file.seek(self.size)
        path_length = self.file.read(2)
        b = (b'\x00\x00')
        path_length = path_length + b
        path_length = struct.unpack('<i', path_length)[0]
        
        sig_chek_list = ['\x02' '\x22' '\x42']
        if self.signature == sig_chek_list:
            path_length = path_length
        else:
            path_length = path_length * 2

        print('path information in section 3')
        i = 0
        while i != self.path_num:
            filepaths = self.file.read(path_length)
            filepaths = filepaths.decode('utf-16', 'ignore')
            filepaths = filepaths.replace('\x00','')
            print(str(filepaths)+'\n')
            i += 1
            
        return filepaths


    def show_all_info(self):
        info_list = []
        info = dict()
        info["file version"] = str(self.file_version())
        info["path information_section one"] = str(self.section_one())
        info["path information_section two"] = str(self.section_two())
        info["path information_section three"] = str(self.section_three())

        print(info)
        info_list.append(info)
        return info_list
