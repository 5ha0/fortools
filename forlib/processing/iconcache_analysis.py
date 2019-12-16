# This is only analysis IconCache.db File- #
import os
import struct
import json
import binascii
from collections import Counter
import forlib.calc_hash as calc_hash


class IconcacheAnalysis:
    def __init__(self, file, path, hash_v):
        self.__file = file
        self.__path = path
        self.__size = None
        self.__signature = None
        self.__path_num = None
        #Save the last position of section 1
        self.__tell_one = None
        #Save the last position of section 2
        self.__tell_two = None
        self.__hash_value = [hash_v]
        self.__icon_json = self.__make_json()
        self.__cal_hash()
        self.Favorite = Favorite(self.__icon_json)

    def __file_version(self):
        json_list = []
        self.__file.seek(12)
        build_num = self.__file.read(4)
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
        self.__file.seek(0)
        self.__size = struct.unpack_from('<I', self.__file.read(4))[0]

        # section one path information num
        self.__file.seek(self.__size)
        self.__path_num = struct.unpack_from('<i', self.__file.read(4))[0]
        icon_obj = {"Section One Path Num": self.__path_num}
        json.dumps(icon_obj)
        json_list.append(icon_obj)

        # path information
        for i in range(0, self.__path_num):

            self.__signature = self.__file.read(2)

            path_length = self.__file.read(2)
            b = (b'\x00\x00')
            path_length = path_length + b
            path_length = struct.unpack('<i', path_length)[0]
            sig_chek_list = [b'"\x00', b'\x02\x00', b'\x42\x00']
            if self.__signature in sig_chek_list:
                path_length = path_length
            else:
                path_length = path_length * 2

            filepaths = self.__file.read(path_length)
            filepaths = filepaths.decode('utf16', 'ignore')
            filepaths = filepaths.replace('\x00', '')

            icon_location = self.__file.read(4)
            icon_location = str(binascii.hexlify(icon_location))

            # num indicates the order in which the paths are located
            icon_obj = {
                "Index"+str(i): 'section one',
                "Path": filepaths,
                "Icon image location": icon_location,
                }
            json.dumps(icon_obj)
            json_list.append(icon_obj)

        self.__tell_one = self.__file.tell()

        return json_list


    def __section_two(self):
        json_list = []

        # section two path information num
        self.__file.seek(self.__tell_one)
        self.__path_num = struct.unpack_from('<i', self.__file.read(4))[0]
        icon_obj = {"Section Two Path Num": self.__path_num}
        json.dumps(icon_obj)
        json_list.append(icon_obj)

        for i in range(0, self.__path_num):

            path_length = self.__file.read(2)
            b = (b'\x00\x00')
            path_length = path_length + b
            path_length = struct.unpack('<i', path_length)[0]
            path_length = path_length * 2

            filepaths = self.__file.read(path_length)
            filepaths = filepaths.decode('utf16', 'ignore')
            filepaths = filepaths.replace('\x00', '')

            icon_location = self.__file.read(12)
            icon_location = str(binascii.hexlify(icon_location))

            # num indicates the order in which the paths are located
            icon_obj = {
                "Index"+str(i): 'section two',
                "Path": filepaths,
                "Icon image location": icon_location,
            }
            json.dumps(icon_obj)
            json_list.append(icon_obj)

        self.__tell_two = self.__file.tell()

        return json_list

    def __section_three(self):
        json_list = []
        icon_obj = dict()

        # section three path information num
        self.__file.seek(self.__tell_two)
        self.__path_num = struct.unpack_from('<i', self.__file.read(4))[0]
        icon_obj["Section Three Path Num"] = self.__path_num
        json.dumps(icon_obj)
        json_list.append(icon_obj)

        for i in range(0, self.__path_num):
            path_length = self.__file.read(2)
            b = (b'\x00\x00')
            path_length = path_length + b
            path_length = struct.unpack('<i', path_length)[0]
            path_length = path_length * 2

            filepaths = self.__file.read(path_length)
            filepaths = filepaths.decode('utf16', 'ignore')
            filepaths = filepaths.replace('\x00', '')

            icon_location = self.__file.read(12)
            icon_location = str(binascii.hexlify(icon_location))

            # num indicates the order in which the paths are located
            icon_obj = {
                "Index"+str(i): 'section three',
                "Path": filepaths,
                "Icon image location": icon_location,
            }
            json.dumps(icon_obj)
            json_list.append(icon_obj)

        return json_list

    # calculate hash value after parsing
    def __cal_hash(self):
        self.__hash_value.append(calc_hash.get_hash(self.__path, 'after'))

    def get_hash(self):
        return self.__hash_value

    def __make_json(self):
        info = dict()
        info_list = []

        info["File Version"] = self.__file_version()[0]["File Version"]
        section_one = self.__section_one()
        info["Section One Path Num"] = section_one[0]["Section One Path Num"]
        for i in range(1, len(section_one)):
            info["Section One Path" + str(i)] = section_one[i]['Path']
            info["Section One Icon image location" + str(i)] = section_one[i]['Icon image location']
        section_two = self.__section_two()
        info["Section Two Path Num"] = section_two[0]["Section Two Path Num"]
        for i in range(1, len(section_two)):
            info["Section Two Path" + str(i)] = section_two[i]['Path']
            info["Section Two Icon image location" + str(i)] = section_two[i]['Icon image location']
        section_three = self.__section_three()
        info["Section Three Path Num"] = section_three[0]["Section Three Path Num"]
        for i in range(1, len(section_three)):
            info["Section Three Path" + str(i)] = section_three[i]['Path']
            info["Section Three Icon image location" + str(i)] = section_three[i]['Icon image location']

        info_list.append(info)

        return info_list

    def show_all_info(self):
        for i in range(0, len(self.__icon_json)):
            print(self.__icon_json[i])

    def get_all_info(self):
        return self.__icon_json


