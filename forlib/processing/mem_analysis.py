import subprocess
import re, os
import forlib.calc_hash as calc_hash
from forlib.processing.convert_time import convert_replace_time as r_time
from datetime import datetime

class MemAnalysis:
    def __init__(self, file, hash_val):
        self.__file = file
        self.__vol_path = os.path.dirname(os.path.realpath(__file__)) + "\\volatility3\\vol.py"
        result_list = list()
        self.__hash_val = [hash_val]
        self.__cal_hash()
        
    def __regx(self, result):
        ret_list = list()
        progress_pattern = re.compile("[Progress].*Scanner\\n")

        for line in iter(result.stdout.readline, ""):
            if progress_pattern.findall(line) or line == '\n':
                pass
            else:
                ret_list.append(line)
        return ret_list

    def __processing(self, reg_list, keyList):
        ret_list = list()
        time_pattern = re.compile("Date")
        time_pattern2 = re.compile("Time")
        for i in range(2, len(reg_list)):
            tmp     = reg_list[i].replace('\n', '')
            tSplit  = tmp.split('\t')
            ret_obj = dict()

            for splitIndex, splitValue in enumerate(tSplit):
                # ret_obj[keyList[splitIndex]] = splitValue
                if time_pattern.findall(keyList[splitIndex]) or time_pattern2.findall(keyList[splitIndex]):
                    if splitValue == "N/A":
                        # print(splitValue)
                        ret_obj[keyList[splitIndex]] = splitValue
                    else:
                        replace_time = datetime.strptime(splitValue[:-1], "%Y-%m-%d %H:%M:%S.%f")
                        ret_obj["TimeZone"] = r_time(replace_time).strftime("%Z")
                        ret_obj[keyList[splitIndex]] = r_time(replace_time).strftime("%Y-%m-%d %H:%M:%S")
                else:
                    ret_obj[keyList[splitIndex]] = splitValue
            ret_list.append(ret_obj)
        return ret_list

    def get_cmdline(self):
        result_list = list()
        ret     = subprocess.Popen("python %s -f %s windows.cmdline" % (self.__vol_path, self.__file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList = ["PID", "Process", "Args"]
        # 실행 결과값을 가져와 특정 문장을 제외 후 결과만을 가져오기 위함
        reg_list = self.__regx(ret)
        # 가져온 실행 결과 값을 파싱
        result_list = self.__processing(reg_list, keyList)

        return result_list

    def get_procdump(self, mode, pid):
        result_list = list()
        if mode == 'all' and pid == 'all':
            ret      = subprocess.Popen("python %s -f %s windows.procdump" % (self.__vol_path, self.__file), shell=True, stdin=None,
                                   stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        elif mode == 'part':
            ret      = subprocess.Popen("python %s -f %s windows.procdump --pid %s" % (self.__vol_path, self.__file, pid), shell=True, stdin=None,
                                   stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        else:
            print("[Error] input mode error by procdump\nPlease check your value\n[mod] all file dump : get('all', 'all') , part file dump : get('part', '1143')")

        keyList  = ["PID", "Process", "Result"]

        reg_list = self.__regx(ret)
        result_list = self.__processing(reg_list, keyList)

        return result_list

    def get_dlldump(self):
        result_list = list()
        ret      = subprocess.Popen("python %s -f %s windows.dlldump" % (self.__vol_path, self.__file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["PID", "Process", "Result"]

        reg_list = self.__regx(ret)
        result_list = self.__processing(reg_list, keyList)

        return result_list

    def get_dlllist(self):
        result_list = list()
        ret      = subprocess.Popen("python %s -f %s windows.dlllist" % (self.__vol_path, self.__file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["PID", "Process", "Base", "Size", "Name", "Path"]

        reg_list = self.__regx(ret)
        result_list = self.__processing(reg_list, keyList)

        return result_list

    def get_driverirp(self):
        result_list = list()
        ret      = subprocess.Popen("python %s -f %s windows.driverirp" % (self.__vol_path, self.__file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["Offset", "Driver Name", "IRP", "Address", "Module", "Symbol"]

        reg_list = self.__regx(ret)
        result_list = self.__processing(reg_list, keyList)

        return result_list

    def get_driverscan(self):
        result_list = list()
        ret      = subprocess.Popen("python %s -f %s windows.driverscan" % (self.__vol_path, self.__file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["Offset", "Start", "Size", "Service Key", "Driver Name", "Name"]

        reg_list = self.__regx(ret)
        result_list = self.__processing(reg_list, keyList)

        return result_list

    def get_filescan(self):
        result_list = list()
        ret = subprocess.Popen("python %s -f %s windows.filescan" % (self.__vol_path, self.__file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["Offset", "Name"]

        reg_list = self.__regx(ret)
        result_list = self.__processing(reg_list, keyList)

        return result_list

    def get_handles(self):
        result_list = list()
        ret = subprocess.Popen("python %s -f %s windows.handles" % (self.__vol_path, self.__file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList = ["PID", "Process", "Offset", "HandleValue", "Type", "GrantendAccess", "Name"]

        reg_list = self.__regx(ret)
        result_list = self.__processing(reg_list, keyList)

        return result_list

    def get_info(self):
        result_list = list()
        print("python %s -f %s windows.info.Info" % (self.__vol_path, self.__file))
        ret      = subprocess.Popen("python %s -f %s windows.info" % (self.__vol_path, self.__file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")

        keyList  = ["Variable", "Value"]

        reg_list = self.__regx(ret)
        result_list = self.__processing(reg_list, keyList)

        return result_list

    def get_mutantscan(self):
        result_list = list()
        ret      = subprocess.Popen("python %s -f %s windows.mutantscan" % (self.__vol_path, self.__file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["Offset", "Name"]

        reg_list = self.__regx(ret)
        result_list = self.__processing(reg_list, keyList)

        return result_list

    def get_malfind(self):
        result_list = list()
        hexcode_pattern = re.compile("([0-9a-f]{2}( )?){8}")
        hexray_pattern  = re.compile("0x[0-9a-f]{0,16}:\t[a-z]{1,}.*\n")
        ret_list        = list()
        #3108\trundll32.exe\t0x70000\t0x70fff\tVadS\tPAGE_EXECUTE_READWRITE\t1\t1\t\n
        #1e ~ ~ ~ ~ ~ ~ ~ ...P..K.\n 0xffffff ~~~
        keyList  = ["PID", "Process", "Start", "End", "Tag", "Protection", "CommitCharge", "PrivateMemory", "HexDump", "Disasm"]
        ret      = subprocess.Popen("python %s -f %s windows.malfind" % (self.__vol_path, self.__file), shell=True,
                               stdin=None, stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        reg_list = self.__regx(ret)

        tmpList  = []
        tmpHex   = ""
        tmpDis   = ""

        for rl in reg_list:
            if hexcode_pattern.findall(rl) != []:
                tmpHex += rl
            elif hexray_pattern.findall(rl) != []:
                tmpDis += rl
            else:
                if tmpHex != "" and tmpDis != "":
                    tmpList.append(tmpHex)
                    tmpList.append(tmpDis)
                    tmpList.append(rl)
                    tmpHex = ""
                    tmpDis = ""
                else:
                    tmpList.append(rl)

        for tmpIndex, tmp in enumerate(tmpList[2:]):
            if tmpIndex % 3 == 0:
                tDict   = {}
                tmp     = tmp.replace('\n', '')
                tSplit  = tmp.split('\t')

                for splitIndex, split in enumerate(tSplit):
                    tDict[keyList[splitIndex]] = split

            elif tmpIndex % 3 == 1:
                tDict[keyList[-2]] = tmp

            elif tmpIndex % 3 == 2:
                tDict[keyList[-1]] = tmp
                result_list.append(tDict)
        '''
        for js in jsonList:
            print(js)
        '''
        return result_list

        # for i in range(1, len(reg_list)  ):
        #     print(reg_list[i])
        #     value = reg_list[i].split('\t')
        #     print(value)
        #     plist_obj = {
        #         "PID" : value[0],
        #         "Process" : value[1],
        #         "Start VPN" : value[2],
        #         "End VPN" : value[3],
        #         "Tag" : value[4],
        #         "Protection" : value[5],
        #         "CommitCharge" : value[6],
        #         "PrivateMemory" : value[7],
        #         "HexDump" : value[8],
        #         "Disasm" : value[9:]
        #     }
        #     ret_list.append(plist_obj)
        # return ret_list

    def get_pslist(self):
        result_list = list()
        ret      = subprocess.Popen("python %s -f %s windows.pslist" % (self.__vol_path, self.__file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["PID", "PPID", "ImageFileName", "Offset(V)", "Threads", "Handles", "SessionId", "Wow64", "CreateTime", "ExitTime"]

        reg_list = self.__regx(ret)
        result_list = self.__processing(reg_list, keyList)

        return result_list

    def get_psscan(self):
        result_list = list()
        ret      = subprocess.Popen("python %s -f %s windows.psscan" % (self.__vol_path, self.__file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["PID", "PPID", "ImageFileName", "Offset(V)", "Threads", "Handles", "SessionId", "Wow64", "CreateTime", "ExitTime"]

        reg_list = self.__regx(ret)
        result_list = self.__processing(reg_list, keyList)

        return result_list

    def get_pstree(self):
        result_list = list()
        ret      = subprocess.Popen("python %s -f %s windows.pstree" % (self.__vol_path, self.__file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["PID", "PPID", "ImageFileName", "Offset(V)", "Threads", "Handles", "SessionId", "Wow64", "CreateTime", "ExitTime"]

        reg_list = self.__regx(ret)
        result_list = self.__processing(reg_list, keyList)

        return result_list

    def get_reg_certificates(self):
        result_list = list()
        ret      = subprocess.Popen("python %s -f %s windows.registry.certificates" % (self.__vol_path, self.__file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")

        keyList  = ["Certificate Path", "Certificate Section", "Certificate ID", "Certificate Name"]
        reg_list = self.__regx(ret)
        result_list = self.__processing(reg_list, keyList)

        return result_list

    def get_reg_hivelist(self):
        result_list = list()
        ret      = subprocess.Popen("python %s -f %s windows.registry.hivelist" % (self.__vol_path, self.__file),
                               shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["Offset", "FileFullPath"]

        reg_list = self.__regx(ret)
        result_list = self.__processing(reg_list, keyList)

        return result_list

    def get_reg_hivescan(self):
        result_list = list()
        ret      = subprocess.Popen("python %s -f %s windows.registry.hivescan" % (self.__vol_path, self.__file),
                               shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["Offset"]
        reg_list = self.__regx(ret)
        result_list = self.__processing(reg_list, keyList)

        return result_list

    def get_reg_printkey(self):
        result_list = list()
        ret      = subprocess.Popen("python %s -f %s windows.registry.printkey" % (self.__vol_path, self.__file),
                               shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["Last Write Time", "Hive Offset", "Type", "Key", "Name", "Data", "Volatile"]

        reg_list = self.__regx(ret)
        result_list = self.__processing(reg_list, keyList)

        return result_list

    def get_reg_userassist(self):
        result_list = list()
        ret = subprocess.Popen("python %s -f %s windows.registry.userassist" % (self.__vol_path, self.__file),
                               shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")

        for line in iter(ret.stdout.readline, ""):
            print(line.rstrip())

    def get_vadinfo(self):
        result_list = list()
        ret      = subprocess.Popen("python %s -f %s windows.vadinfo" % (self.__vol_path, self.__file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["PID", "Process", "Offset", "Start VPN", "End VPN", "Tag", "Protection", "CommitCharge", "PrivateMemory", "Parent", "File"]

        reg_list = self.__regx(ret)
        result_list = self.__processing(reg_list, keyList)

        return result_list

    def get_vaddump(self, mode, addr, pid):
        result_list = list()
        if mode == 'all' and addr == 'all' and pid == 'all':
            ret      = subprocess.Popen("python %s -f %s windows.vadinfo" % (self.__vol_path, self.__file), shell=True, stdin=None,
                                   stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        elif mode == 'part' and addr == 'all':
            ret      = subprocess.Popen("python %s -f %s windows.vaddump --pid %s" % (self.__vol_path, self.__file, pid), shell=True, stdin=None,
                                   stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        elif mode == 'part':
            ret      = subprocess.Popen("python %s -f %s windows.vaddump --address %s --pid %s" % (self.__vol_path, self.__file, addr, pid), shell=True, stdin=None,
                                   stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        else:
            print("[Error] input mode error by procdump\nPlease check your value\n[mod] all file dump : get('all', 'all', 'all') , part file dump (pid) : get('part', 'all', '1143'), part file dump(pid, addr) : get('part', '0xabcd', '114")

        keyList  = ["PID", "Process", "Result"]

        reg_list = self.__regx(ret)
        result_list = self.__processing(reg_list, keyList)

        return result_list

    def get_timeliner(self):
        result_list = list()
        ret      = subprocess.Popen("python %s -f %s timeliner.Timeliner" % (self.__vol_path, self.__file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["Plugin", "Description", "Created Date", "Modified Date", "Accessed Date", "Changed Date"]

        reg_list = self.__regx(ret)
        result_list = self.__processing(reg_list, keyList)

        return result_list
    
    def __cal_hash(self):
        after_hash = calc_hash.get_hash(self.__file, 'after')
        self.__hash_val.append(after_hash)

    def get_hash(self):
        return self.__hash_val    
