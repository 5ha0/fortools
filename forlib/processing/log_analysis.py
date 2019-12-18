import xmltodict
import json
import datetime
import re
import forlib.calc_hash as calc_hash
from forlib.processing.filter import Filter
from datetime import datetime, timedelta, timezone
from forlib.processing.convert_time import get_timezone


# analysis part for event file
class EventAnalysis:

    def __init__(self, file, path, hash_v):
        self._result = []
        self.__evtx_file = file
        self.__evtx_json = self.__make_json()
        self.Favorite = Favorite(self.__evtx_json)
        self.__hash_value = [hash_v]
        self.__path = path
        self.__cal_hash()

    def show_all_info(self):
        for i in self.__evtx_json:
            print(i)

    def get_all_info(self):
        return self.__evtx_json

    def __make_json(self):
        json_list = []
        for i in range(0, len(self.__evtx_file.records)):
            log_obj = dict()
            log_obj["number"] = i
            log_obj["eventID"] = self.__evtx_file.records[i].get_event_identifier()
            time_zone = get_timezone()
            c_time = self.__evtx_file.records[i].get_creation_time().replace(
                tzinfo=timezone(timedelta(minutes=time_zone))) + timedelta(minutes=time_zone)
            log_obj["create Time"] = c_time.strftime("%Y-%m-%d %H:%M:%S")
            log_obj["TimeZone"] = c_time.strftime("%Z")
            log_obj["level"] = self.__evtx_file.records[i].get_event_level()
            log_obj["source"] = self.__evtx_file.records[i].get_source_name()
            log_obj["computer Info"] = self.__evtx_file.records[i].get_computer_name()
            log_obj["SID"] = self.__evtx_file.records[i].get_user_security_identifier()
            json_list.append(log_obj)
        return json_list

    def __cal_hash(self):
        self.__hash_value.append(calc_hash.get_hash(self.__path, 'after'))

    def get_hash(self):
        return self.__hash_value

    def get_string(self):
        json_list = []
        if self.__evtx_file.number_of_records > 0:
            for i in range(0, len(self.__evtx_file.records)):
                dict_type = xmltodict.parse(self.__evtx_file.records[i].get_xml_string())
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
        result = []
        if type(num) is not int:
            print('Parameter of eventid() is int variable.\nPlz check your input.')
            return -1
        for i in range(0, len(self.__evtx_json)):
            if self.__evtx_json[i]['eventID'] == num:
                result.append(self.__evtx_json[i])
        return result

    def level(self, num):
        result = []
        for i in range(0, len(self.__evtx_json)):
            if self.__evtx_json[i]['level'] == num:
                result.append(self.__evtx_json[i])
        return result

    def date(self, date1, date2):
        return Filter.date("create Time", [date1, date2], self.__evtx_json)

    def time(self, time1, time2):
        return Filter.time("create Time", [time1, time2], self.__evtx_json)

    def day(self, day1, day2):
        return Filter.day("create Time", [day1, day2], self.__evtx_json)

    def xml_with_num(self, num):
        if num > len(self.__evtx_json):
            print('Plz check idx.')
        else:
            print(self.__evtx_file.records[num].get_xml_string())


# favorite method for evtx log
class Favorite:
    def __init__(self, json):
        self.__evtx_json = json
        self.Account = Account(self.__evtx_json)
        self.System = System(self.__evtx_json)
        self.Etc = Etc(self.__evtx_json)


class Etc:
    def __init__(self, evtx_json):
        self.__evtx_json = evtx_json

    # detect remote logon record
    def remote(self):
        return EventAnalysis.eventid(self, 540) + EventAnalysis.eventid(self, 4776)

    # app error(1000), app hang(1002)
    def app_crashes(self):
        return EventAnalysis.eventid(self, 1000) + EventAnalysis.eventid(self, 1002)

    # windows error reporting(1001)
    def error_report(self):
        return EventAnalysis.eventid(self, 1001)

    def service_fails(self):
        return EventAnalysis.eventid(self, 7022) + EventAnalysis.eventid(self, 7023) + EventAnalysis.eventid(self,
                                                                                                             7024) + EventAnalysis.eventid(
            self, 7026) + EventAnalysis.eventid(self, 7031) + EventAnalysis.eventid(self, 7032) + EventAnalysis.eventid(
            self, 7034)

    # rule add(2004), rule change(2005), rule deleted(2006, 2033), fail to load group policy(2009)
    def firewall(self):
        return EventAnalysis.eventid(self, 2004) + EventAnalysis.eventid(self, 2005) + EventAnalysis.eventid(self,
                                                                                                             2006) + EventAnalysis.eventid(
            self, 2009) + EventAnalysis.eventid(self, 2033)

    # new device(43), new mass storage installation(400, 410)
    def usb(self):
        return EventAnalysis.eventid(self, 43) + EventAnalysis.eventid(self, 400)+EventAnalysis.eventid(self, 410)+ EventAnalysis.eventid(self, 20001) + EventAnalysis.eventid(self,  20003)

    # starting a wireless connection(8000, 8011), successfully connected(8001), disconnect(8003), failed(8002)
    def wireless(self):
        return EventAnalysis.eventid(self, 8000) + EventAnalysis.eventid(self, 8001) + EventAnalysis.eventid(self,
                                                                                                             8002) + EventAnalysis.eventid(
            self, 8003) + EventAnalysis.eventid(self, 8011) + EventAnalysis.eventid(self,
                                                                                    10000) + EventAnalysis.eventid(self,
                                                                                                                   10001) + EventAnalysis.eventid(
            self, 11000) + EventAnalysis.eventid(self, 11001) + EventAnalysis.eventid(self,
                                                                                      11002) + EventAnalysis.eventid(
            self, 11004) + EventAnalysis.eventid(self, 11005) + EventAnalysis.eventid(self,
                                                                                      11006) + EventAnalysis.eventid(
            self, 11010) + EventAnalysis.eventid(self, 12011) + EventAnalysis.eventid(self,
                                                                                      12012) + EventAnalysis.eventid(
            self, 12013)


