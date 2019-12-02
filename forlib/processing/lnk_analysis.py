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
        self.locbase_path_uni = None
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

        for count, items in enumerate(flags_to_parse):
            if int(items) == 1:
                self.lnk_flag.append(format(flags[count]))
            else:
                continue

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

        drive_type_list = []
        for count, items in enumerate(drive):
            if int(items) == 1:
                drive_type_list.append(format(drive_type[count]))
            else:
                continue

        return drive_type_list

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
                   'TimeZone': 'UTC +9'}
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
                   "TimeZone": 'UTC +9'}
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
                   "TimeZone": 'UTC +9'}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    # Link file Time

    def lnk_creation_time(self):
        c_time = datetime.fromtimestamp(os.path.getctime(self.path))

        lnk_list = []
        lnk_obj = {'Link File Creation Time': str(c_time),
                   "TimeZone": 'UTC +9'}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    def lnk_access_time(self):
        a_time = datetime.fromtimestamp(os.path.getatime(self.path))

        lnk_list = []
        lnk_obj = {'Link File Last Access Time': str(a_time),
                   "TimeZone": 'UTC +9'}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    def lnk_write_time(self):
        w_time = datetime.fromtimestamp(os.path.getmtime(self.path))

        lnk_list = []
        lnk_obj = {'Link File Write Time': str(w_time),
                   "TimeZone": 'UTC +9'}
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

        if 'HasLinkInfo' not in self.lnk_flag:
            self.linkinfo_flag = None
            #Input the value to use on the __extradata() below
            self.start_off = 76
            self.info_size = 0
            return 0
        else:
            self.linkinfo_flag = 'True'

        if 'HasLinkTargetIDList' not in self.lnk_flag:
            self.start_off = 76
        else:
            self.file.seek(76)
            items_hex = self.file.read(2)
            b = (b'\x00\x00')
            items_hex = items_hex + b
            idlistsize = struct.unpack('<i', items_hex)[0]
            self.start_off = 78 + idlistsize

        self.file.seek(self.start_off)
        self.info_size = struct.unpack('<i', self.file.read(4))[0]
        info_header_size = self.file.read(4)
        if info_header_size == '\x00\x00\x00\x1C':
            info_option = 'False'
        else:
            info_option = 'True'
        self.info_flag = self.file.read(4)
        if self.info_flag == '\x00\x00\x00\x01':
            self.info_flag = 'A'
            # volume = 'True'
            # locbase_path = 'True'
            # net = None
            if info_option == 'True':
                self.locbase_path_uni = 'True'
            else:
                self.locbase_path_uni = None
        else:
            self.info_flag = 'B'
            # volume = None
            # locbase_path = None
            # net = 'True'
            self.locbase_path_uni = None

    def volume(self):
        lnk_list = []

        self.__lnkinfo_off()

        if self.linkinfo_flag != 'True':
            print('link info (X)')
            lnk_obj = {'Drivetype': 'None'}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)
            lnk_obj1 = {'Driveserialnumber': 'None',
                        'Volumelable': 'None'}
            json.dumps(lnk_obj1)
            lnk_list.append(lnk_obj1)
            return lnk_list
        elif self.info_flag != 'A':
            print('volume id (X)')
            lnk_obj = {'Drivetype': 'None'}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)
            lnk_obj = {'Driveserialnumber': 'None',
                       'Volumelable': 'None'}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)
            return lnk_list

        vol_off = self.start_off + 12
        self.file.seek(vol_off)
        volumeid_off = struct.unpack('<i', self.file.read(4))[0]
        volumeid_off = volumeid_off + self.start_off
        self.file.seek(volumeid_off)

        vol_size = struct.unpack('<i', self.file.read(4))[0]

        drive_type = struct.unpack('<i', self.file.read(4))[0]
        drive_type = self.__drive_type_list(drive_type)

        driveserialnumber = struct.unpack('<l', self.file.read(4))[0]

        volumelable_off = self.file.read(4)
        if volumelable_off != '0x00000014':
            volumelable_off = struct.unpack('<l', volumelable_off)[0]
            vol_lable_off = volumelable_off
            volumelable_off = volumeid_off + volumelable_off
        else:
            volumelable_off_uni = struct.unpack('<l', self.file.read(4))[0]
            vol_lable_off = volumelable_off_uni
            volumelable_off = volumeid_off + volumelable_off_uni
        self.file.seek(volumelable_off)
        volumelable_size = vol_size - vol_lable_off
        volumelable = self.file.read(volumelable_size)
        volumelable = volumelable.decode('cp1252')

        for i in range(0, len(drive_type)):
            lnk_obj = {"Drivetype": drive_type[i]}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)
        lnk_obj = {'Driveserialnumber': str(driveserialnumber),
                   'Volumelable': volumelable}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list


    def localbase_path(self):
        lnk_list = []

        self.__lnkinfo_off()

        if self.linkinfo_flag != 'True':
            print('this file does not have link info')
            lnk_obj = {'Localbasepath Unicode': 'None',
                       'Localbasepath': 'None'}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)

            return lnk_list
        elif self.info_flag != 'A':
            print('locabasepath (X), locabasepathunicode (X)')
            lnk_obj = {'Localbasepath Unicode': 'None',
                       'Localbasepath': 'None'}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)

            return lnk_list
        elif self.locbase_path_uni != 'True':
            lnk_obj = {'Localbasepath Unicode': '0',
                       'Localbasepath': 'unknown'}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)

            return lnk_list
        else:
            locbase_path_off_uni = self.start_off + 28
            self.file.seek(locbase_path_off_uni)
            locbase_path_off_uni = struct.unpack('<l', self.file.read(4))[0]
            self.locbase_path_uni = locbase_path_off_uni + self.start_off
            self.file.seek(self.locbase_path_uni)
            self.locbase_path_uni = self.file.read(100)
            self.locbase_path_uni = self.locbase_path_uni.decode('utf-8', 'ignore')
            self.locbase_path_uni = []
            for i in self.locbase_path_uni.split('\x00\x00'):
                self.locbase_path_uni.append(i)

        locbasepath_off = self.start_off + 16
        self.file.seek(locbasepath_off)
        locbasepath_off = struct.unpack('<l', self.file.read(4))[0]
        locbasepath_off = locbasepath_off + self.start_off

        self.file.seek(locbasepath_off)
        locbasepath = self.file.read(100)
        locbasepath = locbasepath.decode('utf-8', 'ignore')
        locbasepath = []
        for i in locbasepath.split('\x00\x00'):
            locbasepath.append(i)

        lnk_obj = {'Localbasepath Unicode': self.locbase_path_uni[0],
                   'Localbasepath': locbasepath[0]}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    ################ Extra_Data #############################
    def __extradata_size(self, string_off):
        self.file.seek(string_off)
        string_size = self.file.read(2)
        b = (b'\x00\x00')
        string_size = string_size + b
        string_size = struct.unpack('<i', string_size)[0]

        # if you want to read string, use this
        # relative_path = self.file.read(string_size)
        # relative_path = relative_path.decode('utf8', 'ignore')
        # relative_path = relative_path.replace('\x00', '')

        string_off = string_size + string_off + 2
        return string_off

    def __string_data(self):
        self.__lnkinfo_off()

        string_off = self.start_off + self.info_size

        if 'HasName' in self.lnk_flag:
            string_off = self.__extradata_size(string_off)

        elif 'HasRelativePath' in self.lnk_flag:
            string_off = self.__extradata_size(string_off)

        elif 'HasWorkingDir' in self.lnk_flag:
            string_off = self.__extradata_size(string_off)

        elif 'HasArguments' in self.lnk_flag:
            string_off = self.__extradata_size(string_off)

        elif 'HasIconLocation' in self.lnk_flag:
            string_off = self.__extradata_size(string_off)

        self.extra_off = string_off
        block_signature = self.extra_off + 4
        self.file.seek(block_signature)
        block_signature = self.file.read(4)
        if block_signature == '\xA0\x00\x00\x03':
            self.extra_data = 'True'
        else:
            self.extra_data = None

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
        netbios = str(self.file.read(16))
        netbios = netbios.replace('\x00', '').encode('utf-8', 'ignore').decode('utf-8')

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
        droid = droid.replace('\x00', '').encode('utf-8', 'ignore').decode('utf-8')

        droidbirth = str(self.file.read(32))
        droidbirth = droidbirth.replace('\x00', '').encode('utf-8', 'ignore').decode('utf-8')

        lnk_obj = {'Droid': str(droid),
                   'DroidBirth': str(droidbirth)}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

