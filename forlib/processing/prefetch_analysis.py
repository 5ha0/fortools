from argparse import ArgumentParser
import binascii
import ctypes
from datetime import datetime,timedelta
import ntpath
import os
import struct
import sys
import tempfile
import decompress



class Prefetch:
    def __init__(self,file):
        self.file = file

    def dt_from_win32_ts(timestamp):
        WIN32_EPOCH = datetime(1601, 1, 1)
        return WIN32_EPOCH + timedelta(microseconds=timestamp // 10, hours=9)  

    def pf_size(self):
        self.file.seek(12)
        size = struct.unpack_from('I', self.file.read(4))[0]
        print(size)
        return size
        
    def pf_last_run_time(self):
        self.file.seek(128)
        time = struct.unpack_from("<Q", self.file.read(8))[0]
        time = '%016x' %time
        time = int(time,16)/10.
        last_run_time =  datetime(1601, 1, 1) + timedelta(microseconds=time)+timedelta(hours=9)  
        print("File Last Run Time: " + str(last_run_time) +' UTC+9:00')
        return last_run_time

    def pf_create_time(self, path):
        time = datetime.fromtimestamp(os.path.getctime(path))
        print ('File Create Time: '+str(time) +' UTC+9:00')
        return time
    
    def pf_write_time(self, path):
        time = datetime.fromtimestamp(os.path.getmtime(path))
        print ('File Create Time: '+ str(time) +' UTC+9:00')
        return time
    
    def pf_num_launch(self):
        if version == 23:
            self.file.seek(152)
            num_launch = struct.unpack_from('I', self.file.read(4))[0]
            print('File Run Count:'+ str(num_launch))
        elif version ==30:
            self.file.seek(208)
            num_launch = struct.unpack_from('I', self.file.read(4))[0]
            print('File Run Count:'+ str(num_launch))
        return num_launch
    
    def pf_file_list():
        self.file.seek(100)
        file_list_offset=struct.unpack_from('I', self.file.read(4))[0]
        file_list_size=struct.unpack_from('I', self.file.read(4))[0]
        resource = []
        self.file.seek(file_list_offset)
        filenames = self.file.read(file_list_size)
        filenames = filenames.decode('cp1252')
        for i in filenames.split('\x00\x00'):
            resource.append(i.replace('\x00',''))

        for i in resource:
            count += 1
            pf_obj = {
                "Num" : count,
                "Ref_file" : i
            }
            print(json.dumps(pf_obj))
        return resourcce
    
class favorite:
    ##def time:
        
    def loaded_list:
        self.file.seek(100)
        file_list_offset=struct.unpack_from('I', self.file.read(4))[0]
        file_list_size=struct.unpack_from('I', self.file.read(4))[0]
        resource = []
        self.file.seek(file_list_offset)
        filenames = self.file.read(file_list_size)
        filenames = filenames.decode('cp1252')

        for i in filenames.split('\x00\x00'):
            resource.append(i.replace('\x00',''))

        if version == 23:
            self.file.seek(152)
            num_launch = struct.unpack_from('I', self.file.read(4))[0]
            print('File Run Count:'+ str(num_launch))
        elif version ==30:
            self.file.seek(208)
            num_launch = struct.unpack_from('I', self.file.read(4))[0]
            print('File Run Count:'+ str(num_launch))

        for i in resource:
            count += 1
            pf_obj = {
                "Num" : count,
                "Ref_file" : i
                "Run_count" : num_launch
            }
            print(json.dumps(pf_obj))
        return resourcce, num_launch


