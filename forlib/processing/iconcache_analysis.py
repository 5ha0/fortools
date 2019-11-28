import struct
import json
import binascii
import os
from datetime import datetime
from forlib.processing.filter import *

class IconcacheAnalysis:
    def __init__(self, file):
        self.file = file
        self.size = None
        self.signature = None
        self.path_num = None
        self.time = 1
        self.info_list = self.show_all_info()
        self.drive_exe_list = None
        self.hard_disk_delete = ["Disk Wipe", 'Drive Wipe', 'DBAN', 'CBL Data Shredder', 'MHDD', 'PCDiskEraser', 'KillDisk', 'Format Command With Write Zero Option', 'Macrorit Data Wiper', 'Eraser', 'WipeDisk', 'MiniTool Partition Wizard', 'KillDisk', 'CCleaner', 'PCDiskEraser', 'Super File Shredder']

    def __file_version(self):
        json_list = []
        self.file.seek(12)
        build_num = self.file.read(4)
        if build_num == b'\xB1\x1D\x01\x06':
            icon_obj = {"File Version": 'win 7'}
            json.dumps(icon_obj)
            json_list.append(icon_obj)
        elif build_num == b'\x5A\x29\x00\x00':
            icon_obj = {"File Version": 'win 10'}
            json.dumps(icon_obj)
            json_list.append(icon_obj)
        else:
            return print('not supported version')

        return json_list

    def __section_one(self):
        json_list = []

        # file size
        self.file.seek(0)
        self.size = struct.unpack_from('<I', self.file.read(4))[0]

        # section one path information num
        self.file.seek(self.size)
        self.path_num = struct.unpack_from('<i', self.file.read(4))[0]
        icon_obj = {"section one path num: ": self.path_num}
        json.dumps(icon_obj)
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

            # num indicates the order in which the paths are located
            icon_obj = {
                "Num": i + 1,
                "Path": filepaths,
                "Icon image location": icon_location,
                }
            json.dumps(icon_obj)
            json_list.append(icon_obj)

        return json_list


    def __section_two(self):
        json_list = []

        # section two path information num
        self.path_num = struct.unpack_from('<i', self.file.read(4))[0]
        icon_obj = {"section two path num: ": self.path_num}
        json.dumps(icon_obj)
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

            # num indicates the order in which the paths are located
            icon_obj = {
                "Num": i+1,
                "Path": filepaths,
                "Icon image location": icon_location,
            }
            json.dumps(icon_obj)
            json_list.append(icon_obj)

        return json_list

    def __section_three(self):
        json_list = []

        # section three path information num
        self.path_num = struct.unpack_from('<i', self.file.read(4))[0]
        icon_obj = {"section three path num: ": self.path_num}
        json.dumps(icon_obj)
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

            # num indicates the order in which the paths are located
            icon_obj = {
                "Num": i + 1,
                "Path": filepaths,
                "Icon image location": icon_location,
            }
            json.dumps(icon_obj)
            json_list.append(icon_obj)

        return json_list

    def show_all_info(self):
        self.info_list = []
        info = dict()
        info["file version"] = str(self.__file_version())
        info["path information_section one"] = str(self.__section_one())
        info["path information_section two"] = str(self.__section_two())
        info["path information_section three"] = str(self.__section_three())

        print(info)
        self.info_list.append(info)

        return self.info_list

    def get_all_info(self):
        self.info_list = []
        info = dict()
        info["file version"] = str(self.__file_version())
        info["path information_section one"] = str(self.__section_one())
        info["path information_section two"] = str(self.__section_two())
        info["path information_section three"] = str(self.__section_three())

        self.info_list.append(info)

        return self.info_list

    # Use when you only want to see files with certain extensions.
    def extension_filter(self, extension):
        extension = extension
        result = []

        for i in range(0, 3):
            if i == 0:
                section = self.__section_one()
            elif i == 1:
                section = self.__section_two()
            else:
                section = self.__section_three()
            for j in range(1, len(section)):
                json_info = section[j]
                path = json_info.get("Path")
                if extension in path:
                    result.append(section[j])
        if result:
            print(result)
            return result
        print('There is no file with this extension..')
        return result

    # if you want to know execution for drive delete program, use this
    def drive_delete_exe(self):
        hard_disk_delete = ["Disk Wipe", 'Drive Wipe', 'DBAN', 'CBL Data Shredder', 'MHDD', 'PCDiskEraser', 'KillDisk',
                            'Format Command With Write Zero Option', 'Macrorit Data Wiper', 'Eraser', 'WipeDisk',
                            'MiniTool Partition Wizard', 'KillDisk', 'CCleaner', 'PCDiskEraser', 'Super File Shredder']
        path = []
        execution = []

        for i in range(0, 3):
            if i == 0:
                section = self.__section_one()
            elif i == 1:
                section = self.__section_two()
            else:
                section = self.__section_three()
            for j in range(1, len(section)):
                json_info = section[j]
                path.append(json_info.get("Path"))

        for i in range(0, len(path)):
            if path[i] in hard_disk_delete:
                execution.append(path[i])

        if execution:
            print('This file was executed for hard disk deletion program.' + str(execution))
            return execution
        print('This file was not executed for hard disk deletion program.')
        return execution