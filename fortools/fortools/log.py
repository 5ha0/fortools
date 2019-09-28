from fortools.collection.file_open import *

def file_open(path):
    file_extension = signature_db(path)
    return extension_file_open(file_extension, path)

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