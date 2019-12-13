from Registry import Registry
import re
import codecs
from datetime import datetime, timedelta
import forlib.calc_hash as calc_hash
import time
import binascii

class RegAnalysis:
    def __init__(self, file, path, hash_val):
        self.reg = file
        self.ret_list = list()
        self.len_list = list()
        self.Favorite = Favorite(self.reg)
        self.__hash_val = [hash_val]
        self.__path = path
        self.__cal_hash()

    def __bin_to_int(self, info):
        bin_to_little_endian = bytes.decode(binascii.hexlify(info[0:][::-1]))
        int_info = int(bin_to_little_endian, 16)
        return int_info

    def __cal_time(self, info_time):
        int_time = self.__bin_to_int(info_time)
        int_time = int_time*0.1
        if int_time == 0:
            date = 'Never'
        else:
            date = datetime(1601, 1, 1) + timedelta(microseconds=int_time)
        return str(date)

    def __print_path(self, find_val, reg_key, ktime):
        split_list = reg_key.split("\\")
        key_obj = {
            "Last Written Time" : str(ktime),
            "Search Keywork" : find_val,
            "Root Key" : split_list[0],
            "Search Key Path" : "\\".join(split_list[1:])
        }
        self.ret_list.append(key_obj)
        return self.ret_list

    def __rec(self, key, get_path, find_val):
        for subkey in key.subkeys():
            get_path(subkey, find_val)
            self.__rec(subkey, get_path, find_val)

    def __get_path(self, key, find_val):
        find_pattern = re.compile(find_val)

        if find_pattern.findall(key.path()):
            self.__print_path(find_val, key.path(), key.timestamp())
        else:
            pass

    def find_key(self, keyword):
        try:
            self.__rec(self.reg.root(), self.__get_path, keyword)
            return self.ret_list
        except:
            print("[-] Plz Check the file or keyword")
            return -1

    def find_value(self, key):
        ret_list = list()
        try:
            key_path = self.reg.open(key)
        except:
            print("[-] Plz Check the path or file")
            return -1

        all_value = dict()
        time_pattern = re.compile("Time")

        for i in key_path.values():
            if time_pattern.findall(i.name()) and i.value_type() == Registry.RegBin:
                all_value[i.name()] = self.__cal_time(i.value())
            else:
                all_value["Key Path"] = key
                all_value["Last Written Time"] = str(key_path.timestamp())
                all_value[i.name()] = i.value()

        ret_list.append(all_value)
        return ret_list
    
    def get_info(self, dictonary, search_list):
        ret_list = list()
        for i in dictonary:
            info = dict()
            try:
                for j in search_list:
                    info[j] = i[j]
                ret_list.append(info)
            except:
                print("Plz check your key.")
                return -1
        return ret_list
    
    def __cal_hash(self):
        after_hash = calc_hash.get_hash(self.__path, 'after')
        self.__hash_val.append(after_hash)

    def get_hash(self):
        return self.__hash_val

class Favorite:
    def __init__(self, file):
        self.reg = file
        self.ret_list = list()
        self.NTAnalysis = NTAnalysis(self.reg)
        self.SYSAnalysis = SYSAnalysis(self.reg)
        self.SWAnalysis = SWAnalysis(self.reg)
        self.SAMAnalysis = SAMAnalysis(self.reg)

