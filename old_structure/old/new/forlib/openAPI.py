import magic
import pyevtx
import olefile
import zipfile
import sqlite3
import PyPDF2
from PIL import Image
from Registry import Registry
from os import listdir
from forlib.processing import log_analysis
from forlib.processing import jump_analysis
from forlib.processing import files_analysis
from forlib.processing import reg_analysis


def file_open(path):
    extension = magic.from_file(path).split(',')[0]
    # print(extension)
    if extension == 'MS Windows Vista Event Log':
        file = evtx_open(path)
        return log_analysis.EvtxAnalysis(file)
    elif extension == 'ASCII text':
        file = normal_file_oepn(path)
        return log_analysis.WebLogAnalysis(file)
    elif extension == 'JPEG image data':
        file = jpeg_open(path)
        return files_analysis.JPEGAnalysis(file)
    elif extension == 'MS Windows shortcut':
        return binary_open(path)
    elif extension == 'MS Windows registry file':
        file = reg_analysis(reg_open(path))
        return file
    elif extension == 'Composite Document File V2 Document':
        return jump_analysis.jumplist_analysis(ole_open(path))
    elif extension == 'thumb':
        return binary_open(path)
    elif extension == 'iconcache':
        return binary_open(path)
    elif extension == 'Zip archive data':
        return zip_open(path)
    elif extension == 'Hangul (Korean) Word Processor File 5.x':
        file = ole_open(path)
        return files_analysis.HWPAnalysis(file)
    elif extension == 'systemp':
        file = systemp_open(path)
        return file
    elif extension == 'PDF document':
        file = pdf_open(path)
        return files_analysis.PDFAnalysis(file)
    #PNG image data


def evtx_open(path):
    evtx_file = pyevtx.file()
    evtx_file.open(path)
    return evtx_file


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


def chrome_open(path):
    open_chrome_file = open(path, "rb")
    format = open_chrome_file.read(15).decode()

    if format == "SQLite format 3":
        conn = sqlite3.connect(path)
        db_cursor = conn.cursor()
        return db_cursor
    else:
        return open_chrome_file


def firefox_open(path):
    open_firefox_file = open(path, "rb")
    format = open_firefox_file.read(15).decode()

    if format == "SQLite format 3":
        conn = sqlite3.connect(path)
        db_cursor = conn.cursor()
        return db_cursor
    else:
        return open_firefox_file


def lnk_open(path):
    file = open(path, 'rb')
    return file


def recycle_open(path):
    file = open(path, 'rb')
    return file


def ole_open(path):
    file = olefile.OleFileIO(path)
    return file


def pdf_open(path):
    file = PyPDF2.PdfFileReader(open(path, 'rb'))
    return file
