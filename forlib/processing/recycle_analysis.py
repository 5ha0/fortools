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
        self.file = file
        self.path = path
        self.__hash_value = [hash_v]

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
        rc_obj = {"File Deleted Time": str(filedatetime),
                  "Time Zone": 'UTC +9'}
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

    # calculate hash value after parsing
    def __cal_hash(self):
        self.__hash_value.append(calc_hash.get_hash(self.path))

    def show_all_info(self):
        info_list = []
        temp = dict()

        temp['$I Name'] = self.__i_name()[0]['$I Name']
        temp['File Header'] = self.__header()[0]['File Header']
        temp['Original File Size'] = self.__size()[0]['Original File Size']
        temp['File Deleted Time'] = self.__time()[0]['File Deleted Time']
        temp['Time Zone'] = self.__time()[0]['Time Zone']
        temp['Original File Path'] = self.__original_path()[0]['Original File Path']
        self.__cal_hash()
        temp['before_sha1'] = self.__hash_value[0]['sha1']
        temp['before_md5'] = self.__hash_value[0]['md5']
        temp['after_sha1'] = self.__hash_value[1]['sha1']
        temp['after_md5'] = self.__hash_value[1]['md5']

        print(temp)
        info_list.append(temp)

        return info_list

    def get_all_info(self):
        info_list = []
        temp = dict()

        temp['$I Name'] = self.__i_name()[0]['$I Name']
        temp['File Header'] = self.__header()[0]['File Header']
        temp['Original File Size'] = self.__size()[0]['Original File Size']
        temp['File Deleted Time'] = self.__time()[0]['File Deleted Time']
        temp['Time Zone'] = self.__time()[0]['Time Zone']
        temp['Original File Path'] = self.__original_path()[0]['Original File Path']
        self.__cal_hash()
        temp['before_sha1'] = self.__hash_value[0]['sha1']
        temp['before_md5'] = self.__hash_value[0]['md5']
        temp['after_sha1'] = self.__hash_value[1]['sha1']
        temp['after_md5'] = self.__hash_value[1]['md5']

        info_list.append(temp)

        return info_list