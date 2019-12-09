from forlib.processing.convert_time import convert_time
import struct
import time
import os
import forlib.calc_hash as calc_hash
# from forlib.processing.jump_analysis import decode_str as de
from bitstring import BitArray


class MFTAnalysis:
    def __init__(self, file, path, hash_v):
        self.path = path
        self.file = file
        self.__mft_size = int(os.path.getsize(path))//1024
        self.__hash_value = [hash_v]
        self.__result = self.__parse_info()
        self.__cal_hash()

    def get_info(self):
        return self.__result


    def get_hash(self):
        return self.__hash_value

    def __cal_hash(self):
        self.__hash_value.append(calc_hash.get_hash(self.path))

    def __parse_info(self):
        result = []
        for size in range(0, self.__mft_size):
            self.file.seek(1024*size)
            info_list = dict()
            self.file.read(8)
            info_list["LSN"] = struct.unpack("<Q", self.file.read(8))[0]
            self.file.read(4)
            offset_first = struct.unpack("<H", self.file.read(2))[0]
            flags = self.file.read(2)
            used_size = struct.unpack("<H", self.file.read(2))[0]
            if used_size ==64:
                continue
            allocated_size = struct.unpack("<I", self.file.read(4))[0]
            file_refernce = unpack48(self.file.read(8))
            sequence_value = file_refernce[0]
            mft_entry_number = file_refernce[1]
            next_attr_id = struct.unpack("<H", self.file.read(2))[0]
            next_id = self.file.read(2)
            self.file.seek(1024*size+offset_first)
            self.file.read(8)
            resident_flag = self.file.read(1)
            resident_flag = struct.unpack("<B", resident_flag)[0]
            self.file.seek(3, 1)
            # name_length = struct.unpack("<B", self.file.read(1))[0]
            # offset_name = struct.unpack("<H", self.file.read(2))[0]
            self.file.read(4)
            if resident_flag is 0:  # resident
                self.file.read(8)
            else:  # non-resident
                self.file.read(48)
            # $STANDARD_INFORMATION
            info_list["TimeZone"] = "UTC +00:00"
            c_time = struct.unpack("<Q", self.file.read(8))
            if c_time[0] == 0:
                continue
            try:
                info_list["SIN Creation Time"] = convert_time(c_time[0]).strftime("%Y-%m-%d %H:%M:%S")
            except OverflowError:
                continue
            m_time = struct.unpack("<Q", self.file.read(8))
            try:
                info_list["SIN Modified Time"] = convert_time(m_time[0]).strftime("%Y-%m-%d %H:%M:%S")
            except OverflowError:
                continue
            mft_modified_time = struct.unpack("<Q", self.file.read(8))
            try:
                info_list["SIN MFT Modified Time"] = convert_time(mft_modified_time[0]).strftime("%Y-%m-%d %H:%M:%S")
            except OverflowError:
                continue
            a_time = struct.unpack("<Q", self.file.read(8))
            try:
                info_list["SIN Last Accessed Time"] = convert_time(a_time[0]).strftime("%Y-%m-%d %H:%M:%S")
            except OverflowError:
                continue
            self.file.read(40)
            file_name_off = self.file.tell()
            # $FILE_NAME
            if struct.unpack("<I", self.file.read(4))[0] == 48:
                attr_len = struct.unpack("<I", self.file.read(4))[0]
                self.file.read(1)
                #resident_flag = struct.unpack("<B", self.file.read(1))[0]
                name_length = struct.unpack("<B", self.file.read(1))[0]
                offset_name = struct.unpack("<H", self.file.read(2))[0]
                self.file.read(12)
                file_refernce = BitArray(self.file.read(8)).unpack('uintle:48, <H')
                parent_sequence_value = file_refernce[1]
                parent_mft_entry_number = file_refernce[0]
                c_time = struct.unpack("<Q", self.file.read(8))
                try:
                    info_list["FIN Creation Time"] = convert_time(c_time[0]).strftime("%Y-%m-%d %H:%M:%S")
                except OverflowError:
                    info_list["FIN Creation Time"] = 'none'
                m_time = struct.unpack("<Q", self.file.read(8))
                try:
                    info_list["FIN Modified Time"] = convert_time(m_time[0]).strftime("%Y-%m-%d %H:%M:%S")
                except OverflowError:
                    info_list["FIN Modified Time"] = 'none'
                mft_modified_time = struct.unpack("<Q", self.file.read(8))
                try:
                    info_list["FIN MFT Modified Time"] = convert_time(mft_modified_time[0]).strftime("%Y-%m-%d %H:%M:%S")
                except OverflowError:
                    info_list["FIN MFT Modified Time"] = 'none'
                a_time = struct.unpack("<q", self.file.read(8))
                try:
                    info_list["FIN Last Accessed Time"] = convert_time(a_time[0]).strftime("%Y-%m-%d %H:%M:%S")
                except OverflowError:
                    info_list["FIN Last Accessed Time"] = 'none'
                self.file.read(8)  # file allocation size
                info_list["File Size"] = struct.unpack("<Q", self.file.read(8))[0]
                # info_list["MFT Entry Num"] = mft_entry_number
                # info_list["Parent MFT Entry Num"] = parent_mft_entry_number
                self.file.read(8)
                name_length = struct.unpack("<B", self.file.read(1))[0]
                name_type = struct.unpack("<B", self.file.read(1))[0]
                if name_type == 2:
                    try:
                        self.file.read(name_length * 2).decode('utf-16')
                        self.file.read(attr_len-(self.file.tell()-file_name_off))
                        self.file.read(88)
                        name_length = struct.unpack("<B", self.file.read(1))[0]
                        self.file.read(1)
                        info_list["Name"] = self.file.read(name_length * 2).decode('utf-16')
                    except UnicodeDecodeError:
                        info_list["Name"] = "Unable To Decode Filename"
                else:
                    try:
                        info_list["Name"] = self.file.read(name_length*2).decode('utf-16')
                    except UnicodeDecodeError:
                        info_list["Name"] = "Unable To Decode Filename"
                path_list = []
                while True:
                    parent_result = self.__find_parent(parent_mft_entry_number)
                    parent_mft_entry_number = parent_result[1]
                    parent_name = parent_result[0]
                    if parent_name == 'None' or parent_name == '.':
                        break
                    else:
                        path_list.append(parent_name)
                path = '.'
                for p in reversed(path_list):
                    path = path+'\\'+str(p)
                info_list["parent"] = path
            else:
                info_list["FIN Creation Time"] = ''
                info_list["FIN Modified Time"] = ''
                info_list["FIN MFT Modified Time"] = ''
                info_list["FIN Last Accessed Time"] = ''
                info_list["File Size"] = ''
                info_list["Name"] = ''
                info_list["parent"] = ''
            result.append(info_list)
        return result

    def __find_parent(self, parent_mft_entry_number):
        try:
            self.file.seek(parent_mft_entry_number * 1024)
            self.file.read(20)
            offset_first = struct.unpack("<H", self.file.read(2))[0]
            self.file.seek(parent_mft_entry_number * 1024 + offset_first)
            self.file.read(8)
            resident_flag = self.file.read(1)
            resident_flag = struct.unpack("<B", resident_flag)[0]
            self.file.seek(3, 1)
            self.file.read(4)
            if resident_flag == 0:  # resident
                self.file.read(8)
            else:  # non-resident
                self.file.read(48)
            self.file.read(72)
            file_name_off = self.file.tell()
            if struct.unpack("<I", self.file.read(4))[0] == 48:
                attr_len = struct.unpack("<I", self.file.read(4))[0]
                self.file.read(1)
                name_length = struct.unpack("<B", self.file.read(1))[0]
                offset_name = struct.unpack("<H", self.file.read(2))[0]
                self.file.read(12)
                file_refernce = BitArray(self.file.read(8)).unpack('uintle:48, <H')
                parent_sequence_value = file_refernce[1]
                parent_mft_entry_number = file_refernce[0]
                self.file.read(56)
                name_length = struct.unpack("<B", self.file.read(1))[0]
                name_type = struct.unpack("<B", self.file.read(1))[0]
                if name_type == 2:
                    self.file.read(name_length * 2).decode('utf-16')
                    self.file.read(attr_len - (self.file.tell() - file_name_off))
                    self.file.read(88)
                    name_length = struct.unpack("<B", self.file.read(1))[0]
                    name_type = struct.unpack("<B", self.file.read(1))[0]
                    name = self.file.read(name_length * 2).decode('utf-16').replace('\x00\x00\x90', '')
                else:
                    try:
                        name = self.file.read(name_length*2).decode('utf-16')
                    except UnicodeDecodeError:
                        name = "Unable To Decode Filename"
                return [name, parent_mft_entry_number]
            else:
                return ['None', None]
        except:
            return ['None', None]


