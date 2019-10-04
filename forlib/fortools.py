from forlib.collection.file_open import *
from forlib.processing.file_analysis import *


class unknown:
    def file_open(path):
        extension = signature_db(path)
        if extension == 'evtx':
            return evtx_open(path)
        elif extension == 'jpeg':
            return jpeg_open(path)
        elif extension == 'lnk':
            return 0


class log:
    def file_open(path):
        if signature_db(path) == 'evtx':#evtx
            file = evtx_analysis(evtx_open(path))
        else:
            file = log_nalysis(normal_file_oepn(path))
        return file

class registry():
    def __init__(self, path):
        self.path = path
        
    def file_open(path):
        file = reg_analysis(reg_open(path))
        return file
    
class file:
    def file_open(path):
        extension = signature_db(path)
        if extension == 'zip':
            return zip_open(path)
        elif extension == 'jpeg':
            return jpeg_open(path)
        elif extension == 'jpg':
            print('jpg')


class system_temp:
    def file_open(path):
        file = systemp_open(path)
        return file


class lnk:
    def file_open(path):
        return binary_open(path)


class recycle:
    def file_open(path):
        return binary_open(path)


class jumplist:
    def file_open(path):
        return binary_open(path)

class ie:
    def file_open(path):
        return binary_open(path)


