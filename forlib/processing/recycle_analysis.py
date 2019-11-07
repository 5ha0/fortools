import struct
import binascii
from datetime import datetime
from datetime import timedelta

class RecycleAnalysis:
    def __init__(self, file):
        self.file = file


    def header(self):
        self.file.seek(0)
        fileheader = self.file.read(8)
        fileheader = binascii.hexlify(fileheader).decode('ascii')
        print('File Header: ' + fileheader)

    def size(self):
        self.file.seek(8)
        file_size = struct.unpack('<i', self.file.read(4))[0] + struct.unpack('<i', self.file.read(4))[0]
        print('Original File Size: '+str(file_size))

    def time(self):
        self.file.seek(16)
        filedatetime = struct.unpack_from('<q', self.file.read(8))[0]
        filedatetime = '%016x' %filedatetime
        filedatetime = int(filedatetime,16)/10.
        filedatetime = datetime(1601, 1, 1) + timedelta(microseconds=filedatetime)+timedelta(hours=9)
        print('File Deleted Time: ' + str(filedatetime) + '+ UTC+9:00')


    def path(self):
        self.file.seek(24)
        path = str(self.file.read(), 'cp1252')
        path = path.replace('\x00', '').encode('', 'ignore').decode('cp949', 'ignore')
        print('Original File Path: ' + path)

    def show_all_info(self):
        info_list = []
        info = dict()
        info["file header"] = str(self.header())
        info["original file size"] = str(self.size())
        info["file deleted time"] = str(self.time())
        info["original file path"] = str(self.path())

        print(info)
        info_list.append(info)
        return info_list
