from argparse import ArgumentParser
import binascii
import ctypes
from datetime import datetime,timedelta
import ntpath
import os
import struct
import sys
import tempfile


class PrefetchAnalysis:

    def __init__(self,file):
        self.file = file
 
    def pf_file_name(self):
        self.file.seek(16)
        file_name = self.file.read(58)
        file_name = file_name.decode('utf16', 'ignore')
        file_name = file_name.replace('\x00','')
        print('Executable File Name: ' + file_name)
        return file_name
        
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
        self.file.seek(0)
        version = struct.unpack_from('<I', self.file.read(4))[0]
        
        if version == 23:
            self.file.seek(152)
            print('File Run Count:'+ str(struct.unpack_from('<I', self.file.read(4))[0]))
        elif version ==30:
            self.file.seek(208)
            print('File Run Count:'+ str(struct.unpack_from('<I', self.file.read(4))[0]))
        return num_launch
    
    def pf_file_list():
        self.file.seek(100)
        file_list_offset=struct.unpack_from('<I', self.file.read(4))[0]
        file_list_size=struct.unpack_from('<I', self.file.read(4))[0]
        resource = []
        self.file.seek(file_list_offset)
        filenames = self.file.read(file_list_size)
        filenames = filenames.decode('cp1252')
        for i in filenames.split('\x00\x00'):
            resource.append(i.replace('\x00',''))
        
        count = 0
        for i in resource:
            count += 1
            pf_obj = {
                "Num" : count,
                "Ref_file" : i
            }
            print(json.dumps(pf_obj))
        return resource
    
##class favorite:
##    def time_stamp:
