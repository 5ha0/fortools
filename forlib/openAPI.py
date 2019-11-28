import magic
import pyevtx
import olefile
import zipfile
import sqlite3
import pyesedb
import pyewf, pytsk3
import PyPDF2
import codecs
import struct
import os
from PIL import Image
from Registry import Registry
from os import listdir
from forlib.processing import disk_analysis
from forlib.processing import log_analysis
from forlib.processing import jump_analysis
from forlib.processing import files_analysis
from forlib.processing import reg_analysis
from forlib.processing import thumbnail_analysis
from forlib.processing import lnk_analysis
from forlib.processing import recycle_analysis
from forlib.processing import iconcache_analysis
from forlib.processing import prefetch_analysis
from forlib.processing import mem_analysis
from forlib.processing import browser_analysis
from forlib.processing import filesystem_analysis
from forlib import decompress1
from forlib import signature as sig
from forlib import calc_hash as calc_hash


def sig_check(path):
    extension = magic.from_file(path).split(',')[0]
    if extension[:11] == 'cannot open' or extension == 'data':
        extension = sig.sig_check(path)
    return extension


def file_open(path):
    extension = sig_check(path)
    if extension == 'MS Windows Vista Event Log':
        return EventLog.file_open(path)
    elif extension == 'JPEG image data':
        return Files.JPEG.file_open(path)
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
        list_info = file.listdir(streams=True, storages=False)
        check = 0
        for i in list_info:
            if i[0] == 'DestList':
                check = 1
                break
        if check == 1:
            return JumpList.file_open(path)
        else:  # if file.listdir(streams=True, storages=False)[-1][0] == 'PowerPoint Document':
            return Files.MSOld.file_open(file)
    elif extension == 'thumb':
        return binary_open(path)
    elif extension == 'iconcache':
        return binary_open(path)
    elif extension == 'Zip archive data':
        return Files.ZIP.file_open(path)
    elif extension == 'Hangul (Korean) Word Processor File 5.x':
        return Files.HWP.file_open(path)
    elif extension == 'systemp':
        file = systemp_open(path)
        return file
    elif extension == 'PDF document':
        return Files.PDF.file_open(path)
    elif extension == 'Cache':
        return Thumbnail.file_open(path)
    elif extension == 'MS Windows shortcut':
        return Lnk.file_open(path)
    elif extension == 'recycle_i':
        return Recycle.file_open(path)
    elif extension == 'prefetch':
        return Prefetch.file_open(path)

class Disk:
    def disk_open(path):
        if pyewf.check_file_signature(path) == True:
            filename = pyewf.glob(path)
            ewf_handle = pyewf.handle()
            ewf_handle.open(filename)
            return disk_analysis.E01Analysis(ewf_handle)
        else:
            img_info = pytsk3.Img_Info(image)
            return disk_analysis.DDAnalysis(img_info)

class Mem:
    def mem_open(path):
        extension = sig_check(path)
        if extension == 'data' or extension == 'block special':
            calc_hash.get_hash(path)
            return mem_analysis.MemAnalysis(path)


class EventLog:
    def file_open(path):
        extension = sig_check(path)
        print('extension: ' + extension)
        if extension == 'MS Windows Vista Event Log':
            hash_v = calc_hash.get_hash(path)
            file = event_open(path)
            return log_analysis.EventAnalysis(file, path, hash_v)
        print("check your file format. This is not EVTX file.")
        return -1


class LinuxLog:
    class SysLog:
        def file_open(path):
            calc_hash.get_hash(path)
            file = normal_file_oepn(path)
            return log_analysis.LinuxLogAnalysis.SysLog(file)

    class AuthLog:
        def file_open(path):
            calc_hash.get_hash(path)
            file = normal_file_oepn(path)
            return log_analysis.LinuxLogAnalysis.AuthLog(file)


class Apache:
    class AccessLog:
        def file_open(path):
            calc_hash.get_hash(path)
            file = normal_file_oepn(path)
            return log_analysis.ApacheLog.Access(file)

    class ErrLog:
        def file_open(path):
            calc_hash.get_hash(path)
            file = normal_file_oepn(path)
            return log_analysis.ApacheLog.Error(file)


# class IIS:
class IIS:
    def file_open(path):
        calc_hash.get_hash(path)
        file = normal_file_oepn(path)
        return log_analysis.IIS(file)


