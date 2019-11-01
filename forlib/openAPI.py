import magic
import pyevtx
import olefile
import zipfile
import sqlite3
import PyPDF2
import codecs
from PIL import Image
from Registry import Registry
from os import listdir
from forlib.processing import log_analysis
from forlib.processing import jump_analysis
from forlib.processing import files_analysis
from forlib.processing import reg_analysis
from forlib.processing import thumbnail_analysis


def sig_check(path):
    extension = magic.from_file(path).split(',')[0]
    return extension


def file_open(path):
    extension = sig_check(path)
    print('extension: ' + extension)
    if extension == 'MS Windows Vista Event Log':
        file = evtx_open(path)
        return log_analysis.EvtxAnalysis(file)
    elif extension == 'ASCII text':
        file = normal_file_oepn(path)
        return log_analysis.TextLogAnalysis(file)
    elif extension == 'JPEG image data':
        file = jpeg_open(path)
        return files_analysis.JPEGAnalysis(file)
    elif extension == 'MS Windows shortcut':
        return binary_open(path)
    elif extension == 'MS Windows registry file':
        file = reg_analysis(reg_open(path))
        return file
    elif extension == 'Composite Document File V2 Document':
        file = ole_open(path)
        if file.listdir(streams=True, storages=False)[-1][0] == 'DestList':
            return jump_analysis.JumplistAnalysis(file)
        else: # if file.listdir(streams=True, storages=False)[-1][0] == 'PowerPoint Document':
            return files_analysis.MSOldAnalysis(file)
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
    elif extension == 'UTF-8 Unicode text':
        file = codecs.open(path, 'r', encoding='utf8')
        return log_analysis.TextLogAnalysis(file)
    elif extension == 'Cache':
        file = cache_open(path)
        return thumbnail_analysis.Thumbnail_analysis_windows(file)
    elif extension == 'lnk':
        file = lnk_open(path)
        #return lnk_analysis.(file)
    # elif extension == 'PE32+ executable (console) x86-64':
    #     file =
    # PNG image data


class LinuxLog:
    # auth.log, syslog
    def normal_log(path):
        file = normal_file_oepn(path)
        log_analysis.LinuxLogAnalysis.AuthLog(file)

    class Apache:
        # err log
        def apache_err(path):
            file = normal_file_oepn(path)
            log_analysis.LinuxLogAnalysis.ApacheLog.Error(file)

        # access log
        def apache_access(path):
            file = normal_file_oepn(path)
            log_analysis.LinuxLogAnalysis.ApacheLog.Access(file)


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


def chrome_open(path):
    open_chrome_file = open(path, "rb")
    file_format = open_chrome_file.read(15).decode()
    if file_format == "SQLite format 3":
        return path
    else:
        return open_chrome_file


def firefox_open(path):
    open_firefox_file = open(path, "rb")
    file_format = open_firefox_file.read(15).decode()
    if file_format == "SQLite format 3":
        return path
    else:
        return open_firefox_file


def ole_open(path):
    file = olefile.OleFileIO(path)
    return file


def pdf_open(path):
    file = PyPDF2.PdfFileReader(open(path, 'rb'))
    return file

def cache_open(path):
    cache_file = open(path, "rb")
    return cache_file

def lnk_open(path):
    lnk_file = open(path, 'rb')
    return lnk_file