class NTAnalysis:
    def __init__(self, file):
        self.reg = file

    def __bin_to_int(self, info):
        bin_to_little_endian = bytes.decode(binascii.hexlify(info[0:][::-1]))
        int_info = int(bin_to_little_endian, 16)
        return int_info

    def __cal_time(self, info_time):
        int_time = self.__bin_to_int(info_time)
        int_time = int_time*0.1
        if int_time == 0:
            date = 'Never'
        else:
            date = datetime(1601, 1, 1) + timedelta(microseconds=int_time)
        return str(date)

    def get_recent_docs(self):
        ret_list = list()
        try:
            recent = self.reg.open("SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs")
        except:
            print("Plz Check the file. This file is ", self.reg.hive_type())
            return -1

        for i, v in enumerate(recent.values()):
            if i == 0:
                continue
            #print(v.value().decode('utf-16'))
            reg_obj  = {
                    "time" : str(recent.timestamp()),
                    "TimeZone" : "UTC",
                    "name" : v.name(),
                    "data" : v.value().decode('utf-16').split('\x00')[0]}
            ret_list.append(reg_obj)
        return ret_list

    def get_recent_MRU(self):
        ret_list = list()
        try:
            recent = self.reg.open("Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU")
        except:
            print("Plz Check the file. This file is ", self.reg.hive_type())
            return -1

        for i, v in enumerate(recent.values()):
            reg_obj  = {
                    "time" : str(recent.timestamp()),
                    "TimeZone" : "UTC",
                    "name" : v.name(),
                    "data" : v.value()}
            ret_list.append(reg_obj)
        return ret_list
    
    def get_IE_visit(self):
        ret_list = list()
        try:
            recent = self.reg.open("Software\Microsoft\Internet Explorer\TypedURLs")
        except:
            print("Plz Check the file. This file is ", self.reg.hive_type())
            return -1

        for i, v in enumerate(recent.values()):
            #print(v.value().decode('utf-16'))
            reg_obj  = {
                    "time" : str(recent.timestamp()),
                    "TimeZone" : "UTC",
                    "data" : v.value()}
            ret_list.append(reg_obj)
        return ret_list
    
    def __print_ms(self, recent, version):
        ms_list = list()
        #print("recent.values : ", dir(recent.values()[0]))
        #print("raw_data      : ", recent.values()[0].raw_data())
        #print("raw_data      : ", recent.values()[0].raw_data().decode("utf-16"))
        for i, v in enumerate(recent.values()):
            file_name = v.raw_data().decode('utf-16').split("*")[1]
            reg_obj = {
                    "Version" : version,
                    "MS Key Last Written time" : recent.timestamp().strftime('%Y-%m-%d %H:%M:%S'),
                    "TimeZone" : "UTC",
                    "path" : file_name[:-1]
                    }
            ms_list.append(reg_obj)
        return ms_list

    def get_ms_office(self):
        ret_list = list()
        try:
            path  = "Software\\Microsoft\\Office"
            version = self.reg.open(path)
        except:
            print("Plz Check the file. This file is ", self.reg.hive_type())
            return -1

        temp_list = list()
        a = list()
        for items in version.subkeys():
            try:
                float(items.name())
                a.append(items.name())
            except:
                pass

        for i in range(len(a)):
            if a[i] == '11.0':
                try:
                    recent1 = self.reg.open(path + "\\%s\\Excel\\Recent Files" %(a[i]))
                    xls = self.__print_ms(recent1, a[i])
                except:
                    xls = []

                try:
                    recent2 = self.reg.open(path + "\\%s\\PowerPoint\\Recent File List" %(a[i]))
                    ppt = self.__print_ms(recent2, a[i])
                except:
                    ppt = []

                try:
                    recent3 = self.reg.open(path + "\\%s\\Word\\Recent File List" %(a[i]))
                    word = self.__print_ms(recent3, a[i])
                except:
                    word = []
                temp_list = xls+ppt+word

            if a[i] == '15.0' or a[i] == '12.0':
                outlook = list()
                try:
                    recent0 = self.reg.open(path+"\\%s\\Outlook\\PST" %a[i])
                    for i, v in enumerate(recent0.values()):
                        file_name = v.raw_data().decode('utf-16')
                        reg_obj = {
                                "Version" : a[i],
                                "MS Key Last Written time" : recent0.timestamp().strftime('%Y-%m-%d %H:%M:%S'),
                                "TimeZone" : "UTC",
                                "path" : file_name[:-1]
                            }
                        outlook.append(reg_obj)

                except:
                    outlook = []

                try:
                    recent1 = self.reg.open(path + "\\%s\\Excel\\File MRU" %a[i])
                    xls = self.__print_ms(recent1, a[i])
                except:
                    xls = []

                try:
                    recent2 = self.reg.open(path + "\\%s\\PowerPoint\\File MRU" %a[i])
                    ppt = self.__print_ms(recent2, a[i])
                except:
                    ppt = []

                try:
                    recent3 = self.reg.open(path + "\\%s\\Word\\File MRU" %a[i])
                    word = self.__print_ms(recent3, a[i])
                except:
                    word = []

                temp_list = outlook+xls+ppt+word

            if a[i] == '16.0':
                try:
                    path2 = path + "\\%s\\Excel\\User MRU"%(a[i])
                    path2 = path + "\\%s\\PowerPoint\\User MRU"%(a[i])
                    path2 = path + "\\%s\\Word\\User MRU" % (a[i])
                    LiveId = self.reg.open(path2)
                    outlook = list()
                    b = list()
                    for items in LiveId.subkeys():
                        b.append(items.name())
                except:
                    try:
                        outlook = list()
                        recent0 = self.reg.open(path + "\\%s\\Outlook\\Search" % a[i])
                        for v in recent0.values():
                            ret_obj = {
                                "Version": a[i],
                                "MS key Last Written time": str(recent0.timestamp()),
                                "TimeZone": "UTC",
                                "path": v.name()
                            }
                            outlook.append(ret_obj)

                    except:
                        outlook = []

                try:
                    recent0 = self.reg.open(path+"\\%s\\Outlook\\Search" %a[i])
                    for v in recent0.values():
                        ret_obj = {
                            "Version" : a[i],
                            "MS key Last Written time" : str(recent0.timestamp()),
                            "TimeZone" : "UTC",
                            "path" : v.name()
                        }
                        outlook.append(ret_obj)

                except:
                    outlook = []

                try:
                    recent1 = self.reg.open(path + "\\%s\\Excel\\User MRU\\%s\\File MRU" %(a[i], b[0]))
                    xls = self.__print_ms(recent1, a[i])
                except:
                    xls = []

                try:
                    recent2 = self.reg.open(path + "\\%s\\PowerPoint\\User MRU\\%s\\File MRU" %(a[i], b[0]))
                    ppt = self.__print_ms(recent2, a[i])
                except:
                    ppt = []

                try:
                    recent3 = self.reg.open(path + "\\%s\\Word\\User MRU\\%s\\File MRU" %(a[i], b[0]))
                    word = self.__print_ms(recent3, a[i])
                except:
                    word = []

                temp_list = outlook+xls+ppt+word
            ret_list = ret_list + temp_list
        return ret_list
            #ret_ms.append(self.print_ms(recent1))

    def get_userassist(self):
        ret_list = list()
        # CE : 실행파일 목록
        # F4 : 바로가기 목록
        try:
            path = "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist"
            user_list = list()
            user = self.reg.open(path)
        except:
            print("Plz Check the file. This file is ", self.reg.hive_type())
            return -1

        for items in user.subkeys():
            keys = self.reg.open(path+"\\%s" %(items.name()))
            for userassist_keys in keys.subkeys():
                for userassist_values in userassist_keys.values():
                    file_name = codecs.decode(userassist_values.name(), 'rot_13')
                    reg_obj = {
                        "Time" : self.__cal_time(userassist_values.value()[60:68]),
                        "TimeZone" : "UTC",
                        "Run Count" : self.__bin_to_int(userassist_values.value()[4:8]),
                        "file" : '%s' % file_name
                    }
                    user_list.append(reg_obj)
        ret_list = sorted(user_list, key=lambda e: (e['Time']))
        return ret_list


