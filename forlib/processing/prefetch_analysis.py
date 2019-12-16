from datetime import datetime, timedelta, timezone
import os
import struct
import json
from collections import Counter
import forlib.calc_hash as calc_hash
import forlib.processing.convert_time as convert_time


class PrefetchAnalysis:

    def __init__(self, file, path, hash_v):
        self.__file = file
        self.__path = path
        self.__hash_value = [hash_v]
        self.__file.seek(0)
        self.__file_version = struct.unpack_from('<I', self.__file.read(4))[0]
        self.__pf_json = self.__make_json()
        self.__cal_hash()
        self.Favorite = Favorite(self.__file_list())

    def __file_name(self):
        json_list = []
        self.__file.seek(16)
        executable_file_name = self.__file.read(58)
        executable_file_name = executable_file_name.split(bytes(b'\x00\x00\x00'))[0]
        executable_file_name = executable_file_name + bytes(b'\x00')
        executable_file_name = executable_file_name.decode('utf16', 'ignore')
        executable_file_name = executable_file_name.replace('\x00', '')

        pf_obj = {"Executable File Name": str(executable_file_name)}
        json.dumps(pf_obj)
        json_list.append(pf_obj)

        return json_list

    def __file_list(self):
        json_list = []
        self.__file.seek(100)
        file_list_offset = struct.unpack_from('<I', self.__file.read(4))[0]
        file_list_size = struct.unpack_from('<I', self.__file.read(4))[0]
        resource = []
        self.__file.seek(file_list_offset)
        filenames = self.__file.read(file_list_size)
        filenames = filenames.decode('cp1252')
        for i in filenames.split('\x00\x00'):
            resource.append(i.replace('\x00', ''))

        for i in range(0, len(resource) - 1):
            pf_obj = {
                "Num": i + 1,
                "Ref_file": resource[i]
            }
            json.dumps(pf_obj)
            json_list.append(pf_obj)

        return json_list

    def __metadata_info(self):
        json_list = []
        self.__file.seek(108)
        metadata_info_offset = struct.unpack_from('<I', self.__file.read(4))[0]
        num_metadata_record = struct.unpack_from('<I', self.__file.read(4))[0]

        self.__file.seek(metadata_info_offset)
        volume_device_path_off = struct.unpack_from('<I', self.__file.read(4))[0]
        volume_device_path_off = metadata_info_offset + volume_device_path_off
        volume_device_path_length = struct.unpack_from('<I', self.__file.read(4))[0]
        volume_device_path_length = volume_device_path_length * 2

        time = struct.unpack_from("<Q", self.__file.read(8))[0]
        time = convert_time.convert_time(time)
        volume_creation_time = time.strftime("%Y-%m-%d %H:%M:%S")
        time_zone = time.strftime('%Z')

        volume_serial_num = struct.unpack_from('<I', self.__file.read(4))[0]

        self.__file.seek(volume_device_path_off)
        volume_device_path = self.__file.read(volume_device_path_length)
        volume_device_path = volume_device_path.decode('utf16', 'ignore')
        volume_device_path = volume_device_path.replace('\x00', '')

        pf_obj = {"Num Metadata Records": str(num_metadata_record),
                  "Volume Device Path": str(volume_device_path),
                  "TimeZone": time_zone,
                  "Volume Creation Time": volume_creation_time,
                  "Volume Serial Num": str(volume_serial_num)}
        json.dumps(pf_obj)
        json_list.append(pf_obj)

        return json_list


    def __last_launch_time(self):
        json_list = []
        self.__file.seek(128)
        if self.__file_version == 23:
            end = 1
        else:
            end = 8

        for i in range(0, end):
            time = struct.unpack_from("<Q", self.__file.read(8))[0]
            time = convert_time.convert_time(time)
            last_launch_time = time.strftime("%Y-%m-%d %H:%M:%S")
            time_zone = time.strftime("%Z")

            pf_obj = {"TimeZone": time_zone,
                      "File Last Launch Time": last_launch_time}
            json.dumps(pf_obj)
            json_list.append(pf_obj)

        return json_list

    def __create_time(self):
        json_list = []
        c_time = datetime.fromtimestamp(os.path.getctime(self.__path))
        c_time = c_time.strftime("%Y-%m-%d %H:%M:%S")

        pf_obj = {"TimeZone": 'SYSTEM TIME',
                  "File Create Time": c_time}
        json.dumps(pf_obj)
        json_list.append(pf_obj)

        return json_list

    def __write_time(self):
        json_list = []
        w_time = datetime.fromtimestamp(os.path.getmtime(self.__path))
        w_time = w_time.strftime("%Y-%m-%d %H:%M:%S")

        pf_obj = {"TimeZone": 'SYSTEM TIME',
                  "File Write Time": w_time}
        json.dumps(pf_obj)
        json_list.append(pf_obj)

        return json_list

    def __num_launch(self):
        json_list = []
        if self.__file_version == 23:
            self.__file.seek(152)
        elif self.__file_version == 30:
            self.__file.seek(208)

        num_launch = struct.unpack_from('<I', self.__file.read(4))[0]
        pf_obj = {"File Run Count": str(num_launch)}
        json.dumps(pf_obj)
        json_list.append(pf_obj)

        return json_list

    # calculate hash value after parsing
    def __cal_hash(self):
        self.__hash_value.append(calc_hash.get_hash(self.__path, 'after'))

    def get_hash(self):
        return self.__hash_value

    def __make_json(self):
        info_list = []
        info = dict()
        info["Executable File Name"] = self.__file_name()[0]['Executable File Name']
        file_list = self.__file_list()
        for i in range(0, len(file_list)):
            info["Ref_file" + str(i)] = file_list[i]["Ref_file"]
        metadata_info = self.__metadata_info()
        info["Num Metadata Records"] = metadata_info[0]["Num Metadata Records"]
        info["Volume Device Path"] = metadata_info[0]["Volume Device Path"]
        info["Volume Creation TimeZone"] = metadata_info[0]["TimeZone"]
        info["Volume Creation Time"] = metadata_info[0]["Volume Creation Time"]
        info["Volume Serial Num"] = metadata_info[0]["Volume Serial Num"]
        if self.__file_version == 23:
            info["File Last Launch TimeZone"] = self.__last_launch_time()[0]["TimeZone"]
            info["File Last Launch Time"] = self.__last_launch_time()[0]["File Last Launch Time"]
        else:
            for i in range(0, 8):
                info["File Last Launch TimeZone" + str(i)] = self.__last_launch_time()[i]["TimeZone"]
                info["File Last Launch Time"+str(i)] = self.__last_launch_time()[i]["File Last Launch Time"]
        create_time = self.__create_time()
        info["File Create TimeZone"] = create_time[0]["TimeZone"]
        info["File Create Time"] = create_time[0]["File Create Time"]
        write_time = self.__write_time()
        info["File Write TimeZone"] = write_time[0]["TimeZone"]
        info["File Write Time"] = write_time[0]["File Write Time"]
        info["File Run Count"] = self.__num_launch()[0]["File Run Count"]

        info_list.append(info)

        return info_list

    def show_all_info(self):
        for i in range(0, len(self.__pf_json)):
            print(self.__pf_json[i])

    def get_all_info(self):
        return self.__pf_json


# This class shows the information that processed the entire data.
class Favorite:

    def __init__(self, json_file_list):
        self.__file_list_json = json_file_list

    # Shows the extension information for all sections of the path information and the number of each extension.
    def show_kind_of_extension(self):
        path_list = []

        for i in range(0, len(self.__file_list_json)):
            json_info = self.__file_list_json[i]
            path = json_info.get("Ref_file")
            path = path.lower()
            path = path.split('.')[-1]
            path_list.append(path)

        result = Counter(path_list)
        print('The result of analyzing only reference file keys.')
        for key in result:
            print (key + str(': ') + str(result[key]))

    # It allows you to view only reference list information out of the total information.
    def show_only_ref_path(self):
        info = dict()

        for i in range(0, len(self.__file_list_json)):
            info['Ref_file' + str(i)] = self.__file_list_json[i]['Ref_file']

        print(info)
