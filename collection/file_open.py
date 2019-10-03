import Evtx.Evtx as evtx
import decompress


def signature_db(path):
    file_extension_recycle = path.split('\')[-1]
    if file_extionsion_recycle =='$I':
        return recycle_open(path)

    file_extension = path.split('.')[1]
    return str(file_extension)
    
    def extension_file_open(extension, path):
        if extension == 'pf'
            return pf_open(path)
        elif extension == 'lnk':
            return lnk_open(path)
        elif extension == 'automaticdestinations-ma' or 'customdestinations-ms':
            return jumplist_open(path)

def evtx_open(path):
    return evtx.Evtx(path)

def reg_open(path):
    return path

def zip_open(path):
    return path

def jpeg_open(path):
    return path

def thum_open(path):
    return path

def pf_open(path):
    file = open(path,'rb')
        if file.read(3)  == 'MAM':
            f.close()
            decompress = decompress.decomp('path')
            return decompress
    return file

def lnk_open(path):
    file = open(path,'rb')
    return file

def recycle_open(path):
    file = open(path,'rb')
    return file

def jumplist_open(path):
    file = open(path,'rb')
    return file


