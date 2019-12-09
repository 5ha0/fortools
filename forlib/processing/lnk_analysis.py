from datetime import datetime, timedelta
import struct
from bitstring import BitArray
import os
import json
import forlib.calc_hash as calc_hash


class LnkAnalysis:

    def __init__(self, file, path, hash_v):
        self.file = file
        self.path = path
        self.__hash_value = [hash_v]
        self.lnk_flag = []
        self.locbase_path_uni_off = None
        self.start_off = None
        self.info_size = None
        self.info_flag = None
        self.extra_off = None
        self.extra_data = None
        self.linkinfo_flag = self.__link_flags()

    def __lnk_flag(self, flags_to_parse):
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
                self.lnk_flag.append(format(flags[count]))
            else:
                continue
        print(self.lnk_flag)
        return self.lnk_flag

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
        attrib_to_parse = attrib_to_parse[::-1]
        for count, items in enumerate(attrib_to_parse):
            if int(items) == 1:
                lnk_attributes.append(format(attrib[count]))
            else:
                continue
        print(lnk_attributes)

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

        # drive_type_list = []
        # for count, items in enumerate(drive):
        #     if int(items) == 1:
        #         drive_type_list.append(format(drive_type[count]))
        #     else:
        #         continue
        #
        # return drive_type_list

    ################ Shell_Link_Header #############################

    # show link flag
    def __link_flags(self):
        self.file.seek(20)
        flags = struct.unpack('<i', self.file.read(4))
        file_flags = BitArray(hex(flags[0]))
        self.__lnk_flag(file_flags.bin)

    def file_attribute(self):
        self.file.seek(24)
        attributes = struct.unpack('<i', self.file.read(4))
        flag_atributes = BitArray(hex(attributes[0]))
        flag_atributes = self.__lnk_attrib(flag_atributes.bin)

        lnk_list = []
        for i in range(0, len(flag_atributes)):
            lnk_obj = {"File Attributes": flag_atributes[i]}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)

        return lnk_list

    # Target File time
    def creation_time(self):
        self.file.seek(28)
        c_time = self.file.read(8)
        c_time = struct.unpack('<q', c_time)
        c_time = convert_time(c_time)

        lnk_list = []
        lnk_obj = {'Target File Creation Time': str(c_time),
                   'TimeZone': 'UTC'}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    def access_time(self):
        self.file.seek(36)
        a_time = self.file.read(8)
        a_time = struct.unpack_from('<q', a_time)[0]
        a_time = convert_time(a_time)

        lnk_list = []
        lnk_obj = {'Target File Access Time': str(a_time),
                   "TimeZone": 'UTC'}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    def write_time(self):
        self.file.seek(44)
        w_time = self.file.read(8)
        w_time = struct.unpack('<q', w_time)[0]
        w_time = convert_time(w_time)

        lnk_list = []
        lnk_obj = {'Target File Write Time': str(w_time),
                   "TimeZone": 'UTC'}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    # Link file Time

    def lnk_creation_time(self):
        c_time = datetime.fromtimestamp(os.path.getctime(self.path))

        lnk_list = []
        lnk_obj = {'Link File Creation Time': str(c_time),
                   "TimeZone": 'SYSTEM TIME'}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    def lnk_access_time(self):
        a_time = datetime.fromtimestamp(os.path.getatime(self.path))

        lnk_list = []
        lnk_obj = {'Link File Last Access Time': str(a_time),
                   "TimeZone": 'SYSTEM TIME'}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    def lnk_write_time(self):
        w_time = datetime.fromtimestamp(os.path.getmtime(self.path))

        lnk_list = []
        lnk_obj = {'Link File Write Time': str(w_time),
                   "TimeZone": 'SYSTEM TIME'}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    def file_size(self):
        self.file.seek(52)
        file_size = struct.unpack('<l', self.file.read(4))[0]

        lnk_list = []
        lnk_obj = {'Target File Size': str(file_size) + 'bytes'}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    def iconindex(self):
        self.file.seek(56)
        iconindex = struct.unpack('<l', self.file.read(4))[0]

        lnk_list = []
        lnk_obj = {'IconIndex': str(iconindex)}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    def show_command(self):
        self.file.seek(60)
        showcomand = struct.unpack('<i', self.file.read(4))[0]
        showcomand = hex(showcomand)
        if showcomand == hex(0x1):
            showcomand = 'SW_SHOWNORMAL'
        elif showcomand == hex(0x3):
            showcomand = 'SW_SHOWMAXIMIZED'
        elif showcomand == hex(0x7):
            showcomand = 'SW_SHOWMINNOACTIVE'
        else:
            showcomand = 'SW_SHOWNORMAL(default)'

        lnk_list = []
        lnk_obj = {'Show Command': str(showcomand)}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    ################ Link_Info #############################

    def __lnkinfo_off(self):

        if 'HasLinkTargetIDList' not in self.lnk_flag:
            self.start_off = 76
        else:
            self.file.seek(76)
            items_hex = self.file.read(2)
            b = bytes(b'\x00\x00')
            items_hex = items_hex + b
            idlistsize = struct.unpack('<i', items_hex)[0]
            self.start_off = 78 + idlistsize

        if 'HasLinkInfo' not in self.lnk_flag:
            self.linkinfo_flag = None
            #Input the value to use on the __extradata() below
            self.start_off = 76
            self.info_size = 0
            return 0
        else:
            self.linkinfo_flag = 'True'

        self.file.seek(self.start_off)
        self.info_size = struct.unpack('<i', self.file.read(4))[0]
        info_header_size = struct.unpack('<i', self.file.read(4))[0]
        if info_header_size == 28:
            info_optional = 'not set'
        elif info_header_size >= 36:
            info_optional = 'set'
        self.info_flag = self.file.read(4)
        if self.info_flag == bytes(b'\x01\x00\x00\x00'):
            self.info_flag = 'A'
            # volume_id = 'present'
            # local_base_path = 'present'
            if info_optional == 'set':
                self.locbase_path_uni_off = 'set'
            else:
                self.locbase_path_uni_off = 'None'
        else:
            self.info_flag = 'B'
            # volume = None
            # locbase_path = None
            if info_optional == 'set':
                self.locbase_path_uni_off = '0'
            else:
                self.locbase_path_uni_off = 'None'

        return 0

    def volume(self):
        lnk_list = []

        self.__lnkinfo_off()

        if self.linkinfo_flag != 'True':
            print('HasLinkInfo: False')
            lnk_obj1 = {'Drivetype': 'None',
                        'Driveserialnumber': 'None',
                        'Volumelable': 'None'}
            json.dumps(lnk_obj1)
            lnk_list.append(lnk_obj1)
            return lnk_list
        elif self.info_flag != 'A':
            print('volume id (X)')
            lnk_obj = {'Drivetype': 'None',
                       'Driveserialnumber': 'None',
                       'Volumelable': 'None'}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)
            return lnk_list
        vol_off = self.start_off + 12
        self.file.seek(vol_off)
        volumeid_off = struct.unpack('<i', self.file.read(4))[0]
        volumeid_off = volumeid_off + self.start_off
        self.file.seek(volumeid_off)
        print(self.file.tell())
        vol_size = struct.unpack('<i', self.file.read(4))[0]
        print(vol_size)

        drive_type = struct.unpack('<i', self.file.read(4))[0]
        drive_type = self.__drive_type_list(drive_type)

        driveserialnumber = struct.unpack('<i', self.file.read(4))[0]

        volumelable_off = self.file.read(4)
        if volumelable_off == bytes(b'\x10\x00\x00\x00'):
            volumelable_off = struct.unpack('<i', volumelable_off)[0]
            volumelable_off = volumeid_off + volumelable_off
        else:
            volumelable_off_uni = struct.unpack('<i', self.file.read(4))[0]
            volumelable_off = volumeid_off + volumelable_off_uni
        self.file.seek(volumelable_off)
        end = vol_size + volumeid_off
        volumelable_size = end - volumelable_off

        volumelable = self.file.read(volumelable_size)
        volumelable = volumelable.decode('utf-8', 'ignore')

        lnk_obj = {'Drivetype': drive_type,
                   'Driveserialnumber': str(driveserialnumber),
                   'Volumelable': volumelable}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list


    def localbase_path(self):
        lnk_list = []

        self.__lnkinfo_off()

        if self.linkinfo_flag != 'True':
            print('HasLinkInfo: False')
            lnk_obj = {'Localbasepath Unicode': 'None',
                       'Localbasepath': 'None'}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)

            return lnk_list
        elif self.info_flag != 'A':
            print('locabasepath (X), locabasepathunicode (X)')
            lnk_obj = {'Localbasepath Unicode': self.locbase_path_uni_off,
                       'Localbasepath': 'None'}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)

            return lnk_list

        elif self.locbase_path_uni_off == 'set':
            locbase_path_off_uni = self.start_off + 28
            self.file.seek(locbase_path_off_uni)
            locbase_path_off_uni = struct.unpack('<l', self.file.read(4))[0]
            com_path_off_uni = struct.unpack('<l', self.file.read(4))[0]
            locbase_path_off_uni = locbase_path_off_uni + self.start_off
            com_path_off_uni = com_path_off_uni + self.start_off
            self.file.seek(locbase_path_off_uni)
            read_info_size = com_path_off_uni - locbase_path_off_uni
            self.locbase_path_uni_off = self.file.read(read_info_size)
            self.locbase_path_uni_off.split(bytes(b'\x00\x00'))
            self.locbase_path_uni_off = self.locbase_path_uni.decode('utf-8', 'ignore')


        locbasepath_off = self.start_off + 16
        self.file.seek(locbasepath_off)
        locbasepath_off = struct.unpack('<l', self.file.read(4))[0]
        end = self.start_off + 24
        self.file.seek(end)
        end = struct.unpack('<l', self.file.read(4))[0]
        end = end + self.start_off
        locbasepath_off = locbasepath_off + self.start_off

        self.file.seek(locbasepath_off)
        read_info_size = end - locbasepath_off

        locbasepath = self.file.read(read_info_size)
        locbasepath = locbasepath.decode('utf-8', 'ignore')
        locbasepath = locbasepath.replace('\x00', '')

        lnk_obj = {'Localbasepath Unicode': self.locbase_path_uni_off,
                   'Localbasepath': locbasepath}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    ################ Extra_Data #############################
    def __extradata_size(self, string_off):
        self.file.seek(string_off)
        string_size = self.file.read(2)
        b = bytes(b'\x00\x00')
        string_size = string_size + b
        string_size = struct.unpack('<i', string_size)[0]
        string_size = string_size * 2

        # if you want to read string, use this
        # relative_path = self.file.read(string_size)
        # relative_path = relative_path.decode('utf8', 'ignore')
        # relative_path = relative_path.replace('\x00', '')
        # print(relative_path)

        string_off = string_size + string_off + 2
        return string_off

    def __string_data(self):
        self.__lnkinfo_off()

        string_off = self.start_off + self.info_size

        if 'HasName' in self.lnk_flag:
            string_off = self.__extradata_size(string_off)

        if 'HasRelativePath' in self.lnk_flag:
            print(string_off)
            print('1')
            string_off = self.__extradata_size(string_off)
            print(string_off)
            print('2')

        if 'HasWorkingDir' in self.lnk_flag:
            print(string_off)
            print('3')
            string_off = self.__extradata_size(string_off)
            print(string_off)
            print('dfgsdfgdfsg')

        if 'HasArguments' in self.lnk_flag:
            string_off = self.__extradata_size(string_off)

        if 'HasIconLocation' in self.lnk_flag:
            string_off = self.__extradata_size(string_off)

        self.extra_off = string_off

        self.extra_data = None

        while(1):
            self.file.seek(self.extra_off)
            block_size = struct.unpack('<i', self.file.read(4))[0]
            if block_size < 4:
                break
            block_signature = self.file.read(4)
            if block_signature == bytes(b'\x03\x00\x00\xa0'):
                self.extra_data = 'True'
                break
            else:
                self.extra_off = self.extra_off + block_size

    def netbios(self):
        self.__string_data()

        lnk_list = []

        if self.extra_data != 'True':
            print('netbios data (X)')
            lnk_obj = {'NetBios': 'None'}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)

            return lnk_list

        netbios = self.extra_off + 16
        self.file.seek(netbios)
        netbios = self.file.read(16)
        netbios = netbios.decode('utf8', 'ignore')
        netbios = netbios.replace(('\x00'), '')

        lnk_obj = {'NetBios': str(netbios)}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    def machine_id(self):
        self.__string_data()

        lnk_list = []

        if self.extra_data != 'True':
            print('machine id (X)')
            lnk_obj = {'Droid': 'None',
                       'DroidBirth': 'None'}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)

            return lnk_list
        droid = self.extra_off + 32
        self.file.seek(droid)
        droid = str(self.file.read(32))
        # droid = droid.decode('cp949', 'ignore')
        # droid = droid.replace(('\x00'), '')

        droidbirth = str(self.file.read(32))
        droidbirth = droidbirth.replace('\\x00', '').encode('utf-16', 'ignore').decode('utf-16', 'ignore')

        lnk_obj = {'Droid': str(droid),
                   'DroidBirth': str(droidbirth)}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

