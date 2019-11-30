import xmltodict
import json
import datetime
import re
import forlib.calc_hash as calc_hash
from forlib.processing.filter import custom_filter as filter_method
from forlib.processing.filter import date_filter as date_filter
from forlib.processing.filter import time_filter as time_filter
from forlib.processing.filter import day_filter as day_filter


# analysis part for event file
class EventAnalysis:
    time_cnt = []

    def __init__(self, file, path, hash_v):
        self._result = []
        self.evtx_file = file
        self.evtx_json = self.__make_json()
        self.Favorite = Favorite(self.evtx_json)
        self.__hash_value = [hash_v]
        self.__path = path
        self.__cal_hash()

    def show_all_record(self):
        for i in self.evtx_json:
            print(i)
        return self.evtx_json

    def __make_json(self):
        time_cnt = dict()
        json_list = []
        for i in range(0, len(self.evtx_file.records)):
            log_obj = dict()
            log_obj["number"] = i
            log_obj["eventID"] = self.evtx_file.records[i].get_event_identifier()
            log_obj["create Time"] = str(self.evtx_file.records[i].get_creation_time())
            date = log_obj["create Time"][:7]
            if time_cnt.get(date):
                time_cnt[date] = time_cnt[date] + 1
            else:
                time_cnt[date] = 1
            log_obj["TimeZone"] = 'UTC+0'
            log_obj["level"] = self.evtx_file.records[i].get_event_level()
            log_obj["source"] = self.evtx_file.records[i].get_source_name()
            log_obj["computer Info"] = self.evtx_file.records[i].get_computer_name()
            log_obj["SID"] = self.evtx_file.records[i].get_user_security_identifier()
            json_list.append(log_obj)
        self.time_cnt = time_cnt
        return json_list

    def __cal_hash(self):
        self.__hash_value.append(calc_hash.get_hash(self.__path))

    def get_hash(self):
        return self.__hash_value

    def filtering(self, filter_list):
        self._result = filter_method(filter_list, self.evtx_json)
        return self._result

    def date_cnt(self):
        return self.time_cnt

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
                except Exception as e:
                    pass
        return json_list

    def eventid(self, num):
        for i in range(0, len(self.evtx_json)):
            if self.evtx_json[i]['eventID'] == num:
                self._result.append(self.evtx_json[i])
        return self._result

    def level(self, num):
        for i in range(0, len(self.evtx_json)):
            if self.evtx_json[i]['level'] == num:
                self._result.append(self.evtx_json[i])
        return self._result

    def date(self, date1, date2):
        return date_filter("create Time", [date1, date2], self.evtx_json)

    def time(self, time1, time2):
        return time_filter("create Time", [time1, time2], self.evtx_json)

    def day(self, day1, day2):
        return day_filter("create Time", [day1, day2], self.evtx_json)

    def xml_with_num(self, num):
        print(self.evtx_file.records[num].get_xml_string())


# favorite method for evtx log
class Favorite:
    def __init__(self, json):
        self._result = []
        self.evtx_json = json
        self.Account = Account(self.evtx_json)
        self.System = System(self.evtx_json)
        self.Etc = Etc(self.evtx_json)