################################################################################

    # calculate hash value after parsing
    def cal_hash(self):
        self.__hash_value.append(calc_hash.get_hash(self.path))

#################################################################################

    def show_all_info(self):
        info_list = []
        info = dict()
        file_attribute = self.file_attribute()
        for i in range(0, len(file_attribute)):
            info["File Attributes"+ str(i)] = file_attribute[i]['File Attributes']
        t_creation_time = self.creation_time()
        info["Target File Creation Time"] = t_creation_time[0]['Target File Creation Time']
        info['TimeZone'] = t_creation_time[0]['TimeZone']
        t_access_time = self.access_time()
        info["Target File Access Time"] = t_access_time[0]['Target File Access Time']
        info['TimeZone'] = t_access_time[0]['TimeZone']
        t_write_time = self.write_time()
        info['Target File Write Time'] = t_write_time[0]['Target File Write Time']
        info['TimeZone'] = t_write_time[0]['TimeZone']
        l_creation_time = self.lnk_creation_time()
        info['Link File Creation Time'] = l_creation_time[0]['Link File Creation Time']
        info['TimeZone'] = l_creation_time[0]['TimeZone']
        l_access_time = self.lnk_access_time()
        info['Link File Last Access Time'] = l_access_time[0]['Link File Last Access Time']
        info['TimeZone'] = l_access_time[0]['TimeZone']
        l_write_time = self.lnk_write_time()
        info['Link File Write Time'] = l_write_time[0]['Link File Write Time']
        info['TimeZone'] = l_write_time[0]['TimeZone']
        info['Target File Size'] = self.file_size()[0]['Target File Size']
        info["IconIndex"] = self.iconindex()[0]['IconIndex']
        info["Show Command"] = self.show_command()[0]['Show Command']
        volume = self.volume()
        count = 0
        for i in range(0, len(file_attribute)):
            info["Drivetype" + str(i)] = volume[i]['Drivetype']
            count += 1
        info["Driveserialnumber"] = volume[count]['Driveserialnumber']
        info["Volumelable"] = volume[count]['Volumelable']
        localbase = self.localbase_path()
        info['Localbasepath Unicode'] = localbase[0]['Localbasepath Unicode']
        info['Localbasepath'] = localbase[0]['Localbasepath']
        info["NetBios"] = self.netbios()[0]['NetBios']
        machine = self.machine_id()
        info["Droid"] = machine[0]['Droid']
        info["DroidBirth"] = machine[0]['DroidBirth']
        self.cal_hash()
        info['before_sha1'] = self.__hash_value[0]['sha1']
        info['before_md5'] = self.__hash_value[0]['md5']
        info['after_sha1'] = self.__hash_value[1]['sha1']
        info['after_md5'] = self.__hash_value[1]['md5']

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
        info['TimeZone'] = t_creation_time[0]['TimeZone']
        t_access_time = self.access_time()
        info["Target File Access Time"] = t_access_time[0]['Target File Access Time']
        info['TimeZone'] = t_access_time[0]['TimeZone']
        t_write_time = self.write_time()
        info['Target File Write Time'] = t_write_time[0]['Target File Write Time']
        info['TimeZone'] = t_write_time[0]['TimeZone']
        l_creation_time = self.lnk_creation_time()
        info['Link File Creation Time'] = l_creation_time[0]['Link File Creation Time']
        info['TimeZone'] = l_creation_time[0]['TimeZone']
        l_access_time = self.lnk_access_time()
        info['Link File Last Access Time'] = l_access_time[0]['Link File Last Access Time']
        info['TimeZone'] = l_access_time[0]['TimeZone']
        l_write_time = self.lnk_write_time()
        info['Link File Write Time'] = l_write_time[0]['Link File Write Time']
        info['TimeZone'] = l_write_time[0]['TimeZone']
        info['Target File Size'] = self.file_size()[0]['Target File Size']
        info["IconIndex"] = self.iconindex()[0]['IconIndex']
        info["Show Command"] = self.show_command()[0]['Show Command']
        volume = self.volume()
        count = 0
        for i in range(0, len(file_attribute)):
            info["Drivetype" + str(i)] = volume[i]['Drivetype']
            count += 1
        info["Driveserialnumber"] = volume[count]['Driveserialnumber']
        info["Volumelable"] = volume[count]['Volumelable']
        localbase = self.localbase_path()
        info['Localbasepath Unicode'] = localbase[0]['Localbasepath Unicode']
        info['Localbasepath'] = localbase[0]['Localbasepath']
        info["NetBios"] = self.netbios()[0]['NetBios']
        machine = self.machine_id()
        info["Droid"] = machine[0]['Droid']
        info["DroidBirth"] = machine[0]['DroidBirth']
        self.cal_hash()
        info['before_sha1'] = self.__hash_value[0]['sha1']
        info['before_md5'] = self.__hash_value[0]['md5']
        info['after_sha1'] = self.__hash_value[1]['sha1']
        info['after_md5'] = self.__hash_value[1]['md5']

        info_list.append(info)
        return info_list

def convert_time(time):
    time = '%016x' % time
    time = int(time, 16) / 10.
    time = datetime(1601, 1, 1) + timedelta(microseconds=time) + timedelta(hours=9)
    return time        
