from forlib.openAPI import *
from forlib.outcome.visualize import *
from forlib.openAPI import LinuxLog
from forlib.processing import log_analysis
from forlib.processing import files_analysis
from forlib.processing import jump_analysis
from forlib.processing import thumbnail_analysis
from forlib.processing import reg_analysis
from forlib.processing import lnk_analysis
from forlib.processing import recycle_analysis
from forlib.processing import iconcache_analysis
from forlib.processing import prefetch_analysis
from forlib.processing import browser_analysis

class EvtxLog:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'MS Windows Vista Event Log':
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


class WebLog:
    class Apache:
        class AccessLog:
            def file_open(path):
                file = normal_file_oepn(path)
                return log_analysis.WebAnalysis.ApacheLog.Access(file)

        class ErrLog:
            def file_open(path):
                file = normal_file_oepn(path)
                return log_analysis.WebLog.ApacheLog.Error(file)

    # class IIS:


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


class Lnk:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'MS Windows shortcut':
            file = lnk_open(path)
            return lnk_analysis.LnkAnalysis(file)


class Recycle:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'recycle':
            file = recycle_open(path)
            return recycle_analysis.RecycleAnalysis(file)
     
    
class Iconcache:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'iconcache':
            file = iconcache_open(path)
            return iconcache_analysis.IconcacheAnalysis(file)
        

class Prefetch:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'SCCA':
            file = prefetch_open(path)
            return prefetch_analysis.PrefetchAnalysis(file)
        
        
class Registry:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'MS Windows registry file':
            file = reg_open(path)
            #return reg_analysis.RegistryAnalysis(file)


class JumpList:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'Composite Document File V2 Document':
            file = ole_open(path)
            return jump_analysis.JumplistAnalysis(file)

        
class Thumbnail:
    def file_open(path):
        # extension = sig_check(path)
        # if extension == 'Cache':
        file = cache_open(path)
        return thumbnail_analysis.Thumbnail_analysis_windows(file)

    
    


