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
    global file
    global version
    
    def pf_open(path):
        global file
        global version
        
        file = open(path, 'rb')
        if file.read(3) == b'MAM':
            file.close()
            decompressed = decompress1.decompress(path)
            file = open('', 'wb')
            file.write(decompressed)
            print(decompressed)

        file.seek(0)
        version = struct.unpack_from('I', file.read(4))[0]
            
        if version != 23 and version != 30:
            print ('error: not supported version')

        signature = file.read(4)
        if signature != 'SCCA':
            print('not prefetch file')
        
        print('Success file open')
        return file


    def dt_from_win32_ts(timestamp):
        WIN32_EPOCH = datetime(1601, 1, 1)
        return WIN32_EPOCH + timedelta(microseconds=timestamp // 10, hours=9)  

    def pf_size():
        global file
        global version
        file.seek(12)
        size = struct.unpack_from('I', file.read(4))[0]
        print(size)
        
    def pf_last_run_time():
        file.seek(128)
        time = struct.unpack_from("<Q", file.read(8))[0]
        time = '%016x' %time
        time = int(time,16)/10.
        last_run_time =  datetime(1601, 1, 1) + timedelta(microseconds=time)+timedelta(hours=9)  
        print("File Last Run Time: " + str(last_run_time) +' UTC+9:00')

    def pf_create_time(path):
        time = datetime.fromtimestamp(os.path.getctime(path))
        print ('file create time: '+str(time) +' UTC+9:00')

    def pf_write_time(path):
        time = datetime.fromtimestamp(os.path.getmtime(path))
        print ('file create time: '+ str(time) +' UTC+9:00')

    def pf_num_launch():
        global file
        global version
        if version == 23:
            file.seek(152)
            print('File Run Count:'+ str(struct.unpack_from('I', file.read(4))[0]))
        elif version ==30:
            file.seek(208)
            print('File Run Count:'+ str(struct.unpack_from('I', file.read(4))[0]))
            
    def pf_file_list():
        global file
        global version
        file.seek(100)
        file_list_offset=struct.unpack_from('I', file.read(4))[0]
        file_list_size=struct.unpack_from('I', file.read(4))[0]
        resource = []
        file.seek(file_list_offset)
        filenames = file.read(file_list_size)
        filenames = filenames.decode('cp1252')
        for i in filenames.split('\x00\x00'):
            resource.append(i.replace('\x00',''))
        count = 1
        for i in resource:
            print('NO{}: {}'.format(count,i))
            count += 1

##class favorite:
##    def time_stamp: