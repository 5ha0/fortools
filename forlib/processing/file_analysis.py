import json
from os import listdir
from lxml import etree
import datetime
from Registry import Registry
import os.path, time
from argparse import ArgumentParser
import binascii
import ctypes
from datetime import datetime,timedelta
import ntpath
import os
import struct
import sys
import tempfile
import forlib.processing.reg_analysis as regf

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
    def NTUSER(file):
        return regf.NTAnalysis(file)

    def SYSTEM(file):
        return regf.SYSAnalysis(file)
            
            
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
        
        

