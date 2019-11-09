from datetime import datetime, timedelta
import os
import struct
import json


class PrefetchAnalysis:

    def __init__(self, file, path):
        self.file = file
        self.path = path

    def file_name(self):
        self.file.seek(16)
        file_name = self.file.read(58)
        file_name = file_name.decode('utf16', 'ignore')
        file_name = file_name.replace('\x00', '')
        print('Executable File Name: ' + file_name)

        return file_name

    def last_run_time(self):
        self.file.seek(128)
        time = struct.unpack_from("<Q", self.file.read(8))[0]
        time = '%016x' % time
        time = int(time, 16) / 10.
        last_run_time = datetime(1601, 1, 1) + timedelta(microseconds=time) + timedelta(hours=9)
        print("File Last Run Time: " + str(last_run_time) + ' UTC+9:00')

        return last_run_time

    def create_time(self):
        c_time = datetime.fromtimestamp(os.path.getctime(self.path))
        print('File Create Time: ' + str(c_time) + ' UTC+9:00')

        return c_time

    def write_time(self):
        w_time = datetime.fromtimestamp(os.path.getmtime(self.path))
        print('File Write Time: ' + str(w_time) + ' UTC+9:00')

        return w_time

    def num_launch(self):
        self.file.seek(0)
        version = struct.unpack_from('<I', self.file.read(4))[0]
        if version == 23:
            self.file.seek(152)
        elif version == 30:
            self.file.seek(208)

        num_launch = struct.unpack_from('<I', self.file.read(4))[0]
        print('File Run Count:' + str(num_launch))

        return num_launch

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
            print(json.dumps(pf_obj))
            json_list.append(pf_obj)

        return json_list

    def show_all_info(self):
        info_list = []
        info = dict()
        info["file name"] = str(self.file_name())
        info["last run time"] = str(self.last_run_time())
        info["create time"] = str(self.create_time())
        info["write time"] = str(self.write_time())
        info["num launch"] = str(self.num_launch())
        info["file list"] = str(self.file_list())

        print(info)
        info_list.append(info)
        return info_list

#
# class Favorite:
#
#     def __init__(self, file):
#         self._result = []
#         self.file = file
#
#     def time_stamp(self):
#         l_time = PrefetchAnalysis.last_run_time()
#         c_time = PrefetchAnalysis.create_time()
#         w_time = PrefetchAnalysis.write_time()
#
#         info = dict()
#         info["last run time"] = l_time
#         info["create time"] = c_time
#         info["write time"] = w_time
#         self._result.append(info)
#
#         return self._result
#
#     def reference(self):
#         reference1 = PrefetchAnalysis.num_launch()
#         reference2 = PrefetchAnalysis.file_list()
#
#         info = dict()
#         info["num launch"] = reference1
#         info["referenced file list"] = reference2
#         self._result.append(info)
#
#         return self._result
#
#     # Only files with the desired extensions are visible.
#     def find_extension(self):
#         self.file.seek(100)
#         file_list_offset = struct.unpack_from('<I', self.file.read(4))[0]
#         file_list_size = struct.unpack_from('<I', self.file.read(4))[0]
#         resource = []
#         self.file.seek(file_list_offset)
#         filenames = self.file.read(file_list_size)
#         filenames = filenames.decode('cp1252')
#         for i in filenames.split('\x00\x00'):
#             resource.append(i.replace('\x00', ''))
#         want_file = []
#         for i in resource:
#             if '.EXE' in resource[i]:
#                 want_file = resource[i]
#                 print(resource[i])
#
