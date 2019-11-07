from datetime import datetime,timedelta
import os
import struct
import json


class PrefetchAnalysis:

    def __init__(self,file):
        self.file = file
 
    def file_name(self):
        self.file.seek(16)
        file_name = self.file.read(58)
        file_name = file_name.decode('utf16', 'ignore')
        file_name = file_name.replace('\x00','')
        print('Executable File Name: ' + file_name)
        return file_name
        
    def last_run_time(self):
        self.file.seek(128)
        time = struct.unpack_from("<Q", self.file.read(8))[0]
        time = '%016x' %time
        time = int(time,16)/10.
        last_run_time =  datetime(1601, 1, 1) + timedelta(microseconds=time)+timedelta(hours=9)  
        print("File Last Run Time: " + str(last_run_time) +' UTC+9:00')
        return last_run_time

    def create_time(self, path):
        time = datetime.fromtimestamp(os.path.getctime(path))
        print ('File Create Time: '+str(time) +' UTC+9:00')
        return time
    
    def write_time(self, path):
        time = datetime.fromtimestamp(os.path.getmtime(path))
        print ('File Write Time: '+ str(time) +' UTC+9:00')
        return time
    
    def num_launch(self):
        self.file.seek(0)
        version = struct.unpack_from('<I', self.file.read(4))[0]
        
        if version == 23:
            self.file.seek(152)
            num_launch = struct.unpack_from('<I', self.file.read(4))[0]
        elif version ==30:
            self.file.seek(208)
            num_launch = struct.unpack_from('<I', self.file.read(4))[0]
            
        print('File Run Count:'+ str(num_launch))
        
        return num_launch
    
    def file_list(self):
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
    
<<<<<<< HEAD
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
        print('File Create Time: '+str(c_time) +' UTC+9:00')
        print('File Write Time: '+ str(w_time) +' UTC+9:00')
        # PrefetchAnalysis.last_run_time()
        # PrefetchAnalysis.create_time()
        # PrefetchAnalysis.write_time()
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
        
