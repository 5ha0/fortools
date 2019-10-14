import json
from Registry import Registry
import forlib.processing.log_analysis as log


class LogAnalysis:
    def EvtxAnalysis(file):
        return log.EvtxAnalysis(file)

    def WebLogAnalysis(file):
        return log.WebLogAnalysis(file)

class Files_analysis:
    def __init__(self, file):
        self.file = file

    class jpeg_analysis():
        def __init__(self, file):
            self.file = file

        
class Reg_analysis():
    def __init__(self, file):
        self.reg = file

    def rec(self, key, find_path, find_val):
        find_path(key, find_val)
        for subkey in key.subkeys():
            self.rec(subkey, find_path, find_val)

    def find_path(self, key, find_val):
        for value in [v.value() for v in key.values()
                        if v.value_type() == Registry.RegSZ
                        or v.value_type() == Registry.RegExpandSZ]:
                        if find_val in value:
                            print (key.path())

    def get_find_key(self, keyword):
        self.rec(self.reg.root(), self.find_path, keyword)

    def recent_docs(self):
        recent = self.reg.open("SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs")
        for i, v in enumerate(recent.values()):
            print ('{} > {} : {}'.format(recent.timestamp(), v.name(), v.value().decode('utf-16')))