################################################################################

    # calculate hash value after parsing
    def cal_hash(self):
        lnk_list = []
        lnk_obj = dict()
        self.__hash_value.append(calc_hash.get_hash(self.path))
        lnk_obj['before_sha1'] = self.__hash_value[0]['sha1']
        lnk_obj['before_md5'] = self.__hash_value[0]['md5']
        lnk_obj['after_sha1'] = self.__hash_value[1]['sha1']
        lnk_obj['after_md5'] = self.__hash_value[1]['md5']

        lnk_list.append(lnk_obj)

        return lnk_list

#################################################################################

    def show_all_info(self):
        info_list = []
        info = dict()
        file_attribute = self.file_attribute()
        for i in range(0, len(file_attribute)):
            info["File Attributes"+ str(i)] = file_attribute[i]['File Attributes']
        t_creation_time = self.creation_time()
        info["Target File Creation Time"] = t_creation_time[0]['Target File Creation Time']
        info['Target File Creation TimeZone'] = t_creation_time[0]['TimeZone']
        t_access_time = self.access_time()
        info["Target File Access Time"] = t_access_time[0]['Target File Access Time']
        info['Target File Access TimeZone'] = t_access_time[0]['TimeZone']
        t_write_time = self.write_time()
        info['Target File Write Time'] = t_write_time[0]['Target File Write Time']
        info['Target File Write TimeZone'] = t_write_time[0]['TimeZone']
        l_creation_time = self.lnk_creation_time()
        info['Link File Creation Time'] = l_creation_time[0]['Link File Creation Time']
        info['Link File Creation TimeZone'] = l_creation_time[0]['TimeZone']
        l_access_time = self.lnk_access_time()
        info['Link File Last Access Time'] = l_access_time[0]['Link File Last Access Time']
        info['Link File Last Access TimeZone'] = l_access_time[0]['TimeZone']
        l_write_time = self.lnk_write_time()
        info['Link File Write Time'] = l_write_time[0]['Link File Write Time']
        info['Link File Write TimeZone'] = l_write_time[0]['TimeZone']
        info['Target File Size'] = self.file_size()[0]['Target File Size']
        info["IconIndex"] = self.iconindex()[0]['IconIndex']
        info["Show Command"] = self.show_command()[0]['Show Command']
        volume = self.volume()
        info['Drivetype'] = volume[0]['Drivetype']
        info["Driveserialnumber"] = volume[0]['Driveserialnumber']
        info["Volumelable"] = volume[0]['Volumelable']
        localbase = self.localbase_path()
        info['Localbasepath Unicode'] = localbase[0]['Localbasepath Unicode']
        info['Localbasepath'] = localbase[0]['Localbasepath']
        info["NetBios"] = self.netbios()[0]['NetBios']
        machine = self.machine_id()
        info["Droid"] = machine[0]['Droid']
        info["DroidBirth"] = machine[0]['DroidBirth']
        hash = self.cal_hash()
        info['before_sha1'] = hash[0]['before_sha1']
        info['before_md5'] = hash[0]['before_md5']
        info['after_sha1'] = hash[0]['after_sha1']
        info['after_md5'] = hash[0]['after_md5']

        print(info)
        info_list.append(info)

        return info_list

    def get_all_info(self):
        info_list = []
        info = dict()
        file_attribute = self.file_attribute()
        for i in range(0, len(file_attribute)):
            info["File Attributes"+ str(i)] = file_attribute[i]['File Attributes']
        t_creation_time = self.creation_time()
        info["Target File Creation Time"] = t_creation_time[0]['Target File Creation Time']
        info['Target File Creation TimeZone'] = t_creation_time[0]['TimeZone']
        t_access_time = self.access_time()
        info["Target File Access Time"] = t_access_time[0]['Target File Access Time']
        info['Target File Access TimeZone'] = t_access_time[0]['TimeZone']
        t_write_time = self.write_time()
        info['Target File Write Time'] = t_write_time[0]['Target File Write Time']
        info['Target File Write TimeZone'] = t_write_time[0]['TimeZone']
        l_creation_time = self.lnk_creation_time()
        info['Link File Creation Time'] = l_creation_time[0]['Link File Creation Time']
        info['Link File Creation TimeZone'] = l_creation_time[0]['TimeZone']
        l_access_time = self.lnk_access_time()
        info['Link File Last Access Time'] = l_access_time[0]['Link File Last Access Time']
        info['Link File Last Access TimeZone'] = l_access_time[0]['TimeZone']
        l_write_time = self.lnk_write_time()
        info['Link File Write Time'] = l_write_time[0]['Link File Write Time']
        info['Link File Write TimeZone'] = l_write_time[0]['TimeZone']
        info['Target File Size'] = self.file_size()[0]['Target File Size']
        info["IconIndex"] = self.iconindex()[0]['IconIndex']
        info["Show Command"] = self.show_command()[0]['Show Command']
        volume = self.volume()
        info['Drivetype'] = volume[0]['Drivetype']
        info["Driveserialnumber"] = volume[0]['Driveserialnumber']
        info["Volumelable"] = volume[0]['Volumelable']
        localbase = self.localbase_path()
        info['Localbasepath Unicode'] = localbase[0]['Localbasepath Unicode']
        info['Localbasepath'] = localbase[0]['Localbasepath']
        info["NetBios"] = self.netbios()[0]['NetBios']
        machine = self.droid_value()
        info["Droid"] = machine[0]['Droid']
        info["DroidBirth"] = machine[0]['DroidBirth']
        hash = self.cal_hash()
        info['before_sha1'] = hash[0]['before_sha1']
        info['before_md5'] = hash[0]['before_md5']
        info['after_sha1'] = hash[0]['after_sha1']
        info['after_md5'] = hash[0]['after_md5']

        info_list.append(info)

        return info_list

def convert_time(time):
    time = '%016x' % time
    time = int(time, 16) / 10.
    time = datetime(1601, 1, 1) + timedelta(microseconds=time) + timedelta(hours=9)
    return time        
