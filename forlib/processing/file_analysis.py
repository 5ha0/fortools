import json
from lxml import etree
import datetime
from Registry import Registry

class evtx_analysis():
    def __init__(self, file):
        self.file = file
        self.evtx_xml = self.make_xml()

    def make_xml(self):
        xml_object = []
        with self.file as log:
            for record in log.records():
                xml_object.append(record.xml())
        return xml_object

    def get_event_ID(self, num):
        for i in self.evtx_xml:
            print(i)


class log_analysis():
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


class file_analysis():
    def __init__(self, file):
        self.file = file
        
class reg_analysis():
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

    def get_ms(self):
        self.rec(self.reg.root(), self.find_path, "microsoft")

    def recent_docs(self):
        recent = self.reg.open("SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs")
        for i, v in enumerate(recent.values()):
            print ('{} > {} : {}'.format(recent.timestamp(), v.name(), v.value().decode('utf-16')))
