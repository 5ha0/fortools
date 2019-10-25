import xmltodict
import json
import datetime
import re


# analysis part for evtx file
class EvtxAnalysis:

    result = []

    def __init__(self, file):
        self.evtx_file = file
        self.evtx_json = self.__make_json()
        self.favorite = EvtxGet.Favorite(self.evtx_json)

    def show_all_record(self):
        for i in self.evtx_json:
            print(i)
            self.result.append(i)
        return self.result

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
                finally:
                    print(log_obj)
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

    def date(self, date):
        for i in range(0, len(self.evtx_json)):
            c_date = self.evtx_json[i]['create Time'].split('.')[0]
            if c_date == str(date):
                print(self.evtx_json[i])
                self.result.append(self.evtx_json[i])
        return self.result

    def xml_with_num(self, num):
        print(self.evtx_file.records[num].get_xml_string())
        return self.evtx_file.records[num].get_xml_string()


# favorite method for evtx log
class EvtxGet:
    class Favorite:

        result = []

        def __init__(self, json):
            self.evtx_json = json
            self.accountType = AccountType(self.evtx_json)

        # detect valid logon record
        def logon(self):
            EvtxAnalysis.eventid(self, 4624)

        # detect remote logon record
        def remote(self):
            EvtxAnalysis.eventid(self, 540)
            EvtxAnalysis.eventid(self, 4776)

        # detect malfind record
        def malfind(self):
            EvtxAnalysis.eventid(self, 4776)

        # detect time of elevation of authority
        def authority(self):
            print('user')


# filtering based on logon type
class AccountType:
    def __init__(self, evtx_json):
        self.evtx_json = evtx_json

    def change_pwd(self):
        EvtxAnalysis.eventid(self, 4723)

    def delete_account(self):
        EvtxAnalysis.eventid(self, 4726)

    def verify_account(self):
        EvtxAnalysis.eventid(self, 4720)


# analysis for LinuxLog
class LinuxLogAnalysis:
    class AuthLog:
        def __init__(self, file):
            self.file = file
            self.__parse()

        def __parse(self):
            log_parse(self.file)

    class SysLog:
        def __init__(self, file):
            self.file = file
            self.__parse()

        def __parse(self):
            log_parse(self.file)

    class ApacheLog:
        class Error:
            def __init__(self, file):
                self.file = file
                self.json = self.__parse()

            def __parse(self):
                err_parse(self.file)

        class Access:
            def __init__(self, file):
                self.file = file
                self.json = self.__parse()

            def __parse(self):
                access_parse(self.file)

            def date(self, date):
                for i in range(0, len(self.json)):
                    if self.json["date"] == date:
                        print(self.json[i])


def err_parse(file):
    while True:
        line = file.readline()
        if line == '':
            break
        line_parse = line.split(']')
        log_obj = dict()
        info = ''
        date = datetime.datetime.strptime(str(line_parse[0][1:]), "%a %b %d %H:%M:%S.%f %Y")
        log_obj["date"] = date.strftime('%m/%d')
        log_obj["time"] = date.strftime('%H:%M:%S')
        log_obj["npm"] = line_parse[2]
        log_obj["source"] = line_parse[4][:-1]
        for i in range(5, len(line_parse)):
            info = info + line_parse[i] + ' '
        log_obj["info"] = info
        print(log_obj)
    return log_obj


def log_parse(file):
    while True:
        line = file.readline()
        if line == '':
            break
        line_parse = line.split(' ')
        log_obj = dict()
        info = ''
        date = datetime.datetime.strptime(line_parse[0] + line_parse[1] + line_parse[2], "%b%d%H:%M:%S")
        log_obj["date"] = date.strftime('%m/%d')
        log_obj["time"] = date.strftime('%H:%M:%S')
        log_obj["system"] = line_parse[3]
        log_obj["source"] = line_parse[4][:-1]
        for i in range(5, len(line_parse)):
            info = info + line_parse[i] + ' '
        log_obj["info"] = info
        print(log_obj)
    return log_obj


def access_parse(file):
    err = []
    while True:
        line = file.readline()
        if line == '':
            break
        ip = r'\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}'
        date = r'\d{1,2}/\w{1,3}/\d{1,4}:\d{2}:\d{2}:\d{2} [+]\d{4}'
        method = r'GET|PUSH|PUT|POST|HEAD|OPTIONS'
        respond = r' \d{3} '
        line_parse = line.split(' ')
        log_obj = dict()
        info = ''
        try:
            log_obj["ip"] = re.search(ip, line).group()
        except:
            try:
                log_obj["ip"] = re.search('::1', line).group()
            except:
                err.append(line)
        try:
            date = re.search(date, line).group()
            date = datetime.datetime.strptime(date, '%d/%b/%Y:%H:%M:%S %z')
            log_obj["date"] = str(date.strftime('%Y/%m/%d'))
            log_obj["time"] = str(date.strftime('%H:%M:%S'))
        except:
            err.append(line)
        try:
            log_obj["method"] = re.search(method, line).group()
        except:
            err.append(line)
        try:
            log_obj["respond code"] = re.search(respond, line).group()[1:-1]
        except:
            err.append(line)
        log_obj["uri"] = line_parse[7]
        log_obj["url"] = line_parse[11]
        print(log_obj)
    return log_obj

'''
class TextLogAnalysis:
    def __init__(self, file):
        self.file = file
        self.weblog_json = self.__make_json()

    def __make_json(self):
        idx = 0
        json_list = []
        fields = None
        while True:
            line = self.file.readline()
            if line == '':
                break
            elif line[0] == '#' and line[0:7] != '#Fields':
                continue
            if line[0:7] == '#Fields':
                fields = line.split(' ')
                continue

            if fields is None:
                # apache log
                if line[0] == '[':
                    log_line = line.split(']')
                    log_obj = dict()
                    log_obj['date'] = log_line[0][1:]
                    log_obj['type'] = log_line[1][2:]
                    log_obj['pid'] = log_line[2][6:].split(':')[0]
                    log_obj['info'] = log_line[3]
                # syslog
                else:
                    try:
                        log_line = line.split(':')
                        log_line_split = log_line[2].split()
                        log_obj = dict()
                        log_time = log_line[0].split(' ')
                        log_obj['date'] = log_time[0]+' '+log_time[1]
                        log_obj['time'] = log_time[2]+':'+log_line[1]+':'+log_line_split[0]
                        log_obj['system'] = log_line_split[1]
                        log_obj['source'] = log_line_split[2]
                        log_obj['info'] = log_line[3:]
                    except:
                        print('Linux Log Err, plz check format of file.')
            else:
                try:
                    log_line = line.split()
                    log_obj = dict()
                    for i in range(1, len(log_line)-1):
                        log_obj[fields[i]] = log_line[i - 1]
                except:
                    print('Web Log Err, plz check format of file.')
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
'''
