from Registry import Registry
import json
import codecs
from datetime import datetime
import time
class NTAnalysis:
    def __init__(self, file):
        self.reg = file

    def __rec(self, key, get_path, find_val):
#        get_path(key, find_val)
        for subkey in key.subkeys():
            self.__rec(subkey, get_path, find_val)
        get_path(key,find_val)

    def __get_path(self, key, find_val):
        for value in [v.value() for v in key.values()
                        if v.value_type() == Registry.RegSZ
                        or v.value_type() == Registry.RegExpandSZ]:
                        if find_val in value:
                            reg_key_obj = {
                                "find_keyword" : find_val,
                                "key" : key.path()
                            }
                            print(json.dumps(reg_key_obj))

    def find_key(self, keyword):
        self.__rec(self.reg.root(), self.__get_path, keyword)

    def get_recent_docs(self):
        recent = self.reg.open("SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs")
        for i, v in enumerate(recent.values()):
 
            reg_obj  = {
                    "time" : str(recent.timestamp()),
                    "name" : v.name(),
                    "data" : v.value().decode('utf-16').encode('utf-8')}
            print(json.dumps(reg_obj))
    
    def get_recent_MRU(self):
        recent = self.reg.open("Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU")
        for i, v in enumerate(recent.values()):
            reg_obj  = {
                    "time" : str(recent.timestamp()),
                    "name" : v.name(),
                    "data" : v.value().decode('utf-16')}
            print(json.dumps(reg_obj))
    
    def __print_ms(self, recent):
        ret_list = list()
        for i, v in enumerate(recent.values()):
            file_name = v.value().split("*")[1]
            reg_obj = {
                    "MS time" : str(recent.timestamp()),
                    "path" : file_name
                    }
            ret_list.append(reg_obj)
        return ret_list

    def get_ms_offic(self):
        path  = "Software\\Microsoft\\Office"
        version = self.reg.open(path)
        a = list()
        for items in version.subkeys():
            a.append(items.name())
        
        if a[0] == '11.0':    
            recent1 = self.reg.open(path + "\\%s\\Excel\\Recent Files" %(a[0]))
            recent2 = self.reg.open(path + "\\%s\\PowerPoint\\Recent File List" %(a[0]))
            recent3 = self.reg.open(path + "\\%s\\Word\\Recent File List" %(a[0]))

        if a[0] == '16.0':
            path2 = path+"\\%s\\Excel\\User MRU"%(a[0])
            LiveId = self.reg.open(path2)
            b = list()
            for items in LiveId.subkeys():
                b.append(items.name())

            recent1 = self.reg.open(path + "\\%s\\Excel\\User MRU\\%s\\File MRU" %(a[0], b[0]))
            recent2 = self.reg.open(path + "\\%s\\PowerPoint\\User MRU\\%s\\File MRU" %(a[0], b[0]))
            recent3 = self.reg.open(path + "\\%s\\Word\\User MRU\\%s\\File MRU" %(a[0], b[0]))

        xls = self.__print_ms(recent1)
        ppt = self.__print_ms(recent2)
        word = self.__print_ms(recent3)
        return xls+ppt+word
        #ret_ms.append(self.print_ms(recent1))

    def get_userassist(self):
        # CE : 실행파일 목록
        # F4 : 바로가기 목록
        path = "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist"
        user = self.reg.open(path)
        ret_list = list()
        for items in user.subkeys():
            keys = self.reg.open(path+"\\%s" %(items.name()))
            for userassist_keys in keys.subkeys():
                for userassist_values in userassist_keys.values():
                    print(userassist_values.values())
                    file_name = codecs.decode(userassist_values.name(), 'rot_13')
                    reg_obj = {
                        "GUID" : str(items.name()),
                        "file" : file_name
                    }
                    ret_list.append(reg_obj)
        return ret_list
               

class SYSAnalysis:
    def __init__(self, file):
        self.reg = file

    def control_set_check(self, file):
        key = file.open("Select")
        for v in key.values():
            if v.name() == "Current":
                return v.value()

    def rec(self, key, find_path, find_val):
        self.get_path(key, find_val)
        for subkey in key.subkeys():
            self.rec(subkey, find_path, find_val)

    def get_path(self, key, find_val):
        for value in [v.value() for v in key.values()
                        if v.value_type() == Registry.RegSZ
                        or v.value_type() == Registry.RegExpandSZ]:
                        if find_val in value:
                            reg_key_obj = {
                                "find_keyword" : find_val,
                                "key" : key.path()
                            }
                            print(json.dumps(reg_key_obj))

    def find_key(self, keyword):
        self.rec(self.reg.root(), self.get_path, keyword)

    def get_USB(self):
        recent = self.reg.open("ControlSet00%s\\Enum\\USB" %self.control_set_check(self.reg))
        for i, v in enumerate(recent.values()):
            reg_obj  = {
                    "time" : str(recent.timestamp()),
                    "path" : v.value()}
            print(json.dumps(reg_obj))