class Files:
    class MSOld:
        def file_open(path):
            hash_v = calc_hash.get_hash(path)
            file = file_open(path)
            return files_analysis.MSOldAnalysis(file, path, hash_v)

    class HWP:
        def file_open(path):
            extension = sig_check(path)
            print('extension: ' + extension)
            if extension == 'Hangul (Korean) Word Processor File 5.x':
                hash_v = calc_hash.get_hash(path)
                file = file_open(path)
                return files_analysis.HWPAnalysis(file, path, hash_v)
            print("check your file format. This is not HWP file.")
            return -1

    class JPEG:
        def file_open(path):
            extension = sig_check(path)
            print('extension: ' + extension)
            if extension == 'JPEG image data':
                hash_v = calc_hash.get_hash(path)
                file = jpeg_open(path)
                return files_analysis.JPEGAnalysis(file, path, hash_v)
            print("check your file format. This is not JPEG file.")
            return -1

    class PDF:
        def file_open(path):
            extension = sig_check(path)
            print('extension: ' + extension)
            if extension == 'PDF document':
                hash_v = calc_hash.get_hash(path)
                file = file_open(path)
                return files_analysis.PDFAnalysis(file, path, hash_v)
            print("check your file format. This is not PDF file.")
            return -1

    class ZIP:
        def file_open(path):
            extension = sig_check(path)
            print('extension: ' + extension)
            if extension == 'Zip archive data':
                calc_hash.get_hash(path)
                file = zip_open(path)
                return files_analysis.ZIPAnalysis(file)
            print("check your file format. This is not ZIP file.")
            return -1


class Lnk:
    def file_open(path):
        extension = sig_check(path)
        print('extension: ' + extension)
        if extension == 'MS Windows shortcut':
            calc_hash.get_hash(path)
            file = lnk_open(path)
            return lnk_analysis.LnkAnalysis(file)


class Recycle:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'data':
            calc_hash.get_hash(path)
            file = recycle_open(path)
            return recycle_analysis.RecycleAnalysis(file)


class Iconcache:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'data':
            calc_hash.get_hash(path)
            file = iconcache_open(path)
            return iconcache_analysis.IconcacheAnalysis(file)


class Prefetch:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'prefetch':
            calc_hash.get_hash(path)
            dirname = os.path.dirname(path)
            basename = os.path.basename(path)
            base = os.path.splitext(basename)
            basename = base[0]
            exetension = base[-1]
            file = prefetch_open(dirname + '\\' + basename + '-1' + exetension)
            return prefetch_analysis.PrefetchAnalysis(file, path)


class RegistryHive:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'data':
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
        else:
            print("[-] This is not Registry file")


class JumpList:
    def file_open(path):
        extension = sig_check(path)
        print('extension: ' + extension)
        if extension == 'Composite Document File V2 Document':
            hash_v = calc_hash.get_hash(path)
            file = ole_open(path)
            return jump_analysis.JumplistAnalysis(file, path, hash_v)
        else:
            print("check your file format. This is not Jumplist file.")
            return -1
        


class Thumbnail_Iconcache:
    def file_open(path):
        try:
            extension = sig_check(path)
            if extension == 'Thumb_Icon':
                hash_v = calc_hash.get_hash(path)
                file = cache_open(path)
                return thumbnail_analysis.Thumbnail_analysis_windows(file, path, hash_v)
        except:
            print("File is not found")



class Browser:
    class Chrome:
        def file_open(path):
            chrome_file = browser_analysis.Chrome(path)
            return chrome_file

    class Firefox:
        def file_open(path):
            firefox_file = browser_analysis.Firefox(path)
            return firefox_file

    class Ie_Edge:
        def file_open(path):
            ie_edge_file = browser_analysis.Ie_Edge(ie_edge_open(path))
            return ie_edge_file


class FileSystemLog:
    def file_open(path):
        hash_v = calc_hash.get_hash(path)
        extension = sig_check(path)
        if extension == 'MFT':
            return filesystem_analysis.MFTAnalysis(filesystem_log_open(path), path, hash_v)
        else:
            return filesystem_analysis.UsnJrnl(filesystem_log_open(path), path, hash_v)


def event_open(path):
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
    recycle_file = open(path, 'rb')
    return recycle_file


def iconcache_open(path):
    iconcache_file = open(path, 'rb')
    return iconcache_file


def prefetch_open(path):
    prefetch_file = open(path, 'rb')
    version = struct.unpack_from('I', prefetch_file.read(4))[0]
    if version != 23 and version != 30:
        print('error: not supported version')
        print(version)
    return prefetch_file


def filesystem_log_open(path):
    return binary_open(path)
