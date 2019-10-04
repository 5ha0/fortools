import Evtx.Evtx as evtx
import zipfile
import os
from os import listdir
from PIL import Image
import forlib.collection.signature as sig
from Registry import Registry

def signature_db(path):
    file_extension_recycle = path.split('\')[-1]
    if file_extionsion_recycle =='$I':
        return recycle_open(path)
                                        
    return sig.sig_check(path)


def evtx_open(path):
    return evtx.Evtx(path)

                                        
def reg_open(path):
    return Registry.Registry(path)

                                        
def zip_open(path):
    file = open(path, 'rb')
    z = zipfile.ZipFile(file, 'r')
    return z


def jpeg_open(path):
    return Image.open(path)


def systemp_open(path):
    return [f for f in listdir(path)]


def binary_open(path):
    return open(path, 'rb')


def normal_file_oepn(path):
    return open(path, 'r')

                                        
def thumb_open(path):
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
