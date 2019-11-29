from datetime import datetime, timedelta
import os
import struct
import json


class PrefetchAnalysis:

    def __init__(self, file, path):
        self.file = file
        self.path = path
        self.file.seek(0)
        self.file_version = struct.unpack_from('<I', self.file.read(4))[0]

    def convert_time(self, time):
        time = '%016x' % time
        time = int(time, 16) / 10.
        time = datetime(1601, 1, 1) + timedelta(microseconds=time) + timedelta(hours=9)
        return time

    def file_name(self):
        json_list = []
        self.file.seek(16)
        executable_file_name = self.file.read(58)
        executable_file_name = executable_file_name.decode('utf16', 'ignore')
        executable_file_name = executable_file_name.replace('\x00', '')
        pf_obj = {"Executable File Name: ": str(executable_file_name)}
        json.dumps(pf_obj)
        json_list.append(pf_obj)

        return json_list

    def file_list(self):
        json_list = []
        self.file.seek(100)
        file_list_offset = struct.unpack_from('<I', self.file.read(4))[0]
        file_list_size = struct.unpack_from('<I', self.file.read(4))[0]
        resource = []
        self.file.seek(file_list_offset)
        filenames = self.file.read(file_list_size)
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

    def metadata_info(self):
        json_list = []
        self.file.seek(108)
        metadata_info_offset = struct.unpack_from('<I', self.file.read(4))[0]
        num_metadata_record = struct.unpack_from('<I', self.file.read(4))[0]

        self.file.seek(metadata_info_offset)
        volume_device_path_off = struct.unpack_from('<I', self.file.read(4))[0]
        volume_device_path_off = metadata_info_offset + volume_device_path_off
        volume_device_path_length = struct.unpack_from('<I', self.file.read(4))[0]
        volume_device_path_length = volume_device_path_length * 2
        volume_creation_time = struct.unpack_from("<Q", self.file.read(8))[0]
        volume_creation_time = self.convert_time(volume_creation_time)
        volume_serial_num = struct.unpack_from('<I', self.file.read(4))[0]

        self.file.seek(volume_device_path_off)
        volume_device_path = self.file.read(volume_device_path_length)
        volume_device_path = volume_device_path.decode('utf16', 'ignore')
        volume_device_path = volume_device_path.replace('\x00', '')

        pf_obj = {"Num Metadata Records: ": str(num_metadata_record),
                  "Volume Device Path": str(volume_device_path),
                  "Volume Creation Time": str(volume_creation_time),
                  "TimeZone": 'UTC +9',
                  "Volume Serial Num": str(volume_serial_num)}
        json.dumps(pf_obj)
        json_list.append(pf_obj)

        return json_list


    def last_launch_time(self):
        json_list = []
        self.file.seek(128)
        if self.file_version == 23:
            end = 1
        else:
            end = 8

        for i in range(0, end):
            last_launch_time = struct.unpack_from("<Q", self.file.read(8))[0]
            last_launch_time = self.convert_time(last_launch_time)
            pf_obj = {"File Last Launch Time: ": str(last_launch_time),
                      "TimeZone": 'UTC +9'}
            json.dumps(pf_obj)
            json_list.append(pf_obj)

        return json_list

    def create_time(self):
        json_list = []
        c_time = datetime.fromtimestamp(os.path.getctime(self.path))
        pf_obj = {"File Create Time: ": str(c_time),
                  "TimeZone": 'UTC +9'}
        json.dumps(pf_obj)
        json_list.append(pf_obj)

        return json_list

    def write_time(self):
        json_list = []
        w_time = datetime.fromtimestamp(os.path.getmtime(self.path))
        pf_obj = {"File Write Time: ": str(w_time),
                  "TimeZone": 'UTC +9'}
        json.dumps(pf_obj)
        json_list.append(pf_obj)

        return json_list

    def num_launch(self):
        json_list = []
        if self.file_version == 23:
            self.file.seek(152)
        elif self.file_version == 30:
            self.file.seek(208)

        num_launch = struct.unpack_from('<I', self.file.read(4))[0]
        pf_obj = {"File Run Count: ": str(num_launch)}
        json.dumps(pf_obj)
        json_list.append(pf_obj)

        return json_list

    def get_all_info(self):
        info_list = []
        info = dict()
        info["executable file name"] = str(self.file_name())
        info["last launch time"] = str(self.last_launch_time())
        info["create time"] = str(self.create_time())
        info["write time"] = str(self.write_time())
        info["num launch"] = str(self.num_launch())
        info["file list"] = str(self.file_list())
        info["metadata info"] = str(self.metadata_info())

        info_list.append(info)

        return info_list

    def show_all_info(self):
        info_list = []
        info = dict()
        info["executable file name"] = str(self.file_name())
        info["last launch time"] = str(self.last_launch_time())
        info["create time"] = str(self.create_time())
        info["write time"] = str(self.write_time())
        info["num launch"] = str(self.num_launch())
        info["file list"] = str(self.file_list())
        info["metadata info"] = str(self.metadata_info())

        print(info)
        info_list.append(info)

        return info_list

    # Use when you only want to see files with certain extensions.
    def extension_filter_pf(self, extension):
        extension = extension
        result = []

        file_list = self.file_list()
        for i in range(0, len(file_list)-1):
            json_info = file_list[i]
            path = json_info.get("Ref_file")
            if extension in path:
                result.append(file_list[i])

        if result:
            print(result)
            return result
        print('There is no file list with this extension..')
        return result
