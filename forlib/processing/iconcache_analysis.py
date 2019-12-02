import struct
import json
import binascii
import forlib.calc_hash as calc_hash


class IconcacheAnalysis:
    def __init__(self, file, path, hash_v):
        self.file = file
        self.path = path
        self.size = None
        self.signature = None
        self.path_num = None
        #Section 1 Use to see if it is used
        self.check_one = False
        #Save the last position of section 1
        self.tell_one = None
        self.check_two = False
        self.tell_two = None
        self.__hash_value = [hash_v]
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
            print('not supported version')
            return -1

        return json_list

    def __section_one(self):
        json_list = []

        # file size
        self.file.seek(0)
        self.size = struct.unpack_from('<I', self.file.read(4))[0]

        # section one path information num
        self.file.seek(self.size)
        self.path_num = struct.unpack_from('<i', self.file.read(4))[0]
        icon_obj = {"section one path num": self.path_num}
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

        self.check_one = True
        self.tell_one = self.file.tell()

        return json_list


    def __section_two(self):
        json_list = []

        if self.check_one == False:
            print('Section 1 must be turned first.')
            return -1

        # section two path information num
        self.file.seek(self.tell_one)
        self.path_num = struct.unpack_from('<i', self.file.read(4))[0]
        icon_obj = {"section two path num": self.path_num}
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

        self.check_two = True
        self.tell_two = self.file.tell()

        return json_list

    def __section_three(self):
        json_list = []

        if self.check_two == False:
            print('Section 2 must be turned first.')
            return -1

        # section three path information num
        self.file.seek(self.tell_two)
        self.path_num = struct.unpack_from('<i', self.file.read(4))[0]
        icon_obj = {"section three path num": self.path_num}
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

        # calculate hash value after parsing
    def __cal_hash(self):
        self.__hash_value.append(calc_hash.get_hash(self.path))

    def show_all_info(self):
        info = dict()
        info_list = []

        info["file version"] = self.__file_version()[0]["File Version"]
        section_one = self.__section_one()
        info["section one path num"] = section_one[0]["section one path num"]
        for i in range(1, len(section_one)):
            info["Section One Path" + str(i)] = section_one[i]['Path']
            info["Section One Icon image location"+str(i)] = section_one[i]['Icon image location']
        section_two = self.__section_two()
        info["section two path num"] = section_two[0]["section two path num"]
        for i in range(1, len(section_two)):
            info["Section Two Path" + str(i)] = section_two[i]['Path']
            info["Section Two Icon image location" + str(i)] = section_two[i]['Icon image location']
        section_three = self.__section_three()
        info["section three path num"] = section_three[0]["section three path num"]
        for i in range(1, len(section_three)):
            info["Section Three Path" + str(i)] = section_three[i]['Path']
            info["Section Three Icon image location" + str(i)] = section_three[i]['Icon image location']
        self.__cal_hash()
        info['before_sha1'] = self.__hash_value[0]['sha1']
        info['before_md5'] = self.__hash_value[0]['md5']
        info['after_sha1'] = self.__hash_value[1]['sha1']
        info['after_md5'] = self.__hash_value[1]['md5']

        print(info)
        info_list.append(info)

        return info_list

    def get_all_info(self):
        info = dict()
        info_list = []

        info["file version"] = self.__file_version()[0]["File Version"]
        section_one = self.__section_one()
        section_one = self.__section_one()
        info["section one path num"] = section_one[0]["section one path num"]
        for i in range(1, len(section_one)):
            info["Section One Path" + str(i)] = section_one[i]['Path']
            info["Section One Icon image location" + str(i)] = section_one[i]['Icon image location']
        section_two = self.__section_two()
        info["section two path num"] = section_two[0]["section two path num"]
        for i in range(1, len(section_two)):
            info["Section Two Path" + str(i)] = section_two[i]['Path']
            info["Section Two Icon image location" + str(i)] = section_two[i]['Icon image location']
        section_three = self.__section_three()
        info["section three path num"] = section_three[0]["section three path num"]
        for i in range(1, len(section_three)):
            info["Section Three Path" + str(i)] = section_three[i]['Path']
            info["Section Three Icon image location" + str(i)] = section_three[i]['Icon image location']
        self.__cal_hash()
        info['before_sha1'] = self.__hash_value[0]['sha1']
        info['before_md5'] = self.__hash_value[0]['md5']
        info['after_sha1'] = self.__hash_value[1]['sha1']
        info['after_md5'] = self.__hash_value[1]['md5']

        info_list.append(info)

        return info_list

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
