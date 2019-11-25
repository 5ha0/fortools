# This is only analysis Recycle Bin $I File- #
import struct
import binascii
import os
from datetime import datetime
from datetime import timedelta

class RecycleAnalysis:
    def __init__(self, file, path):
        self.file = file
        self.path = path

    def i_name(self):
        name = os.path.basename(self.path)
        print('$I Name: ' + str(name))

        return name

    def header(self):
        self.file.seek(0)
        fileheader = self.file.read(8)
        fileheader = binascii.hexlify(fileheader).decode('ascii')
        print('File Header: ' + fileheader)

        return fileheader

    def size(self):
        self.file.seek(8)
        file_size = struct.unpack('<i', self.file.read(4))[0] + struct.unpack('<i', self.file.read(4))[0]
        print('Original File Size: '+str(file_size))

        return file_size

    def time(self):
        self.file.seek(16)
        filedatetime = struct.unpack_from('<q', self.file.read(8))[0]
        filedatetime = '%016x' %filedatetime
        filedatetime = int(filedatetime,16)/10.
        filedatetime = datetime(1601, 1, 1) + timedelta(microseconds=filedatetime)+timedelta(hours=9)
        print('File Deleted Time: ' + str(filedatetime) + '+ UTC+9:00')

        return filedatetime


    def original_path(self):
        self.file.seek(24)
        path = str(self.file.read(), 'cp1252')
        path = path.replace('\x00', '').encode('utf-8', 'ignore').decode('cp949', 'ignore')
        print('Original File Path: ' + path)

        return path

    def show_all_info(self):
        info_list = []
        info = dict()
        info["$I name"] = str(self.i_name())
        info["file header"] = str(self.header())
        info["original file size"] = str(self.size())
        info["file deleted time"] = str(self.time())
        info["original file path"] = str(self.original_path())

        print(info)
        info_list.append(info)

        return info_list