class Etc:
    def __init__(self, evtx_json):
        self.evtx_json = evtx_json
        self._result = []


    # detect remote logon record
    def remote(self):
        EventAnalysis.eventid(self, 540)
        EventAnalysis.eventid(self, 4776)
        return self._result

    # app error(1000), app hang(1002)
    def app_crashes(self):
        EventAnalysis.eventid(self, 1000)
        EventAnalysis.eventid(self, 1002)
        return self._result

    # windows error reporting(1001)
    def error_report(self):
        EventAnalysis.eventid(self,1001)
        return self._result

    def service_fails(self):
        EventAnalysis.eventid(self, 7022)
        EventAnalysis.eventid(self, 7023)
        EventAnalysis.eventid(self, 7024)
        EventAnalysis.eventid(self, 7026)
        EventAnalysis.eventid(self, 7031)
        EventAnalysis.eventid(self, 7032)
        EventAnalysis.eventid(self, 7034)
        return self._result

    # rule add(2004), rule change(2005), rule deleted(2006, 2033), fail to load group policy(2009)
    def firewall(self):
        EventAnalysis.eventid(self, 2004)
        EventAnalysis.eventid(self, 2005)
        EventAnalysis.eventid(self, 2006)
        EventAnalysis.eventid(self, 2009)
        EventAnalysis.eventid(self, 2033)
        return self._result

    # new device(43), new mass storage installation(400, 410)
    def usb(self):
        EventAnalysis.eventid(self, 43)
        EventAnalysis.eventid(self, 400)
        EventAnalysis.eventid(self, 410)
        return self._result

    # starting a wireless connection(8000, 8011), successfully connected(8001), disconnect(8003), failed(8002)
    def wireless(self):
        EventAnalysis.eventid(self, 8000)
        EventAnalysis.eventid(self, 8001)
        EventAnalysis.eventid(self, 8002)
        EventAnalysis.eventid(self, 8003)
        EventAnalysis.eventid(self, 8011)
        EventAnalysis.eventid(self, 10000)
        EventAnalysis.eventid(self, 10001)
        EventAnalysis.eventid(self, 11000)
        EventAnalysis.eventid(self, 11001)
        EventAnalysis.eventid(self, 11002)
        EventAnalysis.eventid(self, 11004)
        EventAnalysis.eventid(self, 11005)
        EventAnalysis.eventid(self, 11006)
        EventAnalysis.eventid(self, 11010)
        EventAnalysis.eventid(self, 12011)
        EventAnalysis.eventid(self, 12012)
        EventAnalysis.eventid(self, 12013)
        return self._result


class System:
    def __init__(self, evtx_json):
        self.evtx_json = evtx_json
        self._result = []

    # window start
    def system_on(self):
        EventAnalysis.eventid(self, 4608)
        return self._result

    # window shut down
    def system_off(self):
        EventAnalysis.eventid(self, 4609)
        EventAnalysis.eventid(self, 6006)
        return self._result
    
    # window dirty shut down
    def dirty_shutdown(self):
        EventAnalysis.eventid(self, 6008)
        return self._result


# filtering based on logon type
class Account:
    def __init__(self, evtx_json):
        self.evtx_json = evtx_json
        self._result = []

    # detect valid logon record
    def logon(self):
        EventAnalysis.eventid(self, 4624)
        return self._result

    def logoff(self):
        EventAnalysis.eventid(self, 4647)
        return self._result

    # detect failed user account login
    def login_failed(self):
        EventAnalysis.eventid(self, 4625)
        return self._result

    def change_pwd(self):
        EventAnalysis.eventid(self, 4723)
        return self._result

    def delete_account(self):
        EventAnalysis.eventid(self, 4726)
        return self._result

    def verify_account(self):
        EventAnalysis.eventid(self, 4720)
        return self._result

    def add_privileged_group(self):
        EventAnalysis.eventid(self, 4728)
        EventAnalysis.eventid(self, 4732)
        EventAnalysis.eventid(self, 4756)
        return self._result


# analysis for LinuxLog
class LinuxLogAnalysis:
    class AuthLog:
        def __init__(self, file):
            self.__file = file
            self.__parse()

        def __parse(self):
            log_parse(self.__file)

    class SysLog:
        def __init__(self, file):
            self.__file = file
            self.__parse()

        def __parse(self):
            log_parse(self.__file)


class ApacheLog:
    class Error:
        def __init__(self, file):
            self.__file = file
            self.__json = err_parse(self.__file)

        def show_info(self):
            for i in range(0, len(self.__json)):
                print(self.__json[i])

        def get_info(self):
            return self.__json

        def date(self, date):
            result = []
            for i in range(1, len(self.__json)):
                if self.__json[i]["date"] == date:
                    result.append(self.__json[i])
            return result

        def pid(self, pid):
            result = []
            for i in range(1, len(self.__json)):
                if self.__json[i]["pid"] == pid:
                    result.append(self.__json[i])
            return result

    class Access:
        def __init__(self, file):
            self.__file = file
            self.__json = access_parse(self.__file)

        def show_info(self):
            for i in range(0, len(self.__json)):
                print(self.__json[i])

        def get_info(self):
            return self.__json

        def date(self, date):
            result = []
            for i in range(1, len(self.__json)):
                if self.__json[i]["date"] == date:
                    result.append(self.__json[i])
            return result

        def ip(self, ip):
            result = []
            for i in range(1, len(self.__json)):
                if self.__json[i]["ip"] == ip:
                    result.append(self.__json[i])
            return result

        def method(self, method):
            result = []
            for i in range(1, len(self.__json)):
                if self.__json[i]["method"] == method:
                    result.append(self.__json[i])
            return result

        def respond(self, respond):
            result = []
            for i in range(1, len(self.__json)):
                if int(self.__json[i]["respond code"]) == respond:
                    result.append(self.__json[i])
            return result


