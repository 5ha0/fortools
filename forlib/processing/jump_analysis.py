from forlib.processing.lnk_analysis import convert_time
import struct


class JumplistAnalysis:
    json_list = []

    def __init__(self, file):
        self.file = file
        self.streams = file.listdir(streams=True, storages=False)
        self.__stream()

    def __stream(self):
        for i in range(0, len(self.streams)):
            data = self.file.openstream(self.streams[i])
            file_data = data.read()
            header_value = file_data[:4]
            try:
                if header_value[0] == 76:
                    data_list = dict()
                    c_time = struct.unpack("<q", file_data[28:36])
                    data_list["create time"] = str(convert_time(c_time[0]))
                    a_time = struct.unpack("<q", file_data[36:44])
                    data_list["access time"] = str(convert_time(a_time[0]))
                    w_time = struct.unpack("<q", file_data[44:52])
                    data_list["write time"] = str(convert_time(w_time[0]))
                    data_list["file size"] = struct.unpack("<l", file_data[52:56])[0]
                    try:
                        data_list["path"] = self.__path_info(file_data)
                    except:
                        data_list["path"] = 'none'
                    self.json_list.append(data_list)
                else:
                    self.destlist = file_data
            except:
                pass

    def __path_info(self, file_data):
        lnk_id_list_size = struct.unpack('<h', file_data[76:78])
        lnk_info_size = struct.unpack('<l', file_data[78+lnk_id_list_size[0]:82 + lnk_id_list_size[0]])
        path_offset = struct.unpack('<l', file_data[94+lnk_id_list_size[0]:94+lnk_id_list_size[0]+4])
        size = lnk_info_size[0] - path_offset[0]
        local = file_data[78+lnk_id_list_size[0]+path_offset[0]:78+lnk_id_list_size[0]+path_offset[0] + size]
        return local.decode('ascii')[:-2]

    def access_count(self):
        cnt = struct.unpack("<l", self.destlist[148:152])
        return cnt[0]

    def recent_time(self):
        time = struct.unpack("<q", self.destlist[132:140])
        return str(convert_time(time[0]))

    def show_info(self):
        for i in self.json_list:
            print(i)
