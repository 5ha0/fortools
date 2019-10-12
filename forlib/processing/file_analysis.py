import json
from os import listdir
from lxml import etree
import datetime
from Registry import Registry
import os.path, time


class LogAnalysis:
    class EvtxAnalysis:
        evtx_json = []


        def __init__(self, file):
            self.evtx_file = file
            self.evtx_json = self.make_JSON()

        def show_all_record(self):
            for i in self.evtx_json:
                print(i)

        def make_XML(self):
            if self.evtx_file.number_of_records > 0:
                for i in range(0, len(self.evtx_file.records)):
                    self.evtx_file.records[i].get_xml_string()

        def make_JSON(self):
            json_list = []
            for i in range(0, len(self.evtx_file.records)):
                log_obj = dict()
                log_obj["eventID"] = self.evtx_file.records[i].get_event_identifier()
                log_obj["create Time"] = str(self.evtx_file.records[i].get_creation_time())
                log_obj["level"] = self.evtx_file.records[i].get_event_level()
                log_obj["source"] = self.evtx_file.records[i].get_source_name()
                log_obj["computer Info"] = self.evtx_file.records[i].get_computer_name()
                log_obj["SID"] = self.evtx_file.records[i].get_user_security_identifier()
                log_num_object = dict()
                log_num_object["no"+str(i)] = log_obj
                json_list.append(log_num_object)
            return json_list

        def eventID(self, num):
            for i in range(0, len(self.evtx_json)):
                if self.evtx_json[i]['no'+str(i)]['eventID'] == num:
                    print(self.evtx_json[i])

        def level(self, num):
            for i in  range(0, len(self.evtx_json)):
                if self.evtx_json[i]['no'+str(i)]['level'] == num:
                    print(self.evtx_json[i])

        def xml_with_num(self, num):
            print(self.evtx_file.records[num].get_xml_string())

    class WebLogAnalysis:
        def __init__(self, file):
            self.file = file
            self.weblog_json = self.make_json()

        def make_json(self):
            idx = 0
            json_list = []
            while True:
                line = self.file.readline()
                if line == '':
                    break
                elif line[0] == '#' and line[0:7] != '#Fields':
                    continue
                if line[0:7] == '#Fields':
                    fields = line.split(' ')
                else:
                    log_line = line.split()
                    log_obj = dict()
                    for i in range(1, len(fields)):
                        log_obj[fields[i]] = log_line[i-1]
                    json_list.append({'no'+str(idx): log_obj})
                    idx = idx+1
            return json_list

        def show_all_record(self):
            for i in self.weblog_json:
                print(i)

        def date(self, date):
            for i in range(0, len(self.weblog_json)):
                if self.weblog_json[i]['no'+str(i)]['date'] == date:
                    print(self.weblog_json[i])


class FilesAnalysis:
    def __init__(self, file):
        self.file = file

        
class RegAnalysis:
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
                            reg_key_obj = {
                                "find_keyword" : find_val,
                                "key" : key.path()
                            }
                            print (print(json.dumps(reg_key_obj)))

    def find_key(self, keyword):
        self.rec(self.reg.root(), self.find_path, keyword)

    def get_recent_docs(self):
        recent = self.reg.open("SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs")
        for i, v in enumerate(recent.values()):
            reg_obj  = {
                    "time" : str(recent.timestamp()),
                    "name" : v.name(),
                    "data" : v.value().decode('utf-16')}
            print(json.dumps(reg_obj))
            #print ('{} > {} : {}'.format(recent.timestamp(), v.name(), v.value().decode('utf-16')))
    
    def get_recent_MRU(self):
        recent = self.reg.open("Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU")
        for i, v in enumerate(recent.values()):
            reg_obj  = {
                    "time" : str(recent.timestamp()),
                    "name" : v.name(),
                    "data" : v.value().decode('utf-16')}
            print(json.dumps(reg_obj))
    
    def recent_excel(self):
        recent = self.reg.open("Software\\Microsoft\\Office\\11.0\\Excel\\Recent Files")
        for i, v in enumerate(recent.values()):
            reg_obj  = {
                    "time" : str(recent.timestamp()),
                    "path" : v.value()}
            print(json.dumps(reg_obj))
            
    def get_recent_ppt(self):
        recent = self.reg.open("Software\\Microsoft\\Office\\11.0\\PowerPoint\\Recent File List")
        for i, v in enumerate(recent.values()):
            reg_obj  = {
                    "time" : str(recent.timestamp()),
                    "path" : v.value()}
            print(json.dumps(reg_obj))
            
            
class System_temp_analysis:
    def __init__(self, file):
        self._file = file

    def get_temp(self, path):
        files = [f for f in listdir(path)]

        for i in range(files.__len__()):
            print("[%d] "%(i+1) + files[i])

        file_count = files.__len__()
        file_size = files.__sizeof__()
        print("File Count : %d" %file_count)
        print("File Size : %d" %file_size)

