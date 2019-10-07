import json
from lxml import etree
import datetime
from Registry import Registry

class Evtx_analysis():
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
            json_list.append(log_obj)
        return json_list

    def eventID(self, num):
        for i in self.evtx_json:
            if i['eventID'] == num:
                print(i)

    def level(self, num):
        for i in self.evtx_json:
            if i['level'] == num:
                print(i)


class Log_analysis():
    def __init__(self, file):
        self.file = file

    def make_json(self):
        line = self.file.readline()
        log_line = line.split()
        log_obj = dict()
        log_obj["host"] = log_line[0]
        log_obj["indent"] = log_line[1]
        log_obj["AuthUser"] = log_line[2]
        log_obj["Date"] = log_line[3]
        log_obj["Request"] = log_line[4]
        log_obj["Status"] = log_line[5]
        log_obj["Bytes"] = log_line[6]
        return json.dumps(log_obj, ensure_ascii=False, indent='\t')


class Files_analysis():
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
                            reg_key_obj = {
                                "find_keyword" : find_val,
                                "key" : key.path()
                            }
                            print (print(json.dumps(reg_key_obj)))

    def get_find_key(self, keyword):
        self.rec(self.reg.root(), self.find_path, keyword)

    def recent_docs(self):
        recent = self.reg.open("SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs")
        for i, v in enumerate(recent.values()):
            reg_obj  = {
                    "time" : str(recent.timestamp()),
                    "name" : v.name(),
                    "data" : v.value().decode('utf-16')}
            print(json.dumps(reg_obj))
            #print ('{} > {} : {}'.format(recent.timestamp(), v.name(), v.value().decode('utf-16')))
