from Registry import Registry
import json
import codecs

class NTAnalysis:
    def __init__(self, file):
        self.reg = file

    def rec(self, key, get_path, find_val):
#        get_path(key, find_val)
        for subkey in key.subkeys():
            self.rec(subkey, get_path, find_val)
        get_path(key,find_val)

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

    def get_recent_docs(self):
        recent = self.reg.open("SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs")
        for i, v in enumerate(recent.values()):
            '''
            reg_obj  = {
                    "time" : str(recent.timestamp()),
                    "name" : v.name(),
                    "data" : v.value().decode('utf-16').encode('utf-8')}
            print(json.dumps(reg_obj))
            '''
            print ('{} > {} : {}'.format(recent.timestamp(), v.name(), v.value().decode('utf-16')))
    
    def get_recent_MRU(self):
        recent = self.reg.open("Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU")
        for i, v in enumerate(recent.values()):
            reg_obj  = {
                    "time" : str(recent.timestamp()),
                    "name" : v.name(),
                    "data" : v.value().decode('utf-16')}
            print(json.dumps(reg_obj))
    
    def print_ms(self, recent):
        ret_obj  = dict()
        ret_list = list()
        for i, v in enumerate(recent.values()):
            reg_obj = {
                    "time" : str(recent.timestamp()),
                    "path" : v.value()
                    }
            ret_obj["no."+str(i+1)] = json.dumps(reg_obj)
        ret_list.append(ret_obj)
        return ret_list

    def get_ms_offic(self):
        ret_ms = list()
        recent1 = self.reg.open("Software\\Microsoft\\Office\\11.0\\Excel\\Recent Files")
        print(self.print_ms(recent1))
        #ret_ms.append(self.print_ms(recent1))

    def get_userassist(self):
        # CE : 실행파일 목록
        # F4 : 바로가기 목록
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
                        "GUID" : str(items.name()),
                        "file" : file_name
                    }
                    # count = count+1
                    # ret_obj = dict()
                    # ret_obj["no" + str(count)] = reg_obj
                    ret_list.append(reg_obj)
        return ret_list
               
# SYSTME 임
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