# This class shows the information that processed the entire data.
class Favorite:
    def __init__(self, json):
        self.__icon_json = json

    # For the convenience of users, only the information of the desired section is displayed.
    def show_info_by_section(self, lists):
        info = dict()
        result_list = []
        icon_info = self.__icon_json
        for i in lists:
            i = int(i)
            if i == 1:
                info["Section One Path Num"] = self.__icon_json[0]["Section One Path Num"]
                end = self.__icon_json[0]["Section One Path Num"]
                end  = int(end)
                for i in range(1, end+1):
                    info["Section One Path" + str(i)] = self.__icon_json[0]["Section One Path" + str(i)]
                    info["Section One Icon image location" + str(i)] = self.__icon_json[0]["Section One Icon image location" + str(i)]
            elif i == 2:
                info["Section Two Path Num"] = self.__icon_json[0]["Section Two Path Num"]
                end = self.__icon_json[0]["Section Two Path Num"]
                end = int(end)
                for i in range(1, end+1):
                    info["Section Two Path" + str(i)] = self.__icon_json[0]["Section Two Path" + str(i)]
                    info["Section Two Icon image location" + str(i)] = self.__icon_json[0]["Section Two Icon image location" + str(i)]
            elif i == 3:
                info["Section Three Path Num"] = self.__icon_json[0]["Section Three Path Num"]
                end = self.__icon_json[0]["Section Three Path Num"]
                end = int(end)
                for i in range(1, end+1):
                    info["Section Three Path" + str(i)] = self.__icon_json[0]["Section Three Path" + str(i)]
                    info["Section Three Icon image location" + str(i)] = self.__icon_json[0]["Section Three Icon image location" + str(i)]

        print(info)

    # Shows the extension information for all sections of the path information and the number of each extension.
    def show_kind_of_extension(self):
        result = []
        info = dict()
        extension_list = []

        end = self.__icon_json[0]["Section One Path Num"]
        end = int(end)
        for i in range(1, end + 1):
            value = self.__icon_json[0]["Section One Path" + str(i)]
            lower_value = value.lower()
            lower_value = lower_value.split('.')[-1]
            extension_list.append(lower_value)
        end = self.__icon_json[0]["Section Two Path Num"]
        end = int(end)
        for i in range(1, end + 1):
            value = self.__icon_json[0]["Section Two Path" + str(i)]
            lower_value = value.lower()
            lower_value = value.split('.')[-1]
            extension_list.append(lower_value)
        end = self.__icon_json[0]["Section Three Path Num"]
        end = int(end)
        for i in range(1, end + 1):
            value = self.__icon_json[0]["Section Three Path" + str(i)]
            lower_value = value.lower()
            lower_value = value.split('.')[-1]
            extension_list.append(lower_value)

        result = Counter(extension_list)
        print('The result of analyzing only path keys.')
        for key in result:
            print(key + str(': ') + str(result[key]))

    # The path information in all sections shows the drive type information and the number of each drive type.
    def show_kind_of_dirvetype(self):
        result = []
        info = dict()
        extension_list = []

        end = self.__icon_json[0]["Section One Path Num"]
        end = int(end)
        for i in range(1, end + 1):
            value = self.__icon_json[0]["Section One Path" + str(i)]
            lower_value = value.lower()
            if os.path.isabs(lower_value) == True:
                if ':' in lower_value:
                    lower_value = os.path.splitdrive(lower_value)
                    extension_list.append(lower_value[0])
        end = self.__icon_json[0]["Section Two Path Num"]
        end = int(end)
        for i in range(1, end + 1):
            value = self.__icon_json[0]["Section Two Path" + str(i)]
            lower_value = value.lower()
            if os.path.isabs(lower_value) == True:
                if ':' in lower_value:
                    lower_value = os.path.splitdrive(lower_value)
                    extension_list.append(lower_value[0])
        end = self.__icon_json[0]["Section Three Path Num"]
        end = int(end)
        for i in range(1, end + 1):
            value = self.__icon_json[0]["Section Three Path" + str(i)]
            lower_value = value.lower()
            if os.path.isabs(lower_value) == True:
                if ':' in lower_value:
                    lower_value = os.path.splitdrive(lower_value)
                    extension_list.append(lower_value[0])

        result = Counter(extension_list)
        print('The result of analyzing only path keys.')
        for key in result:
            print (key, result[key])

