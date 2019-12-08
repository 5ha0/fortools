from Registry import Registry
import json
import codecs
from datetime import datetime, timedelta
import forlib.calc_hash as calc_hash
import time
import binascii

class NTAnalysis:
    def __init__(self, file, path, hash_val):
        self.reg = file
        self.ret_list = list()
        self.__hash_val = [hash_val]
        self.__path = path
        self.__cal_hash()

    def __rec(self, key, get_path, find_val):
#        get_path(key, find_val)
        for subkey in key.subkeys():
            self.__rec(subkey, get_path, find_val)
        path = get_path(key,find_val)

    def __get_path(self, key, find_val):
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
        self.__rec(self.reg.root(), self.__get_path, keyword)

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
        recent = self.reg.open("SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs")
        
        for i, v in enumerate(recent.values()):
            if i == 0:
                continue
            #print(v.value().decode('utf-16'))
            reg_obj  = {
                    "time" : str(recent.timestamp()),
                    "TimeZone" : "UTC",
                    "name" : v.name(),
                    "data" : v.value().decode('utf-16').split('\x00')[0]}
            self.ret_list.append(reg_obj)
        return self.ret_list
    
    def get_recent_MRU(self):
        recent = self.reg.open("Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU")
        for i, v in enumerate(recent.values()):
            reg_obj  = {
                    "time" : str(recent.timestamp()),
                    "TimeZone" : "UTC",
                    "name" : v.name(),
                    "data" : v.value()}
            self.ret_list.append(reg_obj)
        return self.ret_list
    
    def __print_ms(self, recent):
        ret_list = list()
        #print("recent.values : ", dir(recent.values()[0]))
        #print("raw_data      : ", recent.values()[0].raw_data())
        #print("raw_data      : ", recent.values()[0].raw_data().decode("utf-16"))
        for i, v in enumerate(recent.values()):
            file_name = v.raw_data().decode('utf-16').split("*")[1]
            reg_obj = {
                    "MS Key Last Written time" : recent.timestamp().strftime('%Y-%m-%d %H:%M:%S'),
                    "TimeZone" : "UTC",
                    "path" : file_name[:-1]
                    }
            ret_list.append(reg_obj)
        return ret_list

    def get_ms_office(self): 
        path  = "Software\\Microsoft\\Office"
        version = self.reg.open(path)
        a = list()
        for items in version.subkeys():
            a.append(items.name())
        
        if a[0] == '11.0':    
            try:
                recent1 = self.reg.open(path + "\\%s\\Excel\\Recent Files" %(a[0]))
                xls = self.__print_ms(recent1)
            except:
                xls = []
                
            try:
                recent2 = self.reg.open(path + "\\%s\\PowerPoint\\Recent File List" %(a[0]))
                ppt = self.__print_ms(recent2)
            except:
                ppt = []
                
            try:
                recent3 = self.reg.open(path + "\\%s\\Word\\Recent File List" %(a[0]))
                word = self.__print_ms(recent3)
            except:
                word = []
            self.ret_list = xls+ppt+word
            return self.ret_list
        
        if a[0] == '15.0' or a[0] == '12.0':
            outlook = list()
            try:
                recent0 = self.reg.open(path+"\\%s\\Outlook\\PST" %a[0])
                for i, v in enumerate(recent0.values()):
                    file_name = v.raw_data().decode('utf-16')
                    reg_obj = {
                            "MS Key Last Written time" : recent0.timestamp().strftime('%Y-%m-%d %H:%M:%S'),
                            "TimeZone" : "UTC",
                            "path" : file_name[:-1]
                        }
                    outlook.append(reg_obj)

            except:
                outlook = []
                            
            try:
                recent1 = self.reg.open(path + "\\%s\\Excel\\File MRU" %a[0])
                xls = self.__print_ms(recent1)
            except:
                xls = []

            try:
                recent2 = self.reg.open(path + "\\%s\\PowerPoint\\File MRU" %a[0])
                ppt = self.__print_ms(recent2)
            except:
                ppt = []

            try:
                recent3 = self.reg.open(path + "\\%s\\Word\\File MRU" %a[0])
                word = self.__print_ms(recent3)
            except:
                word = []
                
            self.ret_list = outlook+xls+ppt+word
            return self.ret_list

        if a[0] == '16.0':
            path2 = path+"\\%s\\Excel\\User MRU"%(a[0])
            LiveId = self.reg.open(path2)
            outlook = list()
            b = list()
            for items in LiveId.subkeys():
                b.append(items.name())
            
            try:
                recent0 = self.reg.open(path+"\\%s\\Outlook\\Search" %a[0])
                for v in recent0.values():
                    ret_obj = {
                        "MS key Last Written time" : str(recent0.timestamp()),
                        "name" : v.name()
                    }
                    outlook.append(ret_obj)

            except:
                outlook = []
                            
            try:
                recent1 = self.reg.open(path + "\\%s\\Excel\\User MRU\\%s\\File MRU" %(a[0], b[0]))
                xls = self.__print_ms(recent1)
            except:
                xls = []

            try:
                recent2 = self.reg.open(path + "\\%s\\PowerPoint\\User MRU\\%s\\File MRU" %(a[0], b[0]))
                ppt = self.__print_ms(recent2)
            except:
                ppt = []

            try:
                recent3 = self.reg.open(path + "\\%s\\Word\\User MRU\\%s\\File MRU" %(a[0], b[0]))
                word = self.__print_ms(recent3)
            except:
                word = []

            self.ret_list = outlook+xls+ppt+word
            return self.ret_list
            #ret_ms.append(self.print_ms(recent1))
           
    def get_userassist(self):
        # CE : 실행파일 목록
        # F4 : 바로가기 목록
        path = "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist"
        user_list = list()
        user = self.reg.open(path)
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
        self.ret_list = sorted(user_list, key=lambda e: (e['Time']))
        return self.ret_list

    def __cal_hash(self):
        after_hash = calc_hash.get_hash(self.__path)
        self.__hash_val.append(after_hash)

    def get_hash(self):
        return self.__hash_val
    

