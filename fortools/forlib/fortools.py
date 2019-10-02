from forlib.collection.file_open import *
from forlib.processing.file_analysis import *

def file_open_func(path):
    file_extension = signature_db(path)
    file = log_analysis(extension_file_open(file_extension, path))
    return file

class unknown():
    def file_open(path):
        return file_open_func(path)

class log():
    def file_open(path):
        file = log_analysis(evtx_open(path))
        return file

class registry():
    def __init__(self, path):
        self.path = path

    def file_open(self):
        return file_open_func(self)

class file():
    def file_open(path):
        file = zip_open(path)
        return file
