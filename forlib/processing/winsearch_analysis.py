import pyesedb
import binascii
from datetime import *
import forlib.calc_hash as calc_hash
import forlib.processing.convert_time as convert_time

class WinSearchAnalysis:

    def __init__(self, file, path, hash_v):
        self.winsearch_list = []
        self.__file = file
        if self.__file==-1:
            self.__winsearch_list==""
        else:
            self.__parse()
        self.__hash_value = [hash_v]
        self.__path = path
        self.__cal_hash()

    def __parse(self):
        edb_data_table = self.__file.get_table_by_name("SystemIndex_0A")
        no = 0
        for row in edb_data_table.records:
            no += 1
            mkdict = dict()
            mkdict["index"] = no
            mkdict["type"] = "window search.edb"
            mkdict["timezone"]=convert_time.convert_time(0).strftime("%Z")
            mkdict["DocID"] = row.get_value_data_as_integer(0)
            mkdict["FileName"] = row.get_value_data_as_string(31).split('\\')[-1]
            if row.get_value_data(5) is None:
                mkdict["System_DateModified"] = convert_time.convert_time(0).strftime("%Y-%m-%d %H:%M:%S")
            else:
                mkdict["System_DateModified"] = convert_time.convert_time(int(bytes.decode(binascii.hexlify(row.get_value_data(5))), 16)).strftime("%Y-%m-%d %H:%M:%S")

            if row.get_value_data(6) is None:
                mkdict["System_DateCreated"] = convert_time.convert_time(0).strftime("%Y-%m-%d %H:%M:%S")
            else:
                mkdict["System_DateCreated"] = convert_time.convert_time(int(bytes.decode(binascii.hexlify(row.get_value_data(6))), 16)).strftime("%Y-%m-%d %H:%M:%S")

            if row.get_value_data(7) is None:
                mkdict["System_DateAccessed"] = convert_time.convert_time(0).strftime("%Y-%m-%d %H:%M:%S")
            else:
                mkdict["System_DateAccessed"] = convert_time.convert_time(int(bytes.decode(binascii.hexlify(row.get_value_data(7))), 16)).strftime("%Y-%m-%d %H:%M:%S")

            mkdict["System_IsFolder"] = int(bytes.decode(binascii.hexlify(row.get_value_data(19))), 16)

            if mkdict["System_IsFolder"] == 1 or row.get_value_data(3) is None:
                mkdict["System_Size"] = ""
            else:
                mkdict["System_Size"] = int(bytes.decode(binascii.hexlify(row.get_value_data(3))), 16)

            mkdict["System_MIMEType"] = row.get_value_data_as_string(21)
            mkdict["System_ItemPathDisplay"] = row.get_value_data_as_string(31)
            if row.get_value_data(193) is None:
                mkdict["System_Search_AutoSummary"] = ""
            else:
                mkdict["System_Search_AutoSummary"] = ""
                # data1 = row.get_value_data(193)
                # data = bytes.decode(binascii.hexlify(row.get_value_data(193)))

            #     mkdict["System_Search_AutoSummary"]=bytes.fromhex(data).decode("utf-16")
            mkdict["System_ItemTypeText"] = row.get_value_data_as_string(253)
            mkdict["System_FileExtension"] = row.get_value_data_as_string(262)
            mkdict["System_ItemPathDisplayNarrow"] = row.get_value_data_as_string(284)
            mkdict["System_FileName"] = row.get_value_data_as_string(363)

            self.winsearch_list.append(mkdict)

    def show_all_info(self):
        for i in self.winsearch_list:
            print(i)

    def get_all_info(self):
        return self.winsearch_list

    def __cal_hash(self):
        self.__hash_value.append(calc_hash.get_hash(self.__path, 'after'))

    def get_hash(self):
        return self.__hash_value
