import os.path
from struct import unpack
import struct
import binascii
from datetime import datetime
from datetime import timedelta
import string
import sys

class RecycleAnalysis:
    def __init__(self, file):
        self.file = file

    def r_header():
        self.file.seek(0)
        fileheader = self.file.read(8)
        fileheader = binascii.hexlify(fileheader).decode('ascii')
        print('File Header: ' + fileheader)

    def r_size():
        self.file.seek(8)
        file_size = struct.unpack('<i', self.file.read(4))[0] + struct.unpack('<i', self.file.read(4))[0]
        print('File Size: '+str(file_size))

        def r_time():
            self.file.seek(16)
            filedatetime = struct.unpack_from('<q', self.file.read(8))[0]
            filedatetime = '%016x' %filedatetime
            filedatetime = int(filedatetime,16)/10.
            filedatetime =  datetime(1601, 1, 1) + timedelta(microseconds=filedatetime)+timedelta(hours=9)  
            print('File Time: ' + str(filedatetime) + '+ UTC-9')


        def r_path():
            self.file.seek(24)
            path = str(self.file.read(), 'cp1252')
            path = path.replace('\x00','').encode('', 'ignore').decode('cp949', 'ignore')
            print('File Path: ' + path)