class SYSAnalysis:
    def __init__(self, file, path, hash_val):
        self.reg = file
        self.ret_list = list()
        self.__hash_val = [hash_val]
        self.__path = path
        self.__cal_hash()
        
    def __rec(self, key, get_path, find_val):
#        get_path(key, find_val)
        for subkey in key.subkeys():
            self.__rec(subkey, get_path, find_val)
        path = get_path(key,find_val)

    def __get_path(self, key, find_val):
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
        self.__rec(self.reg.root(), self.__get_path, keyword)


    def __control_set_check(self, file):
        key = file.open("Select")
        for v in key.values():
            if v.name() == "Current":
                return v.value()

    def __rec(self, key, get_path, find_val):
#        get_path(key, find_val)
        for subkey in key.subkeys():
            self.__rec(subkey, get_path, find_val)
        path = get_path(key,find_val)

    def __get_path(self, key, find_val):
        for value in [v.value() for v in key.values()
                        if v.value_type() == Registry.RegSZ
                        or v.value_type() == Registry.RegExpandSZ]:
                        if find_val in value:
                            reg_key_obj = {
                                "find_keyword" : find_val,
                                "key" : key.path()
                            }
                            ret_list.append(reg_obj)
        return ret_list

    def find_key(self, keyword):
        self.__rec(self.reg.root(), self.__get_path, keyword)

    def get_computer_info(self):
        path = "ControlSet00%s\\services\\Tcpip\\Parameters" % self.__control_set_check(self.reg)
        computer_path = self.reg.open(path)
        network_dict = dict()
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
        
        net_obj = {
                "ICSDomain" : network_dict['ICSDomain'],
                "DataBasePath" : network_dict['DataBasePath'],
                "Hostname" : network_dict['Hostname'],
                "DhcpNameServer" : network_dict['DhcpNameServer'],
                "DhcpDomain" : network_dict['DhcpDomain']
            }
        self.ret_list.append(net_obj)
        return self.ret_list

    def get_USB(self):
        recent = self.reg.open("ControlSet00%s\\Enum\\USB" %self.__control_set_check(self.reg))
        for i, v in enumerate(recent.values()):
            reg_obj  = {
                    "time" : str(recent.timestamp()),
                    "TimeZone" : "UTC",
                    "path" : v.value()}
            self.ret_list.append(reg_obj)
        return self.ret_list

    def get_timezone(self):
        path = "ControlSet00%s\\Control\\TimeZoneInformation" % self.__control_set_check(self.reg)
        time_file = self.reg.open(path)
        time_dict = dict()

        for v in time_file.values():
            if v.name() == "Bias":
                time_dict['Bias'] = v.value()
            if v.name() == "TimeZoneKeyName":
                time_dict['TimeZoneKeyName'] = v.value()
            if v.name() == "ActiveTimeBias":
                time_dict['ActiveTimeBias'] = v.value()

        time_obj = {
            "Bias" : time_dict["Bias"],
            "TimeZoneKeyName" : time_dict["TimeZoneKeyName"],
            "ActiveTimeBias" : time_dict['ActiveTimeBias']
        }
        self.ret_list.append(time_obj)
        return self.ret_list

    def get_network_info(self):
        path = "ControlSet00%s\\services\\Tcpip\\Parameters\\Interfaces" % self.__control_set_check(self.reg)
        print(path)
        net_key = self.reg.open(path)
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
            self.ret_list.append(net_obj)
        return self.ret_list
    
    def __cal_hash(self):
        after_hash = calc_hash.get_hash(self.__path)
        self.__hash_val.append(after_hash)

    def get_hash(self):
        return self.__hash_val     
    
    
