import magic
import pyevtx
import olefile
import zipfile
import sqlite3
import PyPDF2
import codecs
import pyesedb
from PIL import Image
from Registry import Registry
from os import listdir
from forlib.processing import log_analysis
from forlib.processing import jump_analysis
from forlib.processing import files_analysis
from forlib.processing import reg_analysis
from forlib.processing import thumbnail_analysis
from forlib.processing import lnk_analysis
from forlib.processing import recycle_analysis
from forlib.processing import iconcache_analysis
from forlib.processing import prefetch_analysis
from forlib import decompress1
from forlib import signature as sig
from forlib import calc_hash as calc_hash

def sig_check(path):
    extension = magic.from_file(path).split(',')[0]
    return extension


def file_open(path):
    calc_hash.get_md5_hash(path)
    calc_hash.get_sha1_hash(path)
    extension = sig_check(path)
    if extension[:11] == 'cannot open':
        extension = sig.sig_check(path)
        print('extension: ' + extension)
    else:
        print('extension: ' + extension)
    if extension == 'MS Windows Vista Event Log':
        return EvtxLog.file_open(path)
    elif extension == 'ASCII text':
        file = normal_file_oepn(path)
        return log_analysis.TextLogAnalysis(file)
    elif extension == 'JPEG image data':
        file = jpeg_open(path)
        return files_analysis.JPEGAnalysis(file)
    elif extension == 'MS Windows registry file':
        file = reg_open(path)
        if Registry.HiveType.NTUSER == file.hive_type():
            return reg_analysis.NTAnalysis(file)
        elif Registry.HiveType.SAM == file.hive_type():
            return reg_analysis.SAMAnalysis(file)
        elif Registry.HiveType.SOFTWARE == file.hive_type():
            return reg_analysis.SWAnalysis(file)
        elif Registry.HiveType.SYSTEM == file.hive_type():
            return reg_analysis.SYSAnalysis(file)
        elif Registry.HiveType.SYSTEM == file.hive_type():
            print("[-] To be continue")
        else:
            print("[-] This is not HiveFile")
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
    elif extension == 'MS Windows shortcut':
        file = lnk_open(path)
        return lnk_analysis.LnkAnalysis(file)
    elif extension == 'data':
        if '$I' in path:
            file = recycle_open(path)
            return recycle_analysis.RecycleAnalysis(file)
        if 'iconcache.db' in path:
            file = iconcache_open(path)
            return iconcache_analysis.IconcacheAnalysis(file)
        if '.pf' in path:
            file = prefetch_open(path)
            return prefetch_analysis.PrefetchAnalysis(file)
    
    # elif extension == 'Extensible storage engine DataBase':
    # elif extension == 'SQLite 3.x database' :    
    
    # elif extension == 'PE32+ executable (console) x86-64':
    #     file =
    # PNG image data


class EvtxLog:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'MS Windows Vista Event Log':
            calc_hash.get_hash(path)
            file = evtx_open(path)
            return log_analysis.EvtxAnalysis(file)
        print("check your file format. This is not EVTX file.")
        return -1


class LinuxLog:
    class SysLog:
        def file_open(path):
            file = normal_file_oepn(path)
            return log_analysis.LinuxLogAnalysis.SysLog(file)

    class AuthLog:
        def file_open(path):
            file = normal_file_oepn(path)
            return log_analysis.LinuxLogAnalysis.AuthLog(file)

    # class History


class Apache:
    class AccessLog:
        def file_open(path):
            file = normal_file_oepn(path)
            return log_analysis.ApacheLog.Access(file)

    class ErrLog:
        def file_open(path):
            file = normal_file_oepn(path)
            return log_analysis.ApacheLog.Error(file)


# class IIS:
class IIS:
    def file_open(path):
        file = normal_file_oepn(path)
        return log_analysis.IIS(file)


class Files:
    class MSOld:
        class PPT:
            def file_open(path):
                file = file_open(path)
                return files_analysis.MSOldAnalysis(file)

    class HWP:
        def file_open(path):
            file = file_open(path)
            return files_analysis.HWPAnalysis(file)

    class JPEG:
        def file_open(path):
            file = file_open(path)
            return files_analysis.JPEGAnalysis(file)

    class PDF:
        def file_open(path):
            file = file_open(path)
            return files_analysis.PDFAnalysis(file)


class LNK:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'MS Windows shortcut':
            file = binary_open(path)
            #return lnk_analysis.LNKAnalysis(file)


class Registry:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'MS Windows registry file':
            file = reg_open(path)
            return reg_analysis.RegistryAnalysis(file)


class JumpList:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'Composite Document File V2 Document':
            file = ole_open(path)
            return jump_analysis.JumplistAnalysis(file)


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
    
    
def ie_edge_open(path):
    return pyesedb.open(path, 'rb')


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


def recycle_open(path):
    recycle_file_extension = path.split('\\')[-1]
    if '$R' in recycle_file_extension:
        recycle_file = file_open(path)
        return recycle_file
    elif '$I' in file_extension_recycle:
        recycle_file = open(path, 'rb')
        return recycle_file

    
def iconcache_open(path):
    iconcache_file = open(path, 'rb')
    return iconcache_file


def prefetch_open(path):
    prefetch_file = open(path, 'rb')
    if prefetch_file.read(3) == b'MAM':
        prefetch_file.close()
        decompressed = decompress1.decompress(path)

        dirname = os.path.dirname(path)
        basename = os.path.basename(path)
        base = os.path.splitext(basename)
        basename = base[0]
        exetension = base[-1]
            
        prefetch_file = open(dirname+'\\'+basename+'-1'+exetension,'wb')
        prefetch_file.write(decompressed)
        prefetch_file.close()
            
    prefetch_file = open(dirname+'\\'+basename+'-1'+exetension,'rb')
    version = struct.unpack_from('I', prefetch_file.read(4))[0]
            
    if version != 23 and version != 30:
        print ('error: not supported version')

    return prefetch_file
