import Evtx.Evtx as evtx
import zipfile

def signature_db(path):
    file_extension = path.split('.')[1]
    return str(file_extension)

def extension_file_open(extension, path):
    if extension == 'evtx':
        return evtx_open(path)
    elif extension == 'regf':
        return reg_open(path)
    elif extension == 'zip':
        return zip_open(path)
    elif extension == 'jpeg':
        return jpeg_open(path)
    elif extension == 'thum':
        return thum_open(path)

def evtx_open(path):
    return evtx.Evtx(path)

def reg_open(path):
    return path

def zip_open(path):
    file = open(path, 'rb')
    z = zipfile.ZipFile(file, 'r')
    return z

def jpeg_open(path):
    return path

def thum_open(path):
    return path