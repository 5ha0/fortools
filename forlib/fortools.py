from forlib.collection.file_open import *
from forlib.processing.file_analysis import *
from forlib.collection.decompress import *
from forlib.processing.file_analysis import *


class Unknown:
    def file_open(path):
        extension = signature_db(path)
        if extension == 'evtx':
            return evtx_open(path)
        elif extension == 'jpeg':
            return jpeg_open(path)
        elif extension == 'lnk':
            return 0

class Log:
    def file_open(path):
        if signature_db(path) == 'evtx':#evtx
            file = Evtx_analysis(evtx_open(path))
        return file


class Registry:
    def file_open(path):
        file = Reg_analysis(reg_open(path))
        return file


class Prefetch:
    def file_open(path):
        file = binary_open(path)
        if file.read(3) == 'MAM':
            file = decompress.decomp(path)
        return file


class Superfetch:
    def file_open(path):
        file = binary_open()
        if file.read(3) == 'MAM':
            file = decompress.decomp(path)
        return file


class Lnk:
    def file_open(path):
        return binary_open(path)


class Jumplist:
    def file_open(path):
        return binary_open(path)


class Recycle:
    def file_open(path):
        file_kind = path.split('\\')[-1]
        if file_kind.find('R') != -1:
            file_extension = path.split('.')[1]
            file = file_open.extension_file_open(file_extension,path)
        elif file_kind.find('I') != -1:
            file = binary_open(path)
        return file


class Thumbnail:
    def file_open(path):
        return binary_open(path)


class Iconcache:
    def file_open(path):
        return binary_open(path)


class Files:
    def file_open(path):
        extension = signature_db(path)
        if extension == 'zip':
            return zip_open(path)
        elif extension == 'jpg' or extension == 'jpeg':
            return jpeg_open(path)


class System_temp:
    def file_open(path):
        file = systemp_open(path)
        return file


class Ie:
    def file_open(path):
        return binary_open(path)


class Edge:
    def file_open(path):
        return binary_open(path)
