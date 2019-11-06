from argparse import ArgumentParser
import binascii
import ctypes
from datetime import datetime,timedelta
import ntpath
import os
import struct
import sys
import tempfile
import decompress1



class Prefetch:
    def __init__(self,file):
        self.file = file
    
    def pf_open(self, path):    
        self.file = open(path, 'rb')
        if self.file.read(3) == b'MAM':
            self.file.close()
            decompressed = decompress1.decompress(path)

            dirname = os.path.dirname(path)
            basename = os.path.basename(path)
            base = os.path.splitext(basename)
            basename = base[0]
            exetension = base[-1]
            
            self.file = open(dirname+'\\'+basename+'-1'+exetension,'wb')
            self.file.write(decompressed)
            self.file.close()
            
        self.file = open(dirname+'\\'+basename+'-1'+exetension,'rb')
        version = struct.unpack_from('I', self.file.read(4))[0]
            
        if version != 23 and version != 30:
            print ('error: not supported version')

        signature = self.file.read(4)
        print(signature)
        if signature != b'SCCA':
            print('not prefetch file')
        
        print('Success file open')
        return self.file


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
            print('File Run Count:'+ str(struct.unpack_from('I', self.file.read(4))[0]))
        elif version ==30:
            self.file.seek(208)
            print('File Run Count:'+ str(struct.unpack_from('I', self.file.read(4))[0]))
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
    
##class favorite:
##    def time_stamp:
class Favorite:
    
    def __init__(self, file):
        self.file = file
        
    def time_stamp(self):
        l_time = struct.unpack_from("<Q", self.file.read(8))[0]
        l_time = '%016x' %l_time
        l_time = int(l_time,16)/10.
        l_time =  datetime(1601, 1, 1) + timedelta(microseconds=l_time)+timedelta(hours=9)  
        
        c_time = datetime.fromtimestamp(os.path.getctime(path))
        
        w_time = datetime.fromtimestamp(os.path.getmtime(path))
        
        print("File Last Run Time: " + str(last_run_time) +' UTC+9:00')
        print ('File Create Time: '+str(c_time) +' UTC+9:00')
        print ('File Write Time: '+ str(w_time) +' UTC+9:00')
        
        return l_time, c_time, w_time
    
    def file_list_whit_num_launch(self):
        self.file.seek(0)
        version = struct.unpack_from('<I', self.file.read(4))[0]
        
        if version == 23:
            self.file.seek(152)
            num_launch = struct.unpack_from('<I', self.file.read(4))[0]
        elif version ==30:
            self.file.seek(208)
            num_launch = struct.unpack_from('<I', self.file.read(4))[0]
            
        self.file.seek(100)
        file_list_offset=struct.unpack_from('<I', self.file.read(4))[0]
        file_list_size=struct.unpack_from('<I', self.file.read(4))[0]
        resource = []
        self.file.seek(file_list_offset)
        filenames = self.file.read(file_list_size)
        filenames = filenames.decode('cp1252')
        for i in filenames.split('\x00\x00'):
            resource.append(i.replace('\x00',''))
        
        print('File Run Count:'+ str(num_launch))
        
        count = 0
        for i in resource:
            count += 1
            pf_obj = {
                "Num" : count,
                "Ref_file" : i
            }
            print(json.dumps(pf_obj))
        return num_launch, resource
        



