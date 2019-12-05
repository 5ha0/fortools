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
from forlib import decompress
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
    elif extension == 'Icon':
        return Iconcache.file_open(path)
    elif extension == 'Zip archive data':
        return Files.ZIP.file_open(path)
    elif extension == 'Hangul (Korean) Word Processor File 5.x':
        return Files.HWP.file_open(path)
    elif extension == 'PDF document':
        return Files.PDF.file_open(path)
    elif extension == 'Thumb_Icon':
        return Thumbnail_Iconcache.file_open(path)
    elif extension == 'MS Windows shortcut':
        return Lnk.file_open(path)
    elif extension == 'recycle_i':
        return Recycle.file_open(path)
    elif extension == 'prefetch':
        return Prefetch.file_open(path)
    elif extension == 'MFT':
        return FileSystemLog.file_open(path)
    else:
        print('Non sig. Plz check file extension.')

class Disk:
    def disk_open(path):
        hash_val = calc_hash.get_hash(path)
        if pyewf.check_file_signature(path) == True:
            filename = pyewf.glob(path)
            ewf_handle = pyewf.handle()
            ewf_handle.open(filename)
            return disk_analysis.E01Analysis(ewf_handle, path, hash_val)
        else:
            return disk_analysis.DDAnalysis(path, hash_val)

class Mem:
    def mem_open(path):
        extension = sig_check(path)
        if extension == 'data' or extension == 'block special':    
            hash_val = calc_hash.get_hash(path)
            return mem_analysis.MemAnalysis(path, hash_val)


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
            file = ole_open(path)
            return files_analysis.MSOldAnalysis(file, path, hash_v)

    class HWP:
        def file_open(path):
            extension = sig_check(path)
            print('extension: ' + str(extension))
            if extension == 'Hangul (Korean) Word Processor File 5.x' or extension == 'Data':
                hash_v = calc_hash.get_hash(path)
                file = ole_open(path)
                return files_analysis.HWPAnalysis(file, path, hash_v)
            print("check your file format. This is not HWP file.")
            return -1

    class JPEG:
        def file_open(path):
            extension = sig_check(path)
            print('extension: ' + str(extension))
            if extension == 'JPEG image data':
                hash_v = calc_hash.get_hash(path)
                file = jpeg_open(path)
                return files_analysis.JPEGAnalysis(file, path, hash_v)
            print("check your file format. This is not JPEG file.")
            return -1

    class PDF:
        def file_open(path):
            extension = sig_check(path)
            print('extension: ' + str(extension))
            if extension == 'PDF document':
                hash_v = calc_hash.get_hash(path)
                file = pdf_open(path)
                return files_analysis.PDFAnalysis(file, path, hash_v)
            print("check your file format. This is not PDF file.")
            return -1

    class ZIP:
        def file_open(path):
            extension = sig_check(path)
            print('extension: ' + str(extension))
            if extension == 'Zip archive data':
                hash_v = calc_hash.get_hash(path)
                file = zip_open(path)
                return files_analysis.ZIPAnalysis(file, path, hash_v)
            print("check your file format. This is not ZIP file.")
            return -1


class Lnk:
    def file_open(path):
        extension = sig_check(path)
        print('extension: ' + extension)
        if extension == 'MS Windows shortcut':
            hash_v = calc_hash.get_hash(path)
            file = lnk_open(path)
            return lnk_analysis.LnkAnalysis(file, path, hash_v)
        print("check your file format. This is not Lnk file")
        return -1


class Recycle:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'recycle_i':
            hash_v = calc_hash.get_hash(path)
            file = recycle_open(path)
            return recycle_analysis.RecycleAnalysis(file, path, hash_v)
        print("check your file format. This is not Recycle $I file")
        return -1


class Iconcache:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'Icon':
            hash_v = calc_hash.get_hash(path)
            file = iconcache_open(path)
            return iconcache_analysis.IconcacheAnalysis(file, path, hash_v)
        print("check your file format. This is not IconCache.db file")
        return -1


class Prefetch:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'prefetch':
            hash_v = calc_hash.get_hash(path)
            file = prefetch_open(path)
            file.seek(0)
            version = struct.unpack_from('I', file.read(4))[0]
            if version == 23:
                file = prefetch_open(path)
            else:
                dirname = os.path.dirname(path)
                basename = os.path.basename(path)
                base = os.path.splitext(basename)
                basename = base[0]
                exetension = base[-1]
                file = prefetch_open(dirname + '\\' + basename + '-1' + exetension)
                file.seek(0)
                version = struct.unpack_from('I', file.read(4))[0]
                if version != 23 and version != 30:
                    print('error: not supported version')
                    return -1
            return prefetch_analysis.PrefetchAnalysis(file, path, hash_v)
        print("check your file format. This is not Prefetch file")
        return -1


