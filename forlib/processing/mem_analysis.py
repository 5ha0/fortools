import subprocess
import re

class MemAnalysis:
    def __init__(self, file):
        self.file = file
        self.vol_path = ""
        self.ret_list = list()
        
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
        for i in range(1, len(reg_list)):
            tmp     = reg_list[i].replace('\n', '')
            tSplit  = tmp.split('\t')
            ret_obj = dict()

            for splitIndex, splitValue in enumerate(tSplit):
                ret_obj[keyList[splitIndex]] = splitValue

            ret_list.append(ret_obj)
        return ret_list

    def cmdline(self):
        ret     = subprocess.Popen("python3 %s -f %s windows.cmdline" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList = ["PID", "Process", "Args"]
        # 실행 결과값을 가져와 특정 문장을 제외 후 결과만을 가져오기 위함
        reg_list = self.__regx(ret)
        # 가져온 실행 결과 값을 파싱
        self.ret_list = self.__processing(reg_list, keyList)

        return self.ret_list

    def dlldump(self):
        ret      = subprocess.Popen("python3 %s -f %s windows.dlldump" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["PID", "Process", "Result"]

        reg_list = self.__regx(ret)
        self.ret_list = self.__processing(reg_list, keyList)

        return self.ret_list

    def dlllist(self):
        ret      = subprocess.Popen("python3 %s -f %s windows.dlllist" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["PID", "Process", "Base", "Size", "Name", "Path"]

        reg_list = self.__regx(ret)
        self.ret_list = self.__processing(reg_list, keyList)

        return self.ret_list

    def driverirp(self):
        ret      = subprocess.Popen("python3 %s -f %s windows.driverirp" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["Offset", "Driver Name", "IRP", "Address", "Module", "Symbol"]

        reg_list = self.__regx(ret)
        self.ret_list = self.__processing(reg_list, keyList)

        return self.ret_list

    def driverscan(self):
        ret      = subprocess.Popen("python3 %s -f %s windows.driverscan" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["Offset", "Start", "Size", "Service Key", "Driver Name", "Name"]

        reg_list = self.__regx(ret)
        self.ret_list = self.__processing(reg_list, keyList)

        return self.ret_list

    def filescan(self):
        ret = subprocess.Popen("python3 %s -f %s windows.filescan" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["Offset", "Name"]

        reg_list = self.__regx(ret)
        self.ret_list = self.__processing(reg_list, keyList)

        return self.ret_list

    def handles(self):
        ret_list = list()

        ret = subprocess.Popen("python3 %s -f %s windows.handles" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList = ["PID", "Process", "Offset", "HandleValue", "Type", "GrantendAccess", "Name"]

        reg_list = self.__regx(ret)
        self.ret_list = self.__processing(reg_list, keyList)

        return self.ret_list

    def info(self):
        ret      = subprocess.Popen("python3 %s -f %s windows.info" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")

        keyList  = ["Variable", "Value"]

        reg_list = self.__regx(ret)
        self.ret_list = self.__processing(reg_list, keyList)

        return self.ret_list

    def mutantscan(self):
        ret      = subprocess.Popen("python3 %s -f %s windows.mutantscan" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["Offset", "Name"]

        reg_list = self.__regx(ret)
        self.ret_list = self.__processing(reg_list, keyList)

        return self.ret_list

    def malfind(self):
        hexcode_pattern = re.compile("([0-9a-f]{2}( )?){8}")
        hexray_pattern  = re.compile("0x[0-9a-f]{0,16}:\t[a-z]{1,}.*\n")
        ret_list        = list()
        #3108\trundll32.exe\t0x70000\t0x70fff\tVadS\tPAGE_EXECUTE_READWRITE\t1\t1\t\n
        #1e ~ ~ ~ ~ ~ ~ ~ ...P..K.\n 0xffffff ~~~
        keyList  = ["PID", "Process", "Start", "End", "Tag", "Protection", "CommitCharge", "PrivateMemory", "HexDump", "Disasm"]
        ret      = subprocess.Popen("python %s -f %s windows.malfind" % (self.vol_path, self.file), shell=True,
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
                self.ret_list.append(tDict)
        '''
        for js in jsonList:
            print(js)
        '''
        return self.ret_list

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

    def pslist(self):
        ret      = subprocess.Popen("python3 %s -f %s windows.pslist" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["PID", "PPID", "ImageFileName", "Offset(V)", "Threads", "Handles", "SessionId", "Wow64", "CreateTime", "ExitTime"]

        reg_list = self.__regx(ret)
        self.ret_list = self.__processing(reg_list, keyList)

        return self.ret_list

    def psscan(self):
        ret      = subprocess.Popen("python3 %s -f %s windows.psscan" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["PID", "PPID", "ImageFileName", "Offset(V)", "Threads", "Handles", "SessionId", "Wow64", "CreateTime", "ExitTime"]

        reg_list = self.__regx(ret)
        self.ret_list = self.__processing(reg_list, keyList)

        return self.ret_list

    def pstree(self):
        ret      = subprocess.Popen("python3 %s -f %s windows.pstree" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["PID", "PPID", "ImageFileName", "Offset(V)", "Threads", "Handles", "SessionId", "Wow64", "CreateTime", "ExitTime"]

        reg_list = self.__regx(ret)
        self.ret_list = self.__processing(reg_list, keyList)

        return self.ret_list

    def reg_certificates(self):
        ret      = subprocess.Popen("python3 %s -f %s windows.registry.certificates" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")

        keyList  = ["Certificate Path", "Certificate Section", "Certificate ID", "Certificate Name"]
        reg_list = self.__regx(ret)
        self.ret_list = self.__processing(reg_list, keyList)

        return self.ret_list

    def reg_hivelist(self):
        ret      = subprocess.Popen("python3 %s -f %s windows.registry.hivelist" % (self.vol_path, self.file),
                               shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["Offset", "FileFullPath"]

        reg_list = self.__regx(ret)
        self.ret_list = self.__processing(reg_list, keyList)

        return self.ret_list

    def reg_hivescan(self):
        ret      = subprocess.Popen("python3 %s -f %s windows.registry.hivescan" % (self.vol_path, self.file),
                               shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["Offset"]
        reg_list = self.__regx(ret)
        self.ret_list = self.__processing(reg_list, keyList)

        return self.ret_list

    def reg_printkey(self):
        ret      = subprocess.Popen("python3 %s -f %s windows.registry.printkey" % (self.vol_path, self.file),
                               shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["Last Write Time", "Hive Offset", "Type", "Key", "Name", "Data", "Volatile"]

        reg_list = self.__regx(ret)
        self.ret_list = self.__processing(reg_list, keyList)

        return self.ret_list

    def reg_userassist(self):
        ret = subprocess.Popen("python3 %s -f %s windows.registry.userassist" % (self.vol_path, self.file),
                               shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")

        for line in iter(ret.stdout.readline, ""):
            print(line.rstrip())

    def vadinfo(self):
        ret      = subprocess.Popen("python3 %s -f %s windows.vadinfo" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["PID", "Process", "Offset", "Start VPN", "End VPN", "Tag", "Protection", "CommitCharge", "PrivateMemory", "Parent", "File"]

        reg_list = self.__regx(ret)
        self.ret_list = self.__processing(reg_list, keyList)

        return self.ret_list

    def timeliner(self):
        ret      = subprocess.Popen("python3 %s -f %s timeliner.Timeliner" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, encoding="utf-8")
        keyList  = ["Plugin", "Description", "Created Date", "Modified Date", "Accessed Date", "Changed Date"]

        reg_list = self.__regx(ret)
        self.ret_list = self.__processing(reg_list, keyList)

        return self.ret_list