class IIS:
    def __init__(self, file):
        self.__file = file
        self.__json = iis_parse(self.__file)

    def show_info(self):
        for i in self.__json:
            print(i)

    def date(self, date):
        result = []
        for i in range(0, len(self.__json)):
            if self.__json[i]['no' + str(i)]['date'] == date:
                result.append(self.__json[i])
        return result

    def cs_method(self, method):
        result = []
        for i in range(0, len(self.__json)):
            if self.__json[i]['no' + str(i)]['cs-method'] == method:
                result.append(self.__json[i])
        return result

    def s_port(self, port):
        result = []
        for i in range(0, len(self.__json)):
            if self.__json[i]['no' + str(i)]['s-port'] == port:
                result.append(self.__json[i])
        return result

    def sc_status(self, status):
        result = []
        for i in range(0, len(self.__json)):
            if self.__json[i]['no' + str(i)]['sc-status'] == status:
                result.append(self.__json[i])
        return result


def iis_parse(file):
    json_list = []
    fields = None
    while True:
        line = file.readline()
        if line == '':
            break
        elif line[0] == '#' and line[0:7] != '#Fields':
            continue
        if line[0:7] == '#Fields':
            fields = line.split(' ')
            continue
        try:
            log_line = line.split()
            log_obj = dict()
            for i in range(1, len(log_line) - 1):
                log_obj[fields[i]] = log_line[i - 1]
            json_list.append(log_obj)
        except:
            print('IIS Log Err, plz check format of file.')
    return json_list


def err_parse(file):
    date_r = r'\w{3} \w{3} \d{2} \d{2}:\d{2}:\d{2}.\d+ \d{4}'
    pid = r'pid +\d+'
    tid = r'tid \d+'
    info = r'AH\d+:.+'
    json_list = []
    while True:
        line = file.readline()
        if line == '':
            break
        try:
            log_obj = dict()
            date = datetime.datetime.strptime(str(re.search(date_r, line).group()), "%a %b %d %H:%M:%S.%f %Y")
            log_obj["date"] = date.strftime('%m/%d')
            log_obj["time"] = date.strftime('%H:%M:%S')
            log_obj["TimeZone"] = 'system Time'
            log_obj["pid"] = re.search(pid, line).group()[4:]
            log_obj["tid"] = re.search(tid, line).group()[4:]
            log_obj["info"] = re.search(info, line).group()
        except:
            continue
        json_list.append(log_obj)
    return json_list


def access_parse(file):
    ip = r'(\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3})|(::1)'
    date_r = r'\d{1,2}/\w{1,3}/\d{1,4}:\d{2}:\d{2}:\d{2} [+]\d{4}'
    method = r'GET|PUSH|PUT|POST|HEAD|OPTIONS|Head|T'
    respond = r' \d{3} '
    uri = r'( /+\S+)|( \*)'
    url = r'(http|https)://\S+'

    json_list = []
    while True:
        line = file.readline()
        if line == '':
            break
        log_obj = dict()
        try:
            log_obj["ip"] = re.search(ip, line).group()
            date = re.search(date_r, line).group()
            date = datetime.datetime.strptime(date, '%d/%b/%Y:%H:%M:%S %z')
            log_obj["date"] = str(date.strftime('%Y/%m/%d'))
            log_obj["TimeZone"] = 'system Time'
            log_obj["time"] = str(date.strftime('%H:%M:%S'))
            log_obj["method"] = re.search(method, line).group()
            log_obj["respond code"] = re.search(respond, line).group()[1:-1]
        except:
            continue
        try:
            log_obj["uri"] = re.search(uri, line).group()[1:]
        except:
            log_obj["uri"] = 'none'
        try:
            log_obj["url"] = re.search(url, line).group()
        except:
            log_obj["url"] = 'none'
        json_list.append(log_obj)
    return json_list


def log_parse(file):
    result = []
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
        log_obj["TimeZone"] = 'system Time'
        log_obj["system"] = line_parse[3]
        log_obj["source"] = line_parse[4][:-1]
        for i in range(5, len(line_parse)):
            info = info + line_parse[i] + ' '
        log_obj["info"] = info
        result.append(log_obj)
    return result