class System:
    def __init__(self, evtx_json):
        self.__evtx_json = evtx_json

    # window start
    def system_on(self):
        return EventAnalysis.eventid(self, 4608)

    # window shut down
    def system_off(self):
        return EventAnalysis.eventid(self, 4609) + EventAnalysis.eventid(self, 6006) + EventAnalysis.eventid(self, 1100)

    # window dirty shut down
    def dirty_shutdown(self):
        return EventAnalysis.eventid(self, 6008)


# filtering based on logon type
class Account:
    def __init__(self, evtx_json):
        self.__evtx_json = evtx_json

    # detect valid logon record
    def logon(self):
        return EventAnalysis.eventid(self, 4624)

    def logoff(self):
        return EventAnalysis.eventid(self, 4647)

    # detect failed user account login
    def login_failed(self):
        return EventAnalysis.eventid(self, 4625)

    def change_pwd(self):
        return EventAnalysis.eventid(self, 4723)

    def delete_account(self):
        return EventAnalysis.eventid(self, 4726)

    def verify_account(self):
        return EventAnalysis.eventid(self, 4720)

    def add_privileged_group(self):
        return EventAnalysis.eventid(self, 4728) + EventAnalysis.eventid(self, 4732) + EventAnalysis.eventid(self, 4756)


# analysis for LinuxLog
class LinuxLogAnalysis:
    class AuthLog:
        def __init__(self, file, path, hash_v):
            self.__file = file
            self.__parse()

        def __parse(self):
            log_parse(self.__file)

        def show_all_info(self):
            for i in range(0, len(self.__json)):
                print(self.__json[i])

        def get_all_info(self):
            return self.__json

    class SysLog:
        def __init__(self, file, path, hash_v):
            self.__file = file
            self.__parse()

        def __parse(self):
            log_parse(self.__file)

        def show_all_info(self):
            for i in range(0, len(self.__json)):
                print(self.__json[i])

        def get_all_info(self):
            return self.__json


class ApacheLog:
    class Error:
        def __init__(self, file, path, hash_v):
            self.__file = file
            self.__json = err_parse(self.__file)

        def show_all_info(self):
            for i in range(0, len(self.__json)):
                print(self.__json[i])

        def get_all_info(self):
            return self.__json

    class Access:
        def __init__(self, file, path, hash_v):
            self.__file = file
            self.__json = access_parse(self.__file)

        def show_all_info(self):
            for i in range(0, len(self.__json)):
                print(self.__json[i])

        def get_all_info(self):
            return self.__json


class IIS:
    def __init__(self, file, path, hash_v):
        self.__file = file
        self.__json = iis_parse(self.__file)

    def show_all_info(self):
        for i in self.__json:
            print(i)

    def get_all_info(self):
        return self.__json

class Others:
    def __init__(self, file, path, hash_v):
        self.__file = file
        self.__hash_value = [hash_v]
        self.__path = path
        self.__json = self.__parse()
        self.__cal_hash()

    def __parse(self):
        return other_parse(self.__file)

    def show_all_info(self):
        for i in self.__json:
            print(i)

    def get_all_info(self):
        return self.__json

    def __cal_hash(self):
        self.__hash_value.append(calc_hash.get_hash(self.__path, 'after'))

    def get_hash(self):
        return self.__hash_value


def other_parse(file):
    date_r = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
    pid = r'pid=+\d+'
    # path = r'\w+:\\\\.+'
    result = []
    while True:
        line = file.readline()
        if line == '':
            break
        try:
            log_obj = dict()
            date = datetime.strptime(str(re.search(date_r, line).group()), "%Y-%m-%d %H:%M:%S")
            log_obj["date"] = date.strftime('%Y-%m-%d')
            log_obj["time"] = date.strftime('%H:%M:%S')
            log_obj["TimeZone"] = 'system Time'
            log_obj["pid"] = re.search(pid, line).group()[4:]
            log_obj["info"] = line.split('  ')[-1]
        except:
            continue
        result.append(log_obj)
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
            date = datetime.strptime(str(re.search(date_r, line).group()), "%a %b %d %H:%M:%S.%f %Y")
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
            date = datetime.strptime(date, '%d/%b/%Y:%H:%M:%S %z')
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
        date = datetime.strptime(line_parse[0] + line_parse[1] + line_parse[2], "%b%d%H:%M:%S")
        log_obj["date"] = date.strftime('%m/%d')
        log_obj["time"] = date.strftime('%H:%M:%S')
        log_obj["TimeZone"] = 'System Time'
        log_obj["system"] = line_parse[3]
        log_obj["source"] = line_parse[4][:-1]
        for i in range(5, len(line_parse)):
            info = info + line_parse[i] + ' '
        log_obj["info"] = info
        result.append(log_obj)
    return result
