from forlib.processing.convert_time import convert_time
import struct
import forlib.calc_hash as calc_hash


class JumplistAnalysis:
    def __init__(self, file, path, hash_v):
        self.__file = file
        self.__streams = file.listdir(streams=True, storages=False)
        self.__json_list = []
        self.__stream()
        self.__hash_value = [hash_v]
        self.__path = path
        self.__cal_hash()

    def __stream(self):
        for i in range(0, len(self.__streams)):
            data = self.__file.openstream(self.__streams[i])
            file_data = data.read()
            header_value = file_data[:4]
            try:
                if header_value[0] == 76:
                    data_list = dict()
                    c_time = struct.unpack("<Q", file_data[28:36])
                    data_list["create time"] = str(convert_time(c_time[0]))
                    a_time = struct.unpack("<Q", file_data[36:44])
                    data_list["access time"] = str(convert_time(a_time[0]))
                    w_time = struct.unpack("<Q", file_data[44:52])
                    data_list["write time"] = str(convert_time(w_time[0]))
                    file_size = struct.unpack("<L", file_data[52:56])[0]
                    data_list["file size"] = self.__file.get_size(self.__streams[i])
                    data_list["target file size"] = file_size
                    try:
                        return_path = self.__path_info(file_data)
                        data_list["path"] = return_path.decode('ascii').replace('\x00', '')
                    except Exception as e:
                        data_list["path"] = 'cannot decode'
                    self.__json_list.append(data_list)
                else:
                    self.__destlist = file_data
            except:
                pass

    def __path_info(self, file_data):
        lnk_id_list_size = struct.unpack('<H', file_data[76:78])
        lnk_info_size = struct.unpack('<L', file_data[78+lnk_id_list_size[0]:82 + lnk_id_list_size[0]])
        # lnk_volume_id_offset = struct.unpack("<l", file_data[90+lnk_id_list_size[0]:90+lnk_id_list_size[0]+4])
        lnk_info_flag = struct.unpack("<L", file_data[86 + lnk_id_list_size[0]:86 + lnk_id_list_size[0] + 4])
        path_offset = struct.unpack('<L', file_data[94 + lnk_id_list_size[0]:94 + lnk_id_list_size[0] + 4])
        if lnk_info_flag[0] == 1:
            size = lnk_info_size[0] - path_offset[0]
            local = file_data[78+lnk_id_list_size[0]+path_offset[0]:78+lnk_id_list_size[0]+path_offset[0] + size]
        elif lnk_info_flag[0] == 3:
            net_offset = struct.unpack("<L", file_data[98+lnk_id_list_size[0]:102+lnk_id_list_size[0]])
            size = net_offset[0] - path_offset[0]
            local = file_data[78 + lnk_id_list_size[0] + path_offset[0]:78 + lnk_id_list_size[0] + path_offset[0] + size]
        return local

    def __cal_hash(self):
        self.__hash_value.append(calc_hash.get_hash(self.__path))

    def get_hash(self):
        return self.__hash_value

    def access_count(self):
        cnt = struct.unpack("<L", self.__destlist[148:152])
        return cnt[0]

    def recent_time(self):
        time = struct.unpack("<Q", self.__destlist[132:140])
        return str(convert_time(time[0]))

    def netbios(self):
        netbios = self.__destlist[104:120]
        return netbios.decode('ascii')

    def show_info(self):
        for i in self.__json_list:
            print(i)

    def get_info(self):
        return self.__json_list
