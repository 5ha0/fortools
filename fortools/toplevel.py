from forlib.openAPI import *
from forlib.openAPI import LinuxLog
from forlib.processing import log_analysis
from forlib.processing import files_analysis
from forlib.processing import jump_analysis
from forlib.processing import reg_analysis


class EvtxLog:
    def file_open(path):
        extension = sig_check(path)
        if extension == 'MS Windows Vista Event Log':
            file = evtx_open(path)
        return log_analysis.EvtxAnalysis(file)


class Files:
    def file_open(path):
        file = file_open(path)
        return files_analysis.EvtxAnalysis(file)
