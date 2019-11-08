# This file only analysis Iconcache.db
# If you want to analysis Iconcache_##.db, go to Thumbnail_analysis.py
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
        # file size
        self.file.seek(0)
        self.size = struct.unpack_from('<I', self.file.read(4))[0]

        # section one path information num
        self.file.seek(self.size)
        self.path_num = struct.unpack_from('<i', self.file.read(4))[0]
        print(self.path_num)

        for i in range(0, self.path_num):

            self.signature = self.file.read(2)
            print(str(i+1) + ' : ' + 'sig' + ' : ' + str(self.signature))
            # self.size = self.size + 2
            # sss = self.signature

            path_length = self.file.read(2)
            print(path_length)
            b = (b'\x00\x00')
            path_length = path_length + b
            path_length = struct.unpack('<i', path_length)[0]
            print('len1: '+str(path_length))

            sig_chek_list = [b'"\x00', b'\x02\x00', b'\x42\x00']
            if self.signature in sig_chek_list:
                path_length = path_length
            else:
                path_length = path_length * 2
            print('len2: '+str(path_length))

            print('path information :')
            filepaths = self.file.read(path_length)
            filepaths = filepaths.decode('utf16', 'ignore')
            filepaths = filepaths.replace('\x00', '')
            print(str(filepaths) + '\n')

            print('icon location: ')
            icon_location = self.file.read(4)
            print(str(icon_location)+ '\n')
            # icon_location = icon_location.decode('utf16', 'ignore')
            # icon_location = icon_location.replace('\x00', '')
            # print(str(icon_location) + '\n')

        return filepaths


    def section_two(self):

        print('####################################################################################')
        print('section 2')
        # section one path information num
        # self.file.seek(self.size)

        # section one path information num
        self.file.seek(self.size)
        self.path_num = struct.unpack_from('<i', self.file.read(4))[0]
        print(self.path_num)

        for i in range(0, self.path_num):
            print('count: ' + str(i + 1))

            path_length = self.file.read(2)
            b = (b'\x00\x00')
            path_length = path_length + b
            path_length = struct.unpack('<i', path_length)[0]
            path_length = path_length * 2
            print('len1: ' + str(path_length))

            print('path information :')
            filepaths = self.file.read(path_length)
            filepaths = filepaths.decode('utf16', 'ignore')
            filepaths = filepaths.replace('\x00', '')
            print(str(filepaths) + '\n')

            print('icon location: ')
            icon_location = self.file.read(12)
            print(str(icon_location)+ '\n')
            # icon_location = icon_location.decode('utf16', 'ignore')
            # icon_location = icon_location.replace('\x00', '')
            # print(str(icon_location) + '\n')

        return filepaths

    def section_three(self):
        print('####################################################################################')
        print('section 3')
        # section one path information num
        # self.file.seek(self.size)

        # section one path information num
        self.file.seek(self.size)
        self.path_num = struct.unpack_from('<i', self.file.read(4))[0]
        print(self.path_num)

        for i in range(0, self.path_num):
            print('count: ' + str(i + 1))

            path_length = self.file.read(2)
            print(path_length)
            b = (b'\x00\x00')
            path_length = path_length + b
            path_length = struct.unpack('<i', path_length)[0]
            path_length = path_length * 2
            print('len1: ' + str(path_length))

            print('path information :')
            filepaths = self.file.read(path_length)
            filepaths = filepaths.decode('utf16', 'ignore')
            filepaths = filepaths.replace('\x00', '')
            print(str(filepaths) + '\n')

            print('icon location: ')
            icon_location = self.file.read(12)
            print(str(icon_location)+ '\n')
            # icon_location = icon_location.decode('utf16', 'ignore')
            # icon_location = icon_location.replace('\x00', '')
            # print(str(icon_location) + '\n')

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