class SYSAnalysis:
    def __init__(self, file):
        self.reg = file

    def __control_set_check(self, file):
        key = file.open("Select")
        for v in key.values():
            if v.name() == "Current":
                return v.value()

    def get_computer_info(self):
        ret_list = list()
        try:
            path = "ControlSet00%s\\services\\Tcpip\\Parameters" % self.__control_set_check(self.reg)
            computer_path = self.reg.open(path)
            network_dict = dict()
        except:
            print("Plz Check the file. This file is ", self.reg.hive_type())
            return -1

        for v in computer_path.values():
            if v.name() == "ICSDomain":
                network_dict['ICSDomain'] = v.value()
            if v.name() == "DataBasePath":
                network_dict['DataBasePath'] = v.value()
            if v.name() == "Hostname":
                network_dict['Hostname'] = v.value()
            if v.name() == "DhcpNameServer":
                network_dict['DhcpNameServer'] = v.value()
            if v.name() == "DhcpDomain":
                network_dict['DhcpDomain'] = v.value()

        if (not 'ICSDomain' in network_dict) or (network_dict['ICSDomain'] == ''):
            network_dict['ICSDomain'] = "N/A"
        if (not 'DataBasePath' in network_dict) or (network_dict['DataBasePath'] == ''):
            network_dict['DataBasePath'] = "N/A"
        if (not 'Hostname' in network_dict) or (network_dict['Hostname'] == ''):
            network_dict['Hostname'] = "N/A"
        if (not 'DhcpNameServer' in network_dict) or (network_dict['DhcpNameServer'] == ''):
            network_dict['DhcpNameServer'] = "N/A"
        if (not 'DhcpDomain' in network_dict) or (network_dict['DhcpDomain'] == ''):
            network_dict['DhcpDomain'] = "N/A"

        net_obj = {
                "ICSDomain" : network_dict['ICSDomain'],
                "DataBasePath" : network_dict['DataBasePath'],
                "Hostname" : network_dict['Hostname'],
                "DhcpNameServer" : network_dict['DhcpNameServer'],
                "DhcpDomain" : network_dict['DhcpDomain']
            }
        ret_list.append(net_obj)
        return ret_list

    def get_USB(self):
        ret_list = list()
        stor_list = list()
        usb_obj = dict()

        try:
            path = "ControlSet00%s\\Enum\\USBSTOR" %self.__control_set_check(self.reg)
            recent = self.reg.open(path)
        except:
            print("Plz Check the file. This file is ", self.reg.hive_type())
            return -1

        for v in recent.subkeys():
            stor_list.append(v.name())

        for i in stor_list:
            key2 = self.reg.open(path + "\\%s" % i)
            for v in key2.subkeys():
                key3 = self.reg.open(path + "\\%s\\%s" %(i, v.name()))
                for k in key3.values():
                    usb_obj["Device Name"] = i
                    usb_obj[k.name()] = k.value()
                ret_list.append(usb_obj)
        return ret_list

    def get_timezone(self):
        ret_list = list()
        try:
            path = "ControlSet00%s\\Control\\TimeZoneInformation" % self.__control_set_check(self.reg)
            time_file = self.reg.open(path)
            time_dict = dict()
        except:
            print("Plz Check the file. This file is ", self.reg.hive_type())
            return -1

        for v in time_file.values():
            if v.name() == "Bias":
                time_dict['Bias'] = v.value()
            if v.name() == "TimeZoneKeyName":
                time_dict['TimeZoneKeyName'] = v.value()
            if v.name() == "ActiveTimeBias":
                time_dict['ActiveTimeBias'] = v.value()

        if (not 'Bias' in time_dict) or (time_dict['Bias'] == ''):
            time_dict['Bias'] = "N/A"
        if (not 'TimeZoneKeyName' in time_dict) or (time_dict['TimeZoneKeyName'] == ''):
            time_dict['TimeZoneKeyName'] = "N/A"
        if (not 'ActiveTimeBias' in time_dict) or (time_dict['ActiveTimeBias'] == ''):
            time_dict['ActiveTimeBias'] = "N/A"

        time_obj = {
            "Bias" : time_dict["Bias"],
            "TimeZoneKeyName" : time_dict["TimeZoneKeyName"],
            "ActiveTimeBias" : time_dict['ActiveTimeBias']
        }

        ret_list.append(time_obj)
        return ret_list


    def get_network_info(self):
        ret_list = list()
        try:
            path = "ControlSet00%s\\services\\Tcpip\\Parameters\\Interfaces" % self.__control_set_check(self.reg)
            net_key = self.reg.open(path)
        except:
            print("Plz Check the file. This file is ", self.reg.hive_type())
            return -1

        guid_list = list()
        network_dict = dict()

        for v in net_key.subkeys():
            guid_list.append(v.name())

        for i in guid_list:
            key3 = self.reg.open(path + "\\%s" % i)
            for v in key3.values():
                if v.name() == "Domain":
                    network_dict['Domain'] = v.value()
                if v.name() == "IPAddress":
                    # Sometimes the IP would end up in a list here so just doing a little check
                    network_dict['IPAddress'] = v.value()[0]
                if v.name() == "DhcpIPAddress":
                    network_dict['DhcpIPAddress'] = v.value()
                if v.name() == "DhcpServer":
                    network_dict['DhcpServer'] = v.value()
                if v.name() == "DhcpSubnetMask":
                    network_dict['DhcpSubnetMask'] = v.value()

            if (not 'Domain' in network_dict) or (network_dict['Domain'] == ''):
                network_dict['Domain'] = "N/A"
            if (not 'IPAddress' in network_dict) or (network_dict['IPAddress'] == ''):
                network_dict['IPAddress'] = "N/A"
            if (not 'DhcpIPAddress' in network_dict) or (network_dict['DhcpIPAddress'] == ''):
                network_dict['DhcpIPAddress'] = "N/A"
            if (not 'DhcpServer' in network_dict) or (network_dict['DhcpServer'] == ''):
                network_dict['DhcpServer'] = "N/A"
            if (not 'DhcpSubnetMask' in network_dict) or (network_dict['DhcpSubnetMask'] == ''):
                network_dict['DhcpSubnetMask'] = "N/A"

            net_obj = {
                "Domain" : network_dict['Domain'],
                "IPAddress" : network_dict['IPAddress'],
                "DhcpIPAddress" : network_dict['DhcpIPAddress'],
                "DhcpServer" : network_dict['DhcpServer'],
                "DhcpSubnetMask" : network_dict['DhcpSubnetMask']
            }
            ret_list.append(net_obj)
        return ret_list