class RegistryHive:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'MS Windows registry file':
            file = reg_open(path)
            hash_val = calc_hash.get_hash(path)
            if Registry.HiveType.NTUSER == file.hive_type():
                return reg_analysis.NTAnalysis(file, path, hash_val)
            elif Registry.HiveType.SAM == file.hive_type():
                return reg_analysis.SAMAnalysis(file, path, hash_val)
            elif Registry.HiveType.SOFTWARE == file.hive_type():
                return reg_analysis.SWAnalysis(file, path, hash_val)
            elif Registry.HiveType.SYSTEM == file.hive_type():
                return reg_analysis.SYSAnalysis(file, path, hash_val)
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
        extension = sig_check(path)
        print('extension: ' + extension)
        if extension == 'Thumb_Icon':
            hash_v = calc_hash.get_hash(path)
            file = cache_open(path)
            return thumbnail_analysis.Thumbnail_analysis_windows(file, path, hash_v)
        else:
            print("File is not found")
            return -1


class Browser:
    class Chrome:
        class History:
            def file_open(path):
                hash_v=calc_hash.get_hash(path)
                chrome_file = browser_analysis.Chrome.History(path, hash_v)
                return chrome_file

        class Download:
            def file_open(path):
                hash_v = calc_hash.get_hash(path)
                chrome_file = browser_analysis.Chrome.Download(path, hash_v)
                return chrome_file

        class Cookie:
            def file_open(path):
                hash_v = calc_hash.get_hash(path)
                chrome_file = browser_analysis.Chrome.Cookie(path, hash_v)
                return chrome_file
            
        class Cache:
            def file_open(path):
                chrome_file = browser_analysis.Chrome.Cache(path)
                return chrome_file

    class Firefox:
        class History:
            def file_open(path):
                hash_v = calc_hash.get_hash(path)
                firefox_file = browser_analysis.Firefox.History(path, hash_v)
                return firefox_file

        class Download:
            def file_open(path):
                hash_v = calc_hash.get_hash(path)
                firefox_file = browser_analysis.Firefox.Download(path, hash_v)
                return firefox_file

        class Cookie:
            def file_open(path):
                hash_v = calc_hash.get_hash(path)
                firefox_file = browser_analysis.Firefox.Cookie(path, hash_v)
                return firefox_file

    class Ie_Edge:
        class Cache:
            def file_open(path):
                hash_v = calc_hash.get_hash(path)
                ie_edge_file = browser_analysis.Ie_Edge.Cache(ie_edge_open(path), path, hash_v)
                return ie_edge_file

        class Cookie:
            def file_open(path):
                hash_v = calc_hash.get_hash(path)
                ie_edge_file = browser_analysis.Ie_Edge.Cookie(ie_edge_open(path), path, hash_v)
                return ie_edge_file

        class History:
            def file_open(path):
                hash_v = calc_hash.get_hash(path)
                ie_edge_file = browser_analysis.Ie_Edge.History(ie_edge_open(path), path, hash_v)
                return ie_edge_file

        class Download:
            def file_open(path):
                hash_v = calc_hash.get_hash(path)
                ie_edge_file = browser_analysis.Ie_Edge.Download(ie_edge_open(path), path, hash_v)
                return ie_edge_file


class FileSystemLog:
    def file_open(path):
        hash_v = calc_hash.get_hash(path)
        extension = sig_check(path)
        if extension == 'MFT':
            print('extension: MFT')
            return filesystem_analysis.MFTAnalysis(filesystem_log_open(path), path, hash_v)
        elif extension == -1 or extension == 'data':
            return filesystem_analysis.UsnJrnl(filesystem_log_open(path), path, hash_v)
        else:
            print('extension: '+str(extension))
            print("check your file format. This is not File System Log file.")
            return -1


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
        return path


def firefox_open(path):
    open_firefox_file = open(path, "rb")
    file_format = open_firefox_file.read(15).decode()
    if file_format == "SQLite format 3":
        return path
    else:
        return path


def ie_edge_open(path):
    if pyesedb.check_file_signature(path):
        return pyesedb.open(path, 'rb')
    else:
        print("please check your file")
        return -1


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
    return prefetch_file


def filesystem_log_open(path):
    return binary_open(path)
