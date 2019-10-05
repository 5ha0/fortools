from forlib.collection.file_open import *
from forlib.collection.decompress import *
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


class jumplist:
    def jumplist_open(path):
	file = open(path,'rb')
	return file


class iconcache:
    def iconcache_open(path):
	file = open(path,'rb')
	return file


class lnk:
    def lnk_open(path):
	file = open(path, 'rb')
	return file


class prefetch:
    def prefetch_open(path):
	file = open(path,'rb')
	if file.read(3) == 'MAM':
	    file = decompress.decomp(path)
	return file

class superfetch:
    def superfetch_open:
        file = open(path,'rb')
        if file.read(3) == 'MAM':
            file = decompress.decomp(path)
        return file

class recycle:
    def recycle_open(path):
        file_kind = path.split('\\')[-1]
	if file_kind.find('R') != -1:
	    file_extension = path.split('.')[1]
	    file = file_open.extension_file_open(file_extension,path)
	elif file_kind.find('I') != -1:
	    file = open(path,'rb')
	return file  


class thumbnail:
    def thumbnail_open(path):
        file = open(path,'rb')
	return file


class log:
    def file_open(path):
        if signature_db(path) == 'evtx':#evtx
            file = evtx_analysis(evtx_open(path))
        else:
            file = log_analysis(normal_file_oepn(path))
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