class SWAnalysis:
    def __init__(self, file):
        self.reg = file

    def __control_set_check(self, file):
        key = file.open("Select")
        for v in key.values():
            if v.name() == "Current":
                return v.value()

    def get_info(self):
        ret_list = list()
        try:
            os_info = self.reg.open("Microsoft\\Windows NT\\CurrentVersion")
            os_dict = dict()
        except:
            print("Plz Check the file. This file is ", self.reg.hive_type())
            return -1

        for v in os_info.values():
            if v.name() == "CurrentVersion":
                os_dict['CurrentVersion'] = v.value()
            if v.name() == "CurrentBuild":
                os_dict['CurrentBuild'] = v.value()
            if v.name() == "InstallDate":
                os_dict['InstallDate'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(v.value()))
            if v.name() == "RegisteredOwner":
                os_dict['RegisteredOwner'] = v.value()
            if v.name() == "EditionID":
                os_dict['EditionID'] = v.value()
            if v.name() == "ProductName":
                os_dict['ProductName'] = v.value()

        if (not 'CurrentVersion' in os_dict) or (os_dict['CurrentVersion'] == ''):
            os_dict['CurrentVersion'] = "N/A"
        if (not 'CurrentBuild' in os_dict) or (os_dict['CurrentBuild'] == ''):
            os_dict['CurrentBuild'] = "N/A"
        if (not 'InstallDate' in os_dict) or (os_dict['InstallDate'] == ''):
            os_dict['InstallDate'] = "N/A"
        if (not 'TimeZone' in os_dict) or (os_dict['TimeZone'] == ''):
            os_dict['TimeZone'] = "N/A"
        if (not 'RegisteredOwner' in os_dict) or (os_dict['RegisteredOwner'] == ''):
            os_dict['RegisteredOwner'] = "N/A"
        if (not 'EditionID' in os_dict) or (os_dict['EditionID'] == ''):
            os_dict['EditionID'] = "N/A"
        if (not 'ProductName' in os_dict) or (os_dict['ProductName'] == ''):
            os_dict['ProductName'] = "N/A"

        os_obj = {
            "CurrentVersion" : os_dict['CurrentVersion'],
            "CurrentBuild" : os_dict['CurrentBuild'],
            "InstallDate" : os_dict['InstallDate'],
            "TimeZone" : "UTC",
            "RegisteredOwner" : os_dict['RegisteredOwner'],
            "EditionID" : os_dict['EditionID'],
            "ProductName" : os_dict['ProductName']
        }
        ret_list.append(os_obj)

        return ret_list

    def get_network_info(self):
        ret_list = list()
        try:
            key = self.reg.open("Microsoft\\Windows NT\\CurrentVersion\\NetworkCards")
        except:
            print("Plz Check the file. This file is ", self.reg.hive_type())
            return -1

        card_num = list()
        network_info = dict()
        for v in key.subkeys():
            card_num.append(v.name())

        for item in card_num:
            path = self.reg.open("Microsoft\\Windows NT\\CurrentVersion\\NetworkCards\\%s" %item)
            for v in path.values():
                if v.name() == "ServiceName":
                    network_info['ServiceName'] = v.value()
                if v.name() == "Description":
                    network_info['Description'] = v.value()

            if (not 'ServiceName' in network_info) or (network_info['ServiceName'] == ''):
                network_info['ServiceName'] = "N/A"
            if (not 'Description' in network_info) or (network_info['Description'] == ''):
                network_info['Description'] = "N/A"

            net_obj = {
                "ServiceName" : network_info['ServiceName'],
                "Description" : network_info['Description']
            }
            ret_list.append(net_obj)
        return ret_list


