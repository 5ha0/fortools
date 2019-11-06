import subprocess
import re

class MemAnalysis:
    def __init__(self, file):
        self.file = file
        self.vol_path = ""

    def __regx(self, result):
        ret_list = list()
        progress_pattern = '[Progress].*Scanner\\n'
        progress_regex = re.compile(progress_pattern)
        plist_list = list()

        for line in iter(result.stdout.readline, ""):
            if progress_regex.findall(line) or line == '\n':
                pass
            else:
                ret_list.append(line)
        return ret_list

    def __process(self, reg_list):
        plist_list = list()
        for i in range(1, len(reg_list)):
            value = reg_list[i].split('\t')
            plist_obj = {
                "PID": value[0],
                "PPID": value[1],
                "ImageFileName": value[2],
                "Offset(V)": value[3],
                "Threads": value[4],
                "Handles": value[5],
                "SessionId": value[6],
                "Wow64": value[7],
                "CreateTime": value[8],
                "ExitTime": value[9][:-1]
            }
            plist_list.append(plist_obj)

        return plist_list

    def cmdline(self):
        ret_list = list()

        ret = subprocess.run("python3 %s -f %s windows.cmdline" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1)
        # 실행 결과값을 가져와 특정 문장을 제외 후 결과만을 가져오기 위함
        reg_list = self.__regx(ret)

        # 가져온 결과를 파싱
        for i in range(1, len(reg_list)):
            value = reg_list[i].split('\t')
            plist_obj = {
                "PID" : value[0],
                "Process" : value[1],
                "Args" : value[2][:-1]
            }
            ret_list.append(plist_obj)
        return ret_list

    def dlldump(self):
        ret_list = list()

        ret = subprocess.run("python3 %s -f %s windows.dlldump" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1)
        # 실행 결과값을 가져와 특정 문장을 제외 후 결과만을 가져오기 위함
        reg_list = self.__regx(ret)

        # 가져온 결과를 파싱
        for i in range(1, len(reg_list)):
            value = reg_list[i].split('\t')
            plist_obj = {
                "PID" : value[0],
                "Process" : value[1],
                "Result" : value[2][:-1]
            }
            ret_list.append(plist_obj)
        return ret_list
    
    def dlllist(self):
        ret_list = list()

        ret = subprocess.run("python3 %s -f %s windows.dlllist" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1)
        # 실행 결과값을 가져와 특정 문장을 제외 후 결과만을 가져오기 위함
        reg_list = self.__regx(ret)

        # 가져온 결과를 파싱
        for i in range(1, len(reg_list)):
            value = reg_list[i].split('\t')
            plist_obj = {
                "PID" : value[0],
                "Process" : value[1],
                "Base" : value[2][:-1],
                "Size": value[3],
                "Name": value[4],
                "Path": value[5][:-1]
            }
            ret_list.append(plist_obj)
        return ret_list
    
    def pslist(self):
        ret = subprocess.Popen("python3 %s -f %s windows.pslist" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1)
        reg_list = self.__regx(ret)
        ret_list = self.__process(reg_list)
        return ret_list

    def psscan(self):
        ret = subprocess.Popen("python3 %s -f %s windows.psscan" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1)
        reg_list = self.__regx(ret)
        ret_list = self.__process(reg_list)
        return ret_list

    def pstree(self):
        ret = subprocess.Popen("python3 %s -f %s windows.pstree" % (self.vol_path, self.file), shell=True, stdin=None,
                               stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1)
        reg_list = self.__regx(ret)
        ret_list = self.__process(reg_list)
        return ret_list
