from forlib.collection.decompress import *
import forlib.processing.file_analysis as file_analysis
import forlib.collection.file_open as file_open


class Unknown:
    def file_open(path):
        extension = file_open.signature_db(path)
        if extension == 'evtx':
            return file_open.evtx_open(path)
        elif extension == 'jpeg':
            return file_open.jpeg_open(path)
        elif file_open.extension == 'lnk':
            return 0


class Log:
    def file_open(path):
        if file_open.signature_db(path) == 'evtx':#evtx
            file = file_analysis.Evtx_analysis(file_open.evtx_open(path))
        return file


class Registry:
    def file_open(path):
        file = file_analysis.Reg_analysis(file_open.reg_open(path))
        return file

'''
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
'''

class Lnk:
    def file_open(path):
        return file_open.binary_open(path)


class Jumplist:
    def file_open(path):
        return file_open.binary_open(path)

'''
class Recycle:
    def file_open(path):
        file_kind = path.split('\\')[-1]
        if file_kind.find('R') != -1:
            file_extension = path.split('.')[1]
            file = file_open.extension_file_open(file_extension,path)
        elif file_kind.find('I') != -1:
            file = binary_open(path)
        return file
'''

class Thumbnail:
    def file_open(path):
        return file_open.binary_open(path)


class Iconcache:
    def file_open(path):
        return file_open.binary_open(path)


class Files:
    def file_open(path):
        extension = file_open.signature_db(path)
        if extension == 'zip':
            return file_open.zip_open(path)
        elif extension == 'jpg' or extension == 'jpeg':
            return file_open.jpeg_open(path)


class System_temp:
    def file_open(path):
        file = file_open.systemp_open(path)
        return file


class Ie:
    def file_open(path):
        return file_open.binary_open(path)


class Edge:
    def file_open(path):
        return file_open.binary_open(path)
