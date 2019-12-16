# This is only analysis Recycle Bin $I File- #
import struct
import binascii
import os
from datetime import datetime
from datetime import timedelta
import json
import forlib.calc_hash as calc_hash


class RecycleAnalysis:
    def __init__(self, file, path, hash_v):
        self.__file = file
        self.__path = path
        self.__hash_value = [hash_v]
        self.__recycle_json = self.__make_json()
        self.__cal_hash()

    def __i_name(self):
        json_list = []
        name = os.path.basename(self.__path)
        rc_obj = {"$I Name": str(name)}
        json.dumps(rc_obj)
        json_list.append(rc_obj)

        return json_list

    def __header(self):
        json_list = []
        self.__file.seek(0)
        fileheader = self.__file.read(8)
        fileheader = binascii.hexlify(fileheader).decode('ascii')
        rc_obj = {"File Header": str(fileheader)}
        json.dumps(rc_obj)
        json_list.append(rc_obj)

        return json_list

    def __size(self):
        json_list = []
        self.__file.seek(8)
        file_size = struct.unpack('<i', self.__file.read(4))[0] + struct.unpack('<i', self.__file.read(4))[0]
        rc_obj = {"Original File Size": str(file_size)}
        json.dumps(rc_obj)
        json_list.append(rc_obj)

        return json_list

    def __time(self):
        json_list = []
        self.__file.seek(16)
        filedatetime = struct.unpack_from('<q', self.__file.read(8))[0]
        filedatetime = '%016x' %filedatetime
        filedatetime = int(filedatetime,16)/10.
        filedatetime = datetime(1601, 1, 1) + timedelta(microseconds=filedatetime)
        filedatetime = filedatetime.strftime("%Y-%m-%d %H:%M:%S")
        rc_obj = {"File Deleted Time": str(filedatetime),
                  "Time Zone": 'UTC'}
        json.dumps(rc_obj)
        json_list.append(rc_obj)

        return json_list

    def __original_path(self):
        json_list = []
        self.__file.seek(24)
        path = str(self.__file.read(), 'cp1252')
        path = path.replace('\x00', '').encode('utf-8', 'ignore').decode('cp949', 'ignore')
        rc_obj = {"Original File Path": str(path)}
        json.dumps(rc_obj)
        json_list.append(rc_obj)

        return json_list

    # calculate hash value after parsing
    def __cal_hash(self):
        self.__hash_value.append(calc_hash.get_hash(self.__path, 'after'))

    def get_hash(self):
        return self.__hash_value

    def __make_json(self):
        info_list = []
        temp = dict()

        temp['$I Name'] = self.__i_name()[0]['$I Name']
        temp['File Header'] = self.__header()[0]['File Header']
        temp['Original File Size'] = self.__size()[0]['Original File Size']
        temp['File Deleted Time'] = self.__time()[0]['File Deleted Time']
        temp['Time Zone'] = self.__time()[0]['Time Zone']
        temp['Original File Path'] = self.__original_path()[0]['Original File Path']

        info_list.append(temp)

        return info_list

    def show_all_info(self):
        for i in range(0, len(self.__recycle_json)):
            print(self.__recycle_json[i])

    def get_all_info(self):
        return self.__recycle_json


