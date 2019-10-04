import Evtx.Evtx as evtx
import zipfile
import os
from os import listdir
from PIL import Image
import forlib.collection.signature as sig
from Registry import Registry

def signature_db(path):
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
