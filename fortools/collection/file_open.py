import Evtx.Evtx as evtx

def signature_db(path):
    file_extension = path.split('.')[1]
    return str(file_extension)

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