class SAMAnalysis:
    def __init__(self, file):
        self.reg = file

    def __bin_to_int(self, info):
        bin_to_little_endian = bytes.decode(binascii.hexlify(info[0:][::-1]))
        int_info = int(bin_to_little_endian, 16)
        return int_info

    def __cal_time(self, info_time):
        int_time = self.__bin_to_int(info_time)
        int_time = int_time*0.1
        if int_time == 0:
            date = 'Never'
        else:
            date = datetime(1601, 1, 1) + timedelta(microseconds=int_time)
        return str(date)

    def last_login(self):
        ret_list = list()
        try:
            last_list = self.user_info()
        except:
            print("Plz Check the file. This file is ", self.reg.hive_type())
            return -1

        login_list = list()
        for i in range(len(last_list)):
            if last_list[i]['Last Login'] == "Never":
                pass
            else:
                login_list.append(last_list[i])

        sort_list = sorted(login_list, key=lambda e: (e['Last Login']))
        last = len(sort_list)
        ret_list.append(sort_list[last-1])
        return ret_list

    def user_name(self):
        ret_list = list()
        try:
            user_path = "SAM\\Domains\\Account\\Users\\Names"
            user = self.reg.open(user_path)
        except:
            print("Plz Check the file. This file is ", self.reg.hive_type())
            return -1

        for items in user.subkeys():
            user_obj = {
                    'UserName' : items.name(),
                    'Last Written Time' : items.timestamp().strftime("%Y-%m-%d %H:%M:%S"),
                    'TimeZone' : "UTC"
                }
            ret_list.append(user_obj)
        return ret_list

    def user_info(self):
        ret_list = list()
        try:
            user_path = "SAM\\Domains\\Account\\Users"
            user = self.reg.open(user_path)
        except:
            print("Plz Check the file. This file is ", self.reg.hive_type())
            return -1

        ret_list1 = list()
        ret_list2 = list()
        for items in user.subkeys():
            path2 = self.reg.open(user_path+"\\%s"%(items.name()))
            for info_key in path2.values():
                if info_key.name() == "F":
                    info_data = info_key.value()
                    user_obj = {
                        'Last Login' : self.__cal_time(info_data[8:16]),
                        'Last PW Change' : self.__cal_time(info_data[24:32]),
                        'Log Fail Time' : self.__cal_time(info_data[40:48]),
                        'TimeZone' : "UTC",
                        'RID' : self.__bin_to_int(info_data[48:52]),
                        'Logon Success Count' : self.__bin_to_int(info_data[64:66]),
                        'Logon Fail Count' : self.__bin_to_int(info_data[66:68])
                    }
                    ret_list1.append(user_obj)

                #V 필드에서는 기본적으로 offset CC 부터 상재값으로 시작
                if info_key.name() == "V":
                    info_data = info_key.value()
                    user_offset = self.__bin_to_int(info_data[12:16]) + 0xCC
                    user_len = self.__bin_to_int(info_data[16:24])

                    user_obj = {
                        'UserName' : info_data[user_offset:user_offset+user_len].decode('utf16')
                    }
                    ret_list2.append(user_obj)
        for i in range(len(ret_list1)):
            ret_list1[i].update(ret_list2[i])

        return ret_list1