class SWAnalysis:
    def __init__(self, file, path, hash_val):
        self.reg = file
        self.ret_list = list()
        self.__hash_val = [hash_val]
        self.__path = path
        self.__cal_hash()
        
    def __control_set_check(self, file):
        key = file.open("Select")
        for v in key.values():
            if v.name() == "Current":
                return v.value()

    def __rec(self, key, get_path, find_val):
#        get_path(key, find_val)
        for subkey in key.subkeys():
            self.__rec(subkey, get_path, find_val)
        path = get_path(key,find_val)

    def __get_path(self, key, find_val):
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
        self.__rec(self.reg.root(), self.__get_path, keyword)

    def get_info(self):
        ret_list = []
        os_info = self.reg.open("Microsoft\\Windows NT\\CurrentVersion")
        os_dict = dict()
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

        os_obj = {
            "CurrentVersion" : os_dict['CurrentVersion'],
            "CurrentBuild" : os_dict['CurrentBuild'],
            "InstallDate" : os_dict['InstallDate'],
            "TimeZone" : "UTC",
            "RegisteredOwner" : os_dict['RegisteredOwner'],
            "EditionID" : os_dict['EditionID'],
            "ProductName" : os_dict['ProductName']
        }
        self.ret_list.append(os_obj)
            
        return self.ret_list

    def get_network_info(self):
        key = self.reg.open("Microsoft\\Windows NT\\CurrentVersion\\NetworkCards")
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

            net_obj = {
                "ServiceName" : network_info['ServiceName'],
                "Description" : network_info['Description']
            }
            self.ret_list.append(net_obj)
        return self.ret_list

    def __cal_hash(self):
        after_hash = calc_hash.get_hash(self.__path)
        self.__hash_val.append(after_hash)

    def get_hash(self):
        return self.__hash_val
    
    
class SAMAnalysis:
    def __init__(self, file, path, hash_val):
        self.reg = file
        self.ret_list = list()
        self.__hash_val = [hash_val]
        self.__path = path
        self.__cal_hash()
        
    def __rec(self, key, get_path, find_val):
#        get_path(key, find_val)
        for subkey in key.subkeys():
            self.__rec(subkey, get_path, find_val)
        path = get_path(key,find_val)

    def __get_path(self, key, find_val):
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
        self.__rec(self.reg.root(), self.__get_path, keyword)

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
        last_list = self.user_info()
        login_list = list()
        for i in range(len(last_list)):
            if last_list[i]['Last Login'] == "Never":
                pass
            else:
                login_list.append(last_list[i])
                
        sort_list = sorted(login_list, key=lambda e: (e['Last Login']))
        last = len(sort_list)
        self.ret_list.append(sort_list[last-1])
        return self.ret_list

    def user_name(self):
        user_path = "SAM\\Domains\\Account\\Users\\Names"
        user = self.reg.open(user_path)
        for items in user.subkeys():
            user_obj = {
                    'UserName' : items.name(), 
                    'Last Written Time' : items.timestamp().strftime("%Y-%m-%d %H:%M:%S"),
                    'TimeZone' : "UTC"
                }
            self.ret_list.append(user_obj)
        return self.ret_list

    def user_info(self): 
        user_path = "SAM\\Domains\\Account\\Users"
        user = self.reg.open(user_path)
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
        
    def __cal_hash(self):
        after_hash = calc_hash.get_hash(self.__path)
        self.__hash_val.append(after_hash)

    def get_hash(self):
        return self.__hash_val
