import struct
import json
import binascii
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
        json_list = []

        # file size
        self.file.seek(0)
        self.size = struct.unpack_from('<I', self.file.read(4))[0]

        # section one path information num
        self.file.seek(self.size)
        self.path_num = struct.unpack_from('<i', self.file.read(4))[0]
        icon_obj = {"section one path num: ": self.path_num}
        print(json.dumps(icon_obj))
        json_list.append(icon_obj)

        # path information
        for i in range(0, self.path_num):

            self.signature = self.file.read(2)

            path_length = self.file.read(2)
            b = (b'\x00\x00')
            path_length = path_length + b
            path_length = struct.unpack('<i', path_length)[0]
            sig_chek_list = [b'"\x00', b'\x02\x00', b'\x42\x00']
            if self.signature in sig_chek_list:
                path_length = path_length
            else:
                path_length = path_length * 2

            filepaths = self.file.read(path_length)
            filepaths = filepaths.decode('utf16', 'ignore')
            filepaths = filepaths.replace('\x00', '')

            icon_location = self.file.read(4)
            icon_location = str(binascii.hexlify(icon_location))

            icon_obj = {
                "Num": i + 1,
                "Path": filepaths,
                "Icon image location": icon_location
                }
            print(json.dumps(icon_obj))
            json_list.append(icon_obj)

        return json_list


    def section_two(self):

        print('section 2')
        json_list = []

        # section two path information num
        self.path_num = struct.unpack_from('<i', self.file.read(4))[0]
        icon_obj = {"section two path num: ": self.path_num}
        print(json.dumps(icon_obj))
        json_list.append(icon_obj)

        for i in range(0, self.path_num):

            path_length = self.file.read(2)
            b = (b'\x00\x00')
            path_length = path_length + b
            path_length = struct.unpack('<i', path_length)[0]
            path_length = path_length * 2

            filepaths = self.file.read(path_length)
            filepaths = filepaths.decode('utf16', 'ignore')
            filepaths = filepaths.replace('\x00', '')

            icon_location = self.file.read(12)
            icon_location = str(binascii.hexlify(icon_location))

            icon_obj = {
                "Num": i+1,
                "Path": filepaths,
                "Icon image location": icon_location,
            }
            print(json.dumps(icon_obj))
            json_list.append(icon_obj)

        return json_list

    def section_three(self):

        print('section 3')
        json_list = []

        # section three path information num
        self.path_num = struct.unpack_from('<i', self.file.read(4))[0]
        icon_obj = {"section three path num: ": self.path_num}
        print(json.dumps(icon_obj))
        json_list.append(icon_obj)

        for i in range(0, self.path_num):
            path_length = self.file.read(2)
            b = (b'\x00\x00')
            path_length = path_length + b
            path_length = struct.unpack('<i', path_length)[0]
            path_length = path_length * 2

            filepaths = self.file.read(path_length)
            filepaths = filepaths.decode('utf16', 'ignore')
            filepaths = filepaths.replace('\x00', '')

            icon_location = self.file.read(12)
            icon_location = str(binascii.hexlify(icon_location))

            icon_obj = {
                "Num": i + 1,
                "Path": filepaths,
                "Icon image location": icon_location,
            }
            print(json.dumps(icon_obj))
            json_list.append(icon_obj)

        return json_list

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