import json
from Registry import Registry
import forlib.processing.log_analysis as log
import forlib.processing.jump_analysis as jump
import forlib.processing.files_analysis as files
import codecs


class LogAnalysis:
    def evtx_analysis(file):
        return log.EvtxAnalysis(file)

    def weblog_analysis(file):
        return log.WebLogAnalysis(file)


class FilesAnalysis:
    def jpeg_analysis(file):
        return files.JPEGLogAnalysis(file)
            
        
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

    def get_userassist(self):
        path = "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist"
        user = self.reg.open(path)
        count = 0
        ret_list = list()
        for items in user.subkeys():
            keys = self.reg.open(path+"\\%s" %(items.name()))
            for userassist_keys in keys.subkeys():
                for userassist_values in userassist_keys.values():
                    file_name = codecs.decode(userassist_values.name(), 'rot_13')
                    reg_obj = {
                        "user_key" : str(items.name()),
                        "time" : str(userassist_keys.timestamp()),
                        "file" : file_name
                    }
                    count = count+1
                    ret_obj = dict()
                    ret_obj["no" + str(count)] = reg_obj
                    ret_list.append(ret_obj)
        for i in range(2, len(ret_list)):
            print(ret_list[i])


class JumplistAnalysis:
    def jumplist_analysis(file):
        return jump.JumplistAnalysis(file)


