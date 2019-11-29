# This is only analysis Recycle Bin $I File- #
import struct
import binascii
import os
from datetime import datetime
from datetime import timedelta
import json

class RecycleAnalysis:
    def __init__(self, file, path):
        self.file = file
        self.path = path

    def __i_name(self):
        json_list = []
        name = os.path.basename(self.path)
        rc_obj = {"$I Name": str(name)}
        json.dumps(rc_obj)
        json_list.append(rc_obj)

        return json_list

    def __header(self):
        json_list = []
        self.file.seek(0)
        fileheader = self.file.read(8)
        fileheader = binascii.hexlify(fileheader).decode('ascii')
        rc_obj = {"File Header": str(fileheader)}
        json.dumps(rc_obj)
        json_list.append(rc_obj)

        return json_list

    def __size(self):
        json_list = []
        self.file.seek(8)
        file_size = struct.unpack('<i', self.file.read(4))[0] + struct.unpack('<i', self.file.read(4))[0]
        rc_obj = {"Original File Size": str(file_size)}
        json.dumps(rc_obj)
        json_list.append(rc_obj)

        return json_list

    def __time(self):
        json_list = []
        self.file.seek(16)
        filedatetime = struct.unpack_from('<q', self.file.read(8))[0]
        filedatetime = '%016x' %filedatetime
        filedatetime = int(filedatetime,16)/10.
        filedatetime = datetime(1601, 1, 1) + timedelta(microseconds=filedatetime)+timedelta(hours=9)
        rc_obj = {"File Deleted Time": str(filedatetime)}
        json.dumps(rc_obj)
        json_list.append(rc_obj)

        return json_list

    def __original_path(self):
        json_list = []
        self.file.seek(24)
        path = str(self.file.read(), 'cp1252')
        path = path.replace('\x00', '').encode('utf-8', 'ignore').decode('cp949', 'ignore')
        rc_obj = {"Original File Path": str(path)}
        json.dumps(rc_obj)
        json_list.append(rc_obj)

        return json_list

    def show_all_info(self):
        info_list = []
        info = dict()
        info["$I Name"] = str(self.__i_name())
        info["File Header"] = str(self.__header())
        info["Original File Size"] = str(self.__size())
        info["File Deleted Time"] = str(self.__time())
        info["Time Zone"] = 'UTC +09:00'
        info["Original File Path"] = str(self.__original_path())

        info_list.append(info)
        print(info)

        return info_list

    def get_all_info(self):
        info_list = []
        info = dict()
        info["$I Name"] = str(self.__i_name())
        info["File Header"] = str(self.__header())
        info["Original File Size"] = str(self.__size())
        info["File Deleted Time"] = str(self.__time())
        info["Time Zone"] = 'UTC +09:00'
        info["Original File Path"] = str(self.__original_path())

        info_list.append(info)

        return info_list
