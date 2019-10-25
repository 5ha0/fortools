import xmltodict
import json


class WebLogAnalysis:
    def __init__(self, file):
        self.file = file
        self.weblog_json = self.__make_json()

    def __make_json(self):
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
                    log_obj[fields[i]] = log_line[i - 1]
                json_list.append({'no' + str(idx): log_obj})
                idx = idx + 1
        return json_list

    def show_all_record(self):
        for i in self.weblog_json:
            print(i)

    def date(self, date):
        for i in range(0, len(self.weblog_json)):
            if self.weblog_json[i]['no' + str(i)]['date'] == date:
                print(self.weblog_json[i])

    def cs_method(self, method):
        for i in range(0, len(self.weblog_json)):
            if self.weblog_json[i]['no' + str(i)]['cs-method'] == method:
                print(self.weblog_json[i])

    def s_port(self, port):
        for i in range(0, len(self.weblog_json)):
            if self.weblog_json[i]['no' + str(i)]['s-port'] == port:
                print(self.weblog_json[i])

    def sc_status(self, status):
        for i in range(0, len(self.weblog_json)):
            if self.weblog_json[i]['no' + str(i)]['sc-status'] == status:
                print(self.weblog_json[i])


class EvtxAnalysis:
    result = []

    def __init__(self, file):
        self.evtx_file = file
        self.evtx_json = self.__make_json()
        self.favorite = Favorite(self.evtx_json)

    def show_all_record(self):
        for i in self.evtx_json:
            print(i)
            self.result.append(i)
        return self.result

    def get_string(self):
        json_list = []
        if self.evtx_file.number_of_records > 0:
            for i in range(0, len(self.evtx_file.records)):
                dict_type = xmltodict.parse(self.evtx_file.records[i].get_xml_string())
                json_type = json.dumps(dict_type)
                dict2_type = json.loads(json_type)
                try:
                    if dict2_type['Event']['EventData'] is not None:
                        log_obj = dict()
                        log_obj["number"] = i
                        log_obj["string"] = dict2_type['Event']['EventData']['Data']
                        json_list.append(log_obj)
                except:
                    pass
                print(log_obj)
        return json_list

    def __make_json(self):
        json_list = []
        for i in range(0, len(self.evtx_file.records)):
            log_obj = dict()
            log_obj["number"] = i
            log_obj["eventID"] = self.evtx_file.records[i].get_event_identifier()
            log_obj["create Time"] = str(self.evtx_file.records[i].get_creation_time())
            log_obj["level"] = self.evtx_file.records[i].get_event_level()
            log_obj["source"] = self.evtx_file.records[i].get_source_name()
            log_obj["computer Info"] = self.evtx_file.records[i].get_computer_name()
            log_obj["SID"] = self.evtx_file.records[i].get_user_security_identifier()
            json_list.append(log_obj)
        return json_list

    def eventid(self, num):
        for i in range(0, len(self.evtx_json)):
            if self.evtx_json[i]['eventID'] == num:
                self.result.append(self.evtx_json[i])
                print(self.evtx_json[i])
        return self.result


    def level(self, num):
        for i in range(0, len(self.evtx_json)):
            if self.evtx_json[i]['level'] == num:
                print(self.evtx_json[i])
                self.result.append(self.evtx_json[i])
        return self.result

    def xml_with_num(self, num):
        print(self.evtx_file.records[num].get_xml_string())
        return self.evtx_file.records[num].get_xml_string()


class Favorite:
    def __init__(self, json):
        self.evtx_json = json
        self.accountType = AccountType(self.evtx_json)

    def logon(self): #detect valid logon record
        EvtxAnalysis.eventid(self, 4624)

    def remote(self): #detect remote logon record
        EvtxAnalysis.eventid(self, 540)
        EvtxAnalysis.eventid(self, 4776)

    def malfind(self): #detect malfind record

    def user(self): #detect account info
        print('user')

    def authority(self): #detect time of elevation of authority
        print('user')


class AccountType: #filtering based on logon type
    def __init__(self, evtx_json):
        self.evtx_json = evtx_json

    def change_pwd(self):
        EvtxAnalysis.eventid(self, 4723)

    def delete_account(self):
        EvtxAnalysis.eventid(self, 4726)

    def verify_account(self):
        EvtxAnalysis.eventid(self, 4720)


class LinuxLogAnalysis:
    def __init__(self, file):
        self.file = file
