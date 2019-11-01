from forlib.openAPI import *
from forlib.outcome.visualize import *
from forlib.openAPI import LinuxLog
from forlib.processing import log_analysis
from forlib.processing import files_analysis
from forlib.processing import jump_analysis
from forlib.processing import thumbnail_analysis
from forlib.processing import reg_analysis


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
            #return reg_analysis.RegistryAnalysis(file)


class JumpList:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'Composite Document File V2 Document':
            file = ole_open(path)
            return jump_analysis.JumplistAnalysis(file)

class Thumbnail:
    def file_open(path):
        file = file_open(path)
        return thumbnail_analysis(file)