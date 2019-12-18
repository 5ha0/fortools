import pyesedb
import binascii
from datetime import *
import forlib.calc_hash as calc_hash

class WinSearchAnalysis:

    def __init__(self, file, path, hash_v):
        self._result = []
        self.__file = file
        self.__json = self.__parse()
        self.__hash_value = [hash_v]
        self.__path = path
        self.__cal_hash()

    def __parse(self):
        result = []
        edb_data_table = self.__file.get_table_by_name("SystemIndex_0A")
        no = 0
        for row in edb_data_table.records:
            no += 1
            mkdict = dict()
            mkdict["index"] = no
            mkdict["type"] = "window search.edb"
            mkdict["DocID"] = row.get_value_data_as_integer(0)
            mkdict["FileName"] = row.get_value_data_as_string(31).split('\\')[-1]
            if row.get_value_data(5) is None:
                mkdict["System_DateModified"] = ""
            else:
                mkdict["System_DateModified"] = int2date(int(bytes.decode(binascii.hexlify(row.get_value_data(5))), 16))

            if row.get_value_data(6) is None:
                mkdict["System_DateCreated"] = ""
            else:
                mkdict["System_DateCreated"] = int2date(int(bytes.decode(binascii.hexlify(row.get_value_data(6))), 16))

            if row.get_value_data(7) is None:
                mkdict["System_DateAccessed"] = ""
            else:
                mkdict["System_DateAccessed"] = int2date(int(bytes.decode(binascii.hexlify(row.get_value_data(7))), 16))

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
                data1 = row.get_value_data(193)
                data = bytes.decode(binascii.hexlify(row.get_value_data(193)))

            #     mkdict["System_Search_AutoSummary"]=bytes.fromhex(data).decode("utf-16")
            mkdict["System_ItemTypeText"] = row.get_value_data_as_string(253)
            mkdict["System_FileExtension"] = row.get_value_data_as_string(262)
            mkdict["System_ItemPathDisplayNarrow"] = row.get_value_data_as_string(284)
            mkdict["System_FileName"] = row.get_value_data_as_string(363)

            result.append(mkdict)
        return result

    def show_all_info(self):
        for i in self.__json:
            print(i)

    def get_all_info(self):
        return self.__json

    def __cal_hash(self):
        self.__hash_value.append(calc_hash.get_hash(self.__path, 'after'))

    def get_hash(self):
        return self.__hash_value


def int2date(date_time):
    # 1601년 1월 1일부터
    from_date = datetime(1601, 1, 1)
    passing_time = timedelta(microseconds=(date_time * 0.1))
    get_date = from_date + passing_time
    return get_date.strftime("%Y-%m-%d %H:%M:%S")