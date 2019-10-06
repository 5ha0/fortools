from forlib.collection.file_open import *
<<<<<<< HEAD
from forlib.processing.file_analysis import *


class unknown:
=======
from forlib.collection.decompress import *
from forlib.processing.file_analysis import *


class Unknown:
>>>>>>> master
    def file_open(path):
        extension = signature_db(path)
        if extension == 'evtx':
            return evtx_open(path)
<<<<<<< HEAD
        elif extension == 'jpeg':
            return jpeg_open(path)
        elif extension == 'lnk':
            return 0


class log:
=======
        elif extension == 'jpg':
            return jpeg_open(path)
        elif extension == 'lnk':
            return lnk_open(path)
        elif extension == 'zip':
            return lnk_open(path)


class Jumplist:
    def jumplist_open(path):
	file = open(path,'rb')
	return file


class Iconcache:
    def iconcache_open(path):
	file = open(path,'rb')
	return file


class Lnk:
    def lnk_open(path):
	file = open(path, 'rb')
	return file


class Prefetch:
    def prefetch_open(path):
	file = open(path,'rb')
	if file.read(3) == 'MAM':
	    file = decompress.decomp(path)
	return file

class Superfetch:
    def superfetch_open(path):
        file = open(path,'rb')
        if file.read(3) == 'MAM':
            file = decompress.decomp(path)
        return file

class Recycle:
    def recycle_open(path):
        file_kind = path.split('\\')[-1]
	if file_kind.find('R') != -1:
	    file_extension = path.split('.')[1]
	    file = file_open.extension_file_open(file_extension,path)
	elif file_kind.find('I') != -1:
	    file = open(path,'rb')
	return file  


class Thumbnail:
    def thumbnail_open(path):
        file = open(path,'rb')
	return file


class Log:
>>>>>>> master
    def file_open(path):
        if signature_db(path) == 'evtx':#evtx
            file = evtx_analysis(evtx_open(path))
        else:
<<<<<<< HEAD
            file = log_nalysis(normal_file_oepn(path))
        return file


class file:
=======
            file = log_analysis(normal_file_oepn(path))
        return file


class Registry:
    def file_open(path):
        file = reg_analysis(reg_open(path))
        return file


class Files:
>>>>>>> master
    def file_open(path):
        extension = signature_db(path)
        if extension == 'zip':
            return zip_open(path)
<<<<<<< HEAD
        elif extension == 'jpeg':
            return jpeg_open(path)
        elif extension == 'jpg':
            print('jpg')


class system_temp:
=======
        elif extension == 'jpg':
            return jpeg_open(path)


class System_temp:
>>>>>>> master
    def file_open(path):
        file = systemp_open(path)
        return file


<<<<<<< HEAD
class lnk:
    def file_open(path):
        return binary_open(path)


class recycle:
    def file_open(path):
        return binary_open(path)


class jumplist:
=======
class Ie:
>>>>>>> master
    def file_open(path):
        return binary_open(path)