class UsnJrnl:
    def __init__(self, file, path, hash_v):
        self.__path = path
        self.__file = file
        self.__hash_value = [hash_v]
        self.__result = self.__parse()
        self.__cal_hash()

    def get_info(self):
        return self.__result

    def event_filter(self, name):
        return filesys_filter(['Event Info', name], self.__result)

    def get_hash(self):
        return self.__hash_value

    def __cal_hash(self):
        self.__hash_value.append(calc_hash.get_hash(self.__path))

    def __parse(self):
        result = []
        start_offset = self.__read_unil_value()
        while True:
            self.__file.seek(start_offset)
            info_list = dict()
            record_size = self.__file.read(4)
            if record_size == b'':
                break
            elif record_size == b'\x00\x00\x00\x00':
                start_offset = self.__read_unil_value()
            else:
                record_size = struct.unpack("<I", record_size)
                start_offset = start_offset+record_size[0]
            self.__file.read(12)
            parent_mft_r_num = self.__file.read(8)
            info_list["USN"] = struct.unpack("<Q", self.__file.read(8))[0]
            ts_time = struct.unpack("<Q", self.__file.read(8))
            if ts_time[0] == 0:
                continue
            try:
                info_list["Time"] = convert_time(ts_time[0]).strftime("%Y-%m-%d %H:%M:%S")
            except OverflowError:
                info_list["Time"] = 'none'
            info_list["Event Info"] = self.__reason_flag(self.__file.read(4))
            source_info = struct.unpack("<I", self.__file.read(4))[0]
            if source_info == 0:
                info_list["Source"] = "User"
            elif source_info == 1:
                info_list["Source"] = "OS"
            else:
                info_list["Source"] = "Others"
            security_id = self.__file.read(4).decode()
            info_list["File Attribute"] = self.__file_attr(self.__file.read(4))  # file_attr)
            name_size = struct.unpack("<H", self.__file.read(2))[0]
            offset_name = self.__file.read(2)
            try:
                name = self.__file.read(name_size)
                info_list["Filename"] = name.decode('utf-16')
            except UnicodeDecodeError:
                info_list["Filename"] = 'cannot decode'
            result.append(info_list)
        return result

    def __read_unil_value(self):
        while True:
            reader = self.__file.read(4)
            if reader != b'\x00\x00\x00\x00':
                break
        return self.__file.tell() - 4

    def __file_attr(self, file_attr):
        attr_type = [
            {'contents': 'Read-only', 'byte-index': 0, 'location': 3, 'hex': 1},
            {'contents': 'Hidden', 'byte-index': 0, 'location': 3, 'hex': 2},
            {'contents': 'SystemFile', 'byte-index': 0, 'location': 3, 'hex': 4},
            {'contents': 'Directory', 'byte-index': 0, 'location': 2, 'hex': 1},
            {'contents': 'Archive File', 'byte-index': 0, 'location': 2, 'hex': 2},
            {'contents': 'Device File', 'byte-index': 0, 'location': 2, 'hex': 4},
            {'contents': 'Normal', 'byte-index': 0, 'location': 2, 'hex': 8},
            {'contents': 'Temporary', 'byte-index': 1, 'location': 3, 'hex': 1},
            {'contents': 'Sparse', 'byte-index': 1, 'location': 3, 'hex': 2},
            {'contents': 'Reparse or Symbolic Link File', 'byte-index': 1, 'location': 3, 'hex': 4},
            {'contents': 'Compression', 'byte-index': 1, 'location': 3, 'hex': 8},
            {'contents': 'None Indexing', 'byte-index': 1, 'location': 2, 'hex': 2},
            {'contents': 'Encryption', 'byte-index': 1, 'location': 2, 'hex': 4},
            {'contents': 'Virtual File', 'byte-index': 2, 'location': 3, 'hex': 1}
        ]
        result = []
        for i in attr_type:
            value = hex(file_attr[i['byte-index']]).zfill(4)
            if value[i['location']] == str(i['hex']):
                result.append(i['contents'])
        if len(result) == 0:
            result.append('Others')
        return result

    def __reason_flag(self, file_attr):
        attr_type = [
            {'contents': 'Overwrite_$Data', 'byte-index': 0, 'location': 3, 'hex': 1},
            {'contents': 'Add Data_$Data', 'byte-index': 0, 'location': 3, 'hex': 2},
            {'contents': 'Delete Data_$Data', 'byte-index': 0, 'location': 3, 'hex': 4},
            {'contents': 'Overwrite_named $Data', 'byte-index': 0, 'location': 2, 'hex': 1},
            {'contents': 'Add Data_named $Data', 'byte-index': 0, 'location': 2, 'hex': 2},
            {'contents': 'Delete Data_named $Data', 'byte-index': 0, 'location': 2, 'hex': 4},
            {'contents': 'Creation_file or directory', 'byte-index': 1, 'location': 3, 'hex': 1},
            {'contents': 'Deletion_file or directory', 'byte-index': 1, 'location': 3, 'hex': 2},
            {'contents': 'Extended Properties Change', 'byte-index': 1, 'location': 3, 'hex': 4},
            {'contents': 'Change Access Rights', 'byte-index': 1, 'location': 3, 'hex': 8},
            {'contents': 'Renamed_Old', 'byte-index': 1, 'location': 2, 'hex': 1},
            {'contents': 'Renamed_New', 'byte-index': 1, 'location': 2, 'hex': 2},
            {'contents': 'Change Index Status', 'byte-index': 1, 'location': 2, 'hex': 4},
            {'contents': 'Attribute Change', 'byte-index': 1, 'location': 2, 'hex': 8},
            {'contents': 'HardLink Evente', 'byte-index': 2, 'location': 3, 'hex': 1},
            {'contents': 'Compressive State Change', 'byte-index': 2, 'location': 3, 'hex': 2},
            {'contents': 'Encryption State Change', 'byte-index': 2, 'location': 3, 'hex': 4},
            {'contents': 'Change Object ID', 'byte-index': 2, 'location': 3, 'hex': 8}]
        result = []
        for i in attr_type:
            value = hex(file_attr[i['byte-index']]).zfill(4)
            if value[i['location']] == str(i['hex']):
                result.append(i['contents'])
        if len(result) == 0:
            result.append('Others')
        return result


def filesys_filter(filter_list, json_list):
    __result = []

    for i in range(0, len(json_list)):
        for j in range(0, len(json_list[i][filter_list[0]])):
            if json_list[i][filter_list[0]][j] == filter_list[1]:
                __result.append(json_list[i])
    return __result


def unpack48(x):
    x1, x2, x3 = struct.unpack('<HHI', x)
    return x1, x2 | (x3 << 16)
