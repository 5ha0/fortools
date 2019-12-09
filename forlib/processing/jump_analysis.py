from forlib.processing.convert_time import convert_time
import struct
import forlib.calc_hash as calc_hash
from bitstring import BitArray
import olefile
import chardet


class JumplistAnalysis:
    def __init__(self, file, path, hash_v):
        self.__file = file
        self.__streams = file.listdir(streams=True, storages=False)
        self.__json_list = []
        self.__stream()
        self.__hash_value = [hash_v]
        self.__path = path
        self.__cal_hash()

    def __link_flag(self, flags_to_parse):
        lnk_flag = []
        flags = {0: "HasLinkTargetIDList",
                 1: "HasLinkInfo",
                 2: "HasName",
                 3: "HasRelativePath",
                 4: "HasWorkingDir",
                 5: "HasArguments",
                 6: "HasIconLocation",
                 7: "IsUnicode",
                 8: "ForceNoLinkInfo",
                 9: "HasExpString",
                 10: "RunInSeparateProcess",
                 11: "Unused1",
                 12: "HasDarwinID",
                 13: "RunAsUser",
                 14: "HasExpIcon",
                 15: "NoPidlAlias",
                 16: "Unused2",
                 17: "RunWithShimLayer",
                 18: "ForceNoLinkTrack",
                 19: "EnableTargetMetadata",
                 20: "DisableLinkPathTracking",
                 21: "DisableKnownFolderTracking",
                 22: "DisableKnownFolderAlias",
                 23: "AllowLinkToLink",
                 24: "UnaliasOnSave",
                 25: "PreferEnvironmentPath",
                 26: "KeepLocalIDListForUNCTarget"
                 }
        flags_to_parse = flags_to_parse[::-1]
        for count, items in enumerate(flags_to_parse):
            if int(items) == 1:
                lnk_flag.append(format(flags[count]))
            else:
                continue
        return lnk_flag

    def __lnk_attrib(self, attrib_to_parse):
        attrib = {0: "FILE_ATTRIBUTE_READONLY",
                  1: "FILE_ATTRIBUTE_HIDDEN",
                  2: "FILE_ATTRIBUTE_SYSTEM",
                  3: "Reserved1",
                  4: "FILE_ATTRIBUTE_DIRECTORY",
                  5: "FILE_ATTRIBUTE_ARCHIVE",
                  6: "Reserved2",
                  7: "FILE_ATTRIBUTE_NORMAL",
                  8: "FILE_ATTRIBUTE_TEMPORARY",
                  9: "FILE_ATTRIBUTE_SPARSE_FILE",
                  10: "FILE_ATTRIBUTE_REPARSE_POINT",
                  11: "FILE_ATTRIBUTE_COMPRESSED",
                  12: "FILE_ATTRIBUTE_OFFLINE",
                  13: "FILE_ATTRIBUTE_NOT_CONTENT_INDEXED",
                  14: "FILE_ATTRIBUTE_ENCRYPTED"
                  }
        lnk_attributes = []
        for count, items in enumerate(attrib_to_parse):
            if int(items) == 1:
                lnk_attributes.append(format(attrib[count]))
            else:
                continue
        return lnk_attributes

    def __drive_type_list(self, drive):
        drive_type = {
            0: 'DRIVE_UNKNOWN',
            1: 'DRIVE_NO_ROOT_DIR',
            2: 'DRIVE_REMOVABLE',
            3: 'DRIVE_FIXED',
            4: 'DRIVE_REMOTE',
            5: 'DRIVE_CDROM',
            6: 'DRIVE_RAMDISK'
        }
        for i in drive_type.keys():
            if drive == i:
                return drive_type[i]

    def __stream(self):
        for i in range(0, len(self.__streams)):
            data = self.__file.openstream(self.__streams[i])
            file_data = data.read()
            header_value = file_data[:4]

            if header_value[0] == 76:
                data_list = dict()
                lnk_flag = struct.unpack("<L", file_data[20:24])
                lnk_flag = BitArray(hex(lnk_flag[0]))
                link_flag = self.__link_flag(lnk_flag.bin)
                file_attr = struct.unpack("<I", file_data[24:28])
                file_attr = BitArray(hex(file_attr[0]))
                flag_attr = self.__lnk_attrib(file_attr.bin)
                # data_list["file attribute"] = flag_attr
                data_list["TimeZone"] = 'UTC +00:00'
                c_time = struct.unpack("<Q", file_data[28:36])
                data_list["create time"] = convert_time(c_time[0]).strftime("%Y-%m-%d %H:%M:%S")
                a_time = struct.unpack("<Q", file_data[36:44])
                data_list["access time"] = convert_time(a_time[0]).strftime("%Y-%m-%d %H:%M:%S")
                w_time = struct.unpack("<Q", file_data[44:52])
                data_list["write time"] = convert_time(w_time[0]).strftime("%Y-%m-%d %H:%M:%S")
                data_list["file size"] = self.__file.get_size(self.__streams[i])
                file_size = struct.unpack("<L", file_data[52:56])[0]
                data_list["target file size"] = file_size

                lnk_id_list_size = struct.unpack('<H', file_data[76:78])
                lnk_info_size = struct.unpack('<L', file_data[78 + lnk_id_list_size[0]:82 + lnk_id_list_size[0]])
                path_offset = struct.unpack('<L', file_data[94 + lnk_id_list_size[0]:94 + lnk_id_list_size[0] + 4])
                try:
                    volumeid_offset = struct.unpack("<L",file_data[90+lnk_id_list_size[0]:90+lnk_id_list_size[0]+4])
                    volumeid_size = struct.unpack("<L", file_data[78 + lnk_id_list_size[0] + volumeid_offset[0]:volumeid_offset[0] + 82 + lnk_id_list_size[0]])
                    drivetype =  struct.unpack("<L",file_data[82+lnk_id_list_size[0]+volumeid_offset[0]:volumeid_offset[0]+86+lnk_id_list_size[0]])

                    volumelabel_offset = struct.unpack("<L", file_data[90 + lnk_id_list_size[0] + volumeid_offset[0]:volumeid_offset[0] + 94 + lnk_id_list_size[0]])
                    if volumelabel_offset[0] == 14:
                        offset1 = volumeid_size[0] - (4 + 4 + 4 + 4 + 4)
                    else:
                        offset1 = volumeid_size[0] - (4 + 4 + 4 + 4)
                    drive_serial_num = struct.unpack("<L", file_data[86 + lnk_id_list_size[0] + volumeid_offset[0]:volumeid_offset[0] + 90 +lnk_id_list_size[0]])[0]
                    volumelabel = file_data[ volumeid_offset[0] + 94 + lnk_id_list_size[0]:volumeid_offset[0] + 94 +lnk_id_list_size[0] + offset1]
                    volumelabel = decode_str(volumelabel)
                    drivetype = self.__drive_type_list(drivetype[0])
                except struct.error:
                    continue

                if 'HasLinkInfo' in link_flag:
                    size = lnk_info_size[0] - path_offset[0]
                    local_path = file_data[78 + lnk_id_list_size[0] + path_offset[0]:78 + lnk_id_list_size[0] + path_offset[0] + size]
                    data_list["Local Path"] = decode_str(local_path)
                elif 'HasRelativePath' in link_flag:
                    net_offset = struct.unpack("<L", file_data[98 + lnk_id_list_size[0]:102 + lnk_id_list_size[0]])
                    size = net_offset[0] - path_offset[0]
                    local_path = file_data[78 + lnk_id_list_size[0] + path_offset[0]:78 + lnk_id_list_size[0] + path_offset[0] + size]
                    data_list["Local Path"] = decode_str(local_path)
                data_list["drive type"] = drivetype
                data_list["drive serial number"] = drive_serial_num
                data_list["Volume Label"] = volumelabel
                self.__json_list.append(data_list)
            else:
                self.__destlist = file_data

    def __cal_hash(self):
        self.__hash_value.append(calc_hash.get_hash(self.__path))

    def get_hash(self):
        return self.__hash_value

    def get_summary(self, ver):
        info_list = dict()
        total_num = struct.unpack("<L", self.__destlist[4:8])[0]
        info_list["Total Num of JumpList"] = total_num
        num_action = self.__destlist[24:32]
        info_list["Total Num of Add/Delete/Open action"] = num_action[0]
        netbiosname = self.__destlist[104:120]
        entryidnumber = struct.unpack("<L", self.__destlist[120:124])
        info_list["Netbios"] = decode_str(netbiosname) #netbiosname.replace('\x00','')
        time = struct.unpack("<Q", self.__destlist[132:140])
        info_list["TimeZone"] = 'UTC +00:00'
        info_list["Last Access Time"] = convert_time(time[0]).strftime("%Y-%m-%d %H:%M:%S")
        cnt = struct.unpack("<L", self.__destlist[148:152])
        info_list["Access Count"] = cnt[0]
        if ver == 7:
            len_stringdata = struct.unpack("<H", self.__destlist[144:146])
            destlist_stringdata = self.__destlist[146:146 + len_stringdata[0]*2]

            info_list["Data String"] =decode_str(destlist_stringdata)# destlist_stringdata.decode('utf-16')
        elif ver == 10:
            len_stringdata = struct.unpack("<H", self.__destlist[160:162])
            destlist_stringdata = self.__destlist[162:162 + 2 * len_stringdata[0]]
            info_list["Data String"] = destlist_stringdata.decode('utf-16')
        return [info_list]

    def get_destlist_data(self, ver):
        result = []
        total_num = struct.unpack("<L", self.__destlist[4:8])
        entryidnumber = struct.unpack("<L", self.__destlist[120:124])
        if ver == 7:
            len_stringdata = struct.unpack("<H", self.__destlist[144:146])
            offset = 146 + 2 * len_stringdata[0]
        elif ver==10:
            len_stringdata = struct.unpack("<H", self.__destlist[160:162])
            offset = 166 + 2 * len_stringdata[0]
        for entry in range(total_num[0] - 1):
            if entryidnumber[0] > 1:
                info_list = dict()
                if ver==10:
                    mac = self.__destlist[offset + 34:offset + 40]
                    info_list["MAC(new)"] = format(mac[0], '02x') + ':' + format(mac[1], '02x') + ':' + format(mac[2],'02x') + ':' + format(mac[3], '02x') + ':' + format(mac[4], '02x') + ':' + format(mac[5], '02x')
                    mac = self.__destlist[offset + 66:offset + 72]
                    info_list["MAC(birth)"] = format(mac[0], '02x') + ':' + format(mac[1], '02x') + ':' + format(mac[2],'02x') + ':' + format(mac[3], '02x') + ':' + format(mac[4], '02x') + ':' + format(mac[5], '02x')
                    netbiosname = self.__destlist[offset+72:offset+88]
                    try:
                        info_list["netbios"] = netbiosname.decode('ascii').replace('\x00','')
                    except UnicodeDecodeError:
                        info_list["netbios"] = 'cannot decode'
                    entryidnumber = struct.unpack("<L", self.__destlist[offset + 88:offset + 92])
                    last_access_time = struct.unpack("<Q", self.__destlist[offset + 100:offset + 108])
                    info_list["TimeZone"] = 'UTC +00:00'
                    info_list["last access time"] = convert_time(last_access_time[0]).strftime("%Y-%m-%d %H:%M:%S")
                    access_cnt = struct.unpack("<L", self.__destlist[offset + 116:offset + 120])
                    info_list["access count"] = access_cnt[0]
                    len_stringdata = struct.unpack("<H", self.__destlist[offset + 128:offset + 130])
                    offset_new = offset + 130 + 2 * len_stringdata[0]
                    string_data = self.__destlist[offset + 130:offset_new]
                    info_list["data"] = string_data.decode('utf-16')
                    offset = offset_new + 4
                    result.append(info_list)
                elif ver==7:
                    try:
                        mac = self.__destlist[offset + 34:offset + 40]
                        info_list["MAC(new)"] = format(mac[0],'02x')+':'+format(mac[1],'02x')+':'+format(mac[2],'02x')+':'+format(mac[3],'02x')+':'+format(mac[4],'02x')+':'+format(mac[5],'02x')
                        mac = self.__destlist[offset + 66:offset + 72]
                        info_list["MAC(birth)"] = format(mac[0], '02x') + ':' + format(mac[1], '02x') + ':' + format(mac[2], '02x') + ':' + format(mac[3], '02x') + ':' + format(mac[4], '02x') + ':' + format(mac[5], '02x')
                        netbiosname = self.__destlist[offset + 72:offset + 88]
                        try:
                            info_list["netbios"] = netbiosname.decode('ascii').replace('\x00','')
                        except UnicodeDecodeError:
                            info_list["netbios"] = 'cannot decode'
                        entryidnumber = struct.unpack("<Q", self.__destlist[offset + 88:offset + 96])
                        last_access_time = struct.unpack("<Q", self.__destlist[offset + 100:offset + 108])
                        info_list["TimeZone"] = 'UTC +00:00'
                        info_list["last access time"] = convert_time(last_access_time[0]).strftime("%Y-%m-%d %H:%M:%S")
                        len_stringdata = struct.unpack("<H", self.__destlist[offset + 112:offset + 114])
                        offset_new = offset + 114 + 2 * len_stringdata[0]
                        string_data = self.__destlist[offset+114 :offset_new]
                        info_list["data"] = string_data.decode('utf-16')
                        new_time = struct.unpack("<Q", self.__destlist[offset + 24:offset + 32])
                        if new_time[0] == 0:
                            info_list["new time"] = 'non info'
                        else:
                            new_time2 = self.__convert_hex(hex(new_time[0]))
                            info_list["new time"] = convert_time(new_time2 - 5748192000000000).strftime("%Y-%m-%d %H:%M:%S")
                        birth_time = struct.unpack("<Q", self.__destlist[offset + 56:offset + 64])
                        if birth_time[0] == 0:
                            info_list["birth time"] = 'non info'
                        else:
                            birth_time2 = self.__convert_hex(hex(birth_time[0]))
                            info_list["birth time"] = convert_time(birth_time2 - 5748192000000000).strftime("%Y-%m-%d %H:%M:%S")

                        offset = offset_new
                        result.append(info_list)
                    except:
                        pass
        return result

    def show_info(self):
        for i in self.__json_list:
            print(i)

    def get_all_info(self):
        return self.__json_list

    def get_info(self):
        result = []
        for i in self.__json_list:
            info = dict()
            try:
                for j in list:
                    info[j] = i[j]
                result.append(info)
            except KeyError:
                print("Plz check your key.")
                return -1
        return result

    def __convert_hex(self,gethex):
        gethex = gethex[:2] + "0" + gethex[3:]
        return int(gethex, 0)

def decode_str(data):
    encoding_list = chardet.detect(data)['encoding']
    if encoding_list == None:
        encoding_list = 'ascii'
    try:
        result = data.decode(encoding_list).replace('\x00', '')
    except UnicodeDecodeError:
        try:
            result = data.decode('cp949').replace('\x00', '')
        except UnicodeDecodeError:
            result = 'cannot decode'
    return result
