from datetime import datetime, timedelta
import struct
from bitstring import BitArray
import os
import json
import forlib.calc_hash as calc_hash
import binascii


class LnkAnalysis:

    def __init__(self, file, path, hash_v):
        self.__file = file
        self.__path = path
        self.__hash_value = [hash_v]
        self.__lnk_flags_value = []
        self.__locbase_path_uni_off = None
        self.__start_off = None
        self.__info_size = None
        self.__info_flag = 'False'
        self.__extra_off = None
        self.__extra_data = 'False'
        self.__linkinfo_flag = self.__link_flags()
        self.__lnk_json = self.__make_json()
        self.__cal_hash()
        self.__has_info_flag = 'False'

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
                self.__lnk_flags_value.append(format(flags[count]))
            else:
                continue
        return self.__lnk_flags_value

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

    def __net_flag(self, netflag):
        attrib = {0: "A",
                  1: "B"
                  }

        lnk_attributes = []
        netflag = netflag[::-1]
        for count, items in enumerate(netflag):
            if int(items) == 1:
                lnk_attributes.append(format(attrib[count]))
            else:
                continue

        return lnk_attributes

    def __net_type(self, nettype):
        if nettype == '001A0000':
            return "WNNC_NET_AVID"
        if nettype == '001B0000':
            return "WNNC_NET_DOCUSPACE"
        if nettype == '001C0000':
            return "WNNC_NET_MANGOSOFT"
        if nettype == '001D0000':
            return "WNNC_NET_SERNET"
        if nettype == '001E0000':
            return "WNNC_NET_RIVERFRONT1"
        if nettype == '001F0000':
            return "WNNC_NET_RIVERFRONT2"
        if nettype == '00200000':
            return "WNNC_NET_DECORB"
        if nettype == '00210000':
            return "WNNC_NET_PROTSTOR"
        if nettype == '00220000':
            return "WNNC_NET_FJ_REDIR"
        if nettype == '00230000':
            return "WNNC_NET_DISTINCT"
        if nettype == '00240000':
            return "WNNC_NET_TWINS"
        if nettype == '00250000':
            return "WNNC_NET_RDR2SAMPLE"
        if nettype == '00260000':
            return "WNNC_NET_CSC"
        if nettype == '00270000':
            return "WNNC_NET_3IN1"
        if nettype == '00290000':
            return "WNNC_NET_EXTENDNET"
        if nettype == '002A0000':
            return "WNNC_NET_STAC"
        if nettype == '002B0000':
            return "WNNC_NET_FOXBAT"
        if nettype == '002C0000':
            return "WNNC_NET_YAHOO"
        if nettype == '002D0000':
            return "WNNC_NET_EXIFS"
        if nettype == '002E0000':
            return "WNNC_NET_DAV"
        if nettype == '002F0000':
            return "WNNC_NET_KNOWARE"
        if nettype == '00300000':
            return "WNNC_NET_OBJECT_DIRE"
        if nettype == '00310000':
            return "WNNC_NET_MASFAX"
        if nettype == '00320000':
            return "WNNC_NET_HOB_NFS"
        if nettype == '00330000':
            return "WNNC_NET_SHIVA"
        if nettype == '00340000':
            return "WNNC_NET_IBMAL"
        if nettype == '00350000':
            return "WNNC_NET_LOCK"
        if nettype == '00360000':
            return "WNNC_NET_TERMSRV"
        if nettype == '00370000':
            return "WNNC_NET_SRT"
        if nettype == '00380000':
            return "WNNC_NET_QUINCY"
        if nettype == '00390000':
            return "WNNC_NET_OPENAFS"
        if nettype == '003A0000':
            return "WNNC_NET_AVID1"
        if nettype == '003B0000':
            return "WNNC_NET_DFS"
        if nettype == '003C0000':
            return "WNNC_NET_KWNP"
        if nettype == '003D0000':
            return "WNNC_NET_ZENWORKS"
        if nettype == '003E0000':
            return "WNNC_NET_DRIVEONWEB"
        if nettype == '003F0000':
            return "WNNC_NET_VMWARE"
        if nettype == '00400000':
            return "WNNC_NET_RSFX"
        if nettype == '00410000':
            return "WNNC_NET_MFILES"
        if nettype == '00420000':
            return "WNNC_NET_MS_NFS"
        if nettype == '00430000':
            return "WNNC_NET_GOOGLE"

        return "UNKNOWN"



    ################ Shell_Link_Header #############################

    # show link flag
    def __link_flags(self):
        self.__file.seek(20)
        flags = struct.unpack('<i', self.__file.read(4))
        file_flags = BitArray(hex(flags[0]))
        self.__lnk_flag(file_flags.bin)

    def __file_attribute(self):
        self.__file.seek(24)
        attributes = struct.unpack('<i', self.__file.read(4))
        flag_atributes = BitArray(hex(attributes[0]))
        flag_atributes = self.__lnk_attrib(flag_atributes.bin)

        lnk_list = []
        for i in range(0, len(flag_atributes)):
            lnk_obj = {"File Attributes": flag_atributes[i]}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)

        return lnk_list

    # Target File time
    def __creation_time(self):
        self.__file.seek(28)
        c_time = self.__file.read(8)
        c_time = struct.unpack('<q', c_time)
        c_time = convert_time(c_time)
        c_time = c_time.strftime("%Y-%m-%d %H:%M:%S")

        lnk_list = []
        lnk_obj = {'Target File Creation Time': c_time,
                   'TimeZone': 'UTC'}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    def __access_time(self):
        self.__file.seek(36)
        a_time = self.__file.read(8)
        a_time = struct.unpack_from('<q', a_time)[0]
        a_time = convert_time(a_time)
        a_time = a_time.strftime("%Y-%m-%d %H:%M:%S")

        lnk_list = []
        lnk_obj = {'Target File Access Time': str(a_time),
                   "TimeZone": 'UTC'}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    def __write_time(self):
        self.__file.seek(44)
        w_time = self.__file.read(8)
        w_time = struct.unpack('<q', w_time)[0]
        w_time = convert_time(w_time)
        w_time = w_time.strftime("%Y-%m-%d %H:%M:%S")

        lnk_list = []
        lnk_obj = {'Target File Write Time': str(w_time),
                   "TimeZone": 'UTC'}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    # Link file Time

    def __lnk_creation_time(self):
        c_time = datetime.fromtimestamp(os.path.getctime(self.__path))
        c_time = c_time.strftime("%Y-%m-%d %H:%M:%S")

        lnk_list = []
        lnk_obj = {'Link File Creation Time': str(c_time),
                   "TimeZone": 'SYSTEM TIME'}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    def __lnk_access_time(self):
        a_time = datetime.fromtimestamp(os.path.getatime(self.__path))
        a_time = a_time.strftime("%Y-%m-%d %H:%M:%S")

        lnk_list = []
        lnk_obj = {'Link File Last Access Time': str(a_time),
                   "TimeZone": 'SYSTEM TIME'}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    def __lnk_write_time(self):
        w_time = datetime.fromtimestamp(os.path.getmtime(self.__path))
        w_time = w_time.strftime("%Y-%m-%d %H:%M:%S")

        lnk_list = []
        lnk_obj = {'Link File Write Time': str(w_time),
                   "TimeZone": 'SYSTEM TIME'}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    def __file_size(self):
        self.__file.seek(52)
        file_size = struct.unpack('<l', self.__file.read(4))[0]

        lnk_list = []
        lnk_obj = {'Target File Size': str(file_size) + 'bytes'}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    def __iconindex(self):
        self.__file.seek(56)
        iconindex = struct.unpack('<l', self.__file.read(4))[0]

        lnk_list = []
        lnk_obj = {'IconIndex': str(iconindex)}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    def __show_command(self):
        self.__file.seek(60)
        showcomand = struct.unpack('<i', self.__file.read(4))[0]
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
        self.__start_off = 76

        if 'HasLinkTargetIDList' not in self.__lnk_flags_value:
            self.__start_off = 76
        else:
            self.__file.seek(76)
            items_hex = self.__file.read(2)
            b = bytes(b'\x00\x00')
            items_hex = items_hex + b
            idlistsize = struct.unpack('<i', items_hex)[0]
            self.__start_off = 78 + idlistsize

        if 'HasLinkInfo' not in self.__lnk_flags_value:
            self.__linkinfo_flag = 'False'
            #Input the value to use on the __extradata() below
            self.__info_size = 0
            return 0
        else:
            self.__linkinfo_flag = 'True'

        self.__file.seek(self.__start_off)
        self.__info_size = struct.unpack('<i', self.__file.read(4))[0]
        info_header_size = struct.unpack('<i', self.__file.read(4))[0]
        # info_optional is express localbasepathoffsetunicode and commonpathsuffixoffsetunicode
        if info_header_size == 28:
            info_optional = 'not set'
        elif info_header_size >= 36:
            info_optional = 'set'
        self.__info_flag = self.__file.read(4)
        if self.__info_flag == bytes(b'\x01\x00\x00\x00'):
            self.__info_flag = 'A'
            # volume_id = 'present'
            # local_base_path = 'present'
            if info_optional == 'set':
                self.__locbase_path_uni_off = 'set'
            else:
                self.__locbase_path_uni_off = 'None'
        else:
            self.__info_flag = 'B'
            # volume = None
            # locbase_path = None
            if info_optional == 'set':
                self.__locbase_path_uni_off = '0'
            else:
                self.__locbase_path_uni_off = 'None'

        return 0

    def __volume(self):
        lnk_list = []

        self.__lnkinfo_off()

        if self.__linkinfo_flag != 'True':
            lnk_obj1 = {'Drivetype': 'None',
                        'Driveserialnumber': 'None',
                        'Volumelable': 'None'}
            json.dumps(lnk_obj1)
            lnk_list.append(lnk_obj1)

            return lnk_list

        elif self.__info_flag != 'A':
            lnk_obj = {'Drivetype': 'None',
                       'Driveserialnumber': 'None',
                       'Volumelable': 'None'}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)

            return lnk_list


        vol_off = self.__start_off + 12
        self.__file.seek(vol_off)
        volumeid_off = struct.unpack('<i', self.__file.read(4))[0]

        volumeid_off = volumeid_off + self.__start_off
        self.__file.seek(volumeid_off)

        vol_size = struct.unpack('<i', self.__file.read(4))[0]

        drive_type = struct.unpack('<i', self.__file.read(4))[0]
        drive_type = self.__drive_type_list(drive_type)

        driveserialnumber = self.__file.read(4)
        driveserialnumber = bytes.decode(binascii.hexlify(driveserialnumber))

        volumelable_off = self.__file.read(4)
        if volumelable_off == bytes(b'\x10\x00\x00\x00'):
            volumelable_off = struct.unpack('<i', volumelable_off)[0]
            volumelable_off = volumeid_off + volumelable_off
        else:
            volumelable_off_uni = struct.unpack('<i', self.__file.read(4))[0]
            volumelable_off = volumeid_off + volumelable_off_uni

        self.__file.seek(volumelable_off)
        end = vol_size + volumeid_off
        volumelable_size = end - volumelable_off
        volumelable = self.__file.read(volumelable_size)
        volumelable = volumelable.decode('utf-8', 'ignore')
        volumelable = volumelable.replace('\x00', '')

        lnk_obj = {'Drivetype': drive_type,
                   'Driveserialnumber': str(driveserialnumber),
                   'Volumelable': volumelable}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list


    def __localbase_path(self):
        lnk_list = []

        self.__lnkinfo_off()

        if self.__linkinfo_flag != 'True':
            lnk_obj = {'Localbasepath Unicode': 'None',
                       'Localbasepath': 'None'}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)

            return lnk_list
        elif self.__info_flag != 'A':

            lnk_obj = {'Localbasepath Unicode': self.__locbase_path_uni_off,
                       'Localbasepath': 'None'}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)

            return lnk_list

        elif self.__locbase_path_uni_off == 'set':
            locbase_path_off_uni = self.__start_off + 28
            self.__file.seek(locbase_path_off_uni)
            locbase_path_off_uni = struct.unpack('<l', self.__file.read(4))[0]
            com_path_off_uni = struct.unpack('<l', self.__file.read(4))[0]
            locbase_path_off_uni = locbase_path_off_uni + self.__start_off
            com_path_off_uni = com_path_off_uni + self.__start_off

            self.__file.seek(locbase_path_off_uni)
            read_info_size = com_path_off_uni - locbase_path_off_uni
            self.__locbase_path_uni_off = self.__file.read(read_info_size)
            self.__locbase_path_uni_off.split(bytes(b'\x00\x00'))
            self.__locbase_path_uni_off = self.locbase_path_uni.decode('utf-8', 'ignore')
            self.__locbase_path_uni_off = self.__locbase_path_uni_off.replace('\x00', '')

        locbasepath_off = self.__start_off + 16
        self.__file.seek(locbasepath_off)
        locbasepath_off = struct.unpack('<l', self.__file.read(4))[0]
        end = self.__start_off + 24
        self.__file.seek(end)
        end = struct.unpack('<l', self.__file.read(4))[0]
        end = end + self.__start_off
        locbasepath_off = locbasepath_off + self.__start_off

        self.__file.seek(locbasepath_off)
        read_info_size = end - locbasepath_off
        locbasepath = self.__file.read(read_info_size)
        locbasepath = locbasepath.decode('utf-8', 'ignore')
        locbasepath = locbasepath.replace('\x00', '')

        lnk_obj = {'Localbasepath Unicode': self.__locbase_path_uni_off,
                   'Localbasepath': locbasepath}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    def __common_network_relative_link(self):
        lnk_list = []

        self.__lnkinfo_off()

        if self.__linkinfo_flag != 'True':
            lnk_obj = {'NetName': 'None',
                       'DeviceName': 'None',
                       'NetworkProviderType': 'None'}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)

            return lnk_list
        elif self.__info_flag != 'B':
            lnk_obj = {'NetName': 'None',
                       'DeviceName': 'None',
                       'NetworkProviderType': 'None'}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)

            return lnk_list

        self.__lnkinfo_off()
        net_off = self.__start_off + 20
        net_off = self.__file.seek(net_off)
        net_off = struct.unpack('<i', self.__file.read(4))[0]

        net_off = self.__start_off + net_off
        self.__file.seek(net_off)
        net_size = struct.unpack('<i', self.__file.read(4))[0]
        net_size = net_off + net_size
        net_flag_info = self.__file.read(4)
        net_flag_info = BitArray(hex(net_flag_info[0]))
        net_flag = self.__net_flag(net_flag_info)

        net_name = struct.unpack('<i', self.__file.read(4))[0]
        if net_name > 20:
            optional = 'True'
        else:
            optional = 'False'
        net_name = net_name + net_off

        device_name = struct.unpack('<i', self.__file.read(4))[0]
        device_name = device_name + net_off

        if 'B' in net_flag:
            net_type = struct.unpack('<i', self.__file.read(4))[0]
            net_type = "%08x" % net_type
            net_type = self.__net_type(net_type)
        else:
            net_type = 'None'

        self.__file.seek(net_name)
        net_name_size = device_name - net_name
        net_name = self.__file.read(net_name_size)
        net_name = net_name.decode('utf8', 'ignore')
        net_name = net_name.replace('\x00', '')

        if optional == 'True':
            name_uni_off = net_off + 20
            name_uni_off = struct.unpack('<i', string_size)[0]
            name_uni_off = net_off + name_uni

            device_uni_off = net_off + 24
            device_uni_off = struct.unpack('<i', string_size)[0]
            device_uni_off = net_off + device_uni_off

            self.__file.seek(name_uni_off)
            name_uni_size = device_uni_off - name_uni_off
            name_uni = self.__file.read(name_uni_size)
            name_uni = name_uni.decode('utf8', 'ignore')
            name_uni = name_uni.replace('\x00', '')

            self.__file.seek(device_uni_off)
            device_uni_off_size = net_size - device_uni_off
            device_uni = self.__file.read(device_uni_off_size)
            device_uni = device_uni.decode('utf8', 'ignore')
            device_uni = device_uni.replace('\x00', '')

            if 'A' in net_flag:
                self.__file.seek(device_name)
                device_name_size = name_uni - device_name_size
                device_name = self.__file.read(device_name_size)
                device_name = device_name.decode('utf8', 'ignore')
                device_name = device_name.replace('\x00', '')
            else:
                device_name = 'None'

        else:
            if 'A' in net_flag:
                self.__file.seek(device_name)
                device_name_size = net_size - device_name
                device_name = self.__file.read(device_name_size)
                device_name = device_name.decode('utf8', 'ignore')
                device_name = device_name.replace('\x00', '')
            else:
                device_name = 'None'

        lnk_obj = {'NetName': net_name,
                   'DeviceName': device_name,
                   'NetworkProviderType': net_type}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    ################ Extra_Data #############################
    def __extradata_size(self, string_off):
        self.__file.seek(string_off)
        string_size = self.__file.read(2)
        b = bytes(b'\x00\x00')
        string_size = string_size + b
        string_size = struct.unpack('<i', string_size)[0]
        string_size = string_size * 2

        # if you want to read string, use this
        # relative_path = self.__file.read(string_size)
        # relative_path = relative_path.decode('utf8', 'ignore')
        # relative_path = relative_path.replace('\x00', '')
        # print(relative_path)

        string_off = string_size + string_off + 2
        return string_off

    def __string_data(self):
        self.__lnkinfo_off()

        string_off = self.__start_off + self.__info_size

        if 'HasName' in self.__lnk_flags_value:
            string_off = self.__extradata_size(string_off)

        if 'HasRelativePath' in self.__lnk_flags_value:
            string_off = self.__extradata_size(string_off)

        if 'HasWorkingDir' in self.__lnk_flags_value:
            string_off = self.__extradata_size(string_off)

        if 'HasArguments' in self.__lnk_flags_value:
            string_off = self.__extradata_size(string_off)

        if 'HasIconLocation' in self.__lnk_flags_value:
            string_off = self.__extradata_size(string_off)

        self.__extra_off = string_off

        self.__extra_data = 'False'

        while(1):
            self.__file.seek(self.__extra_off)
            block_size = struct.unpack('<i', self.__file.read(4))[0]
            if block_size < 4:
                break
            block_signature = self.__file.read(4)
            if block_signature == bytes(b'\x03\x00\x00\xa0'):
                self.__extra_data = 'True'
                break
            else:
                self.__extra_off = self.__extra_off + block_size

    def __netbios(self):
        self.__string_data()

        lnk_list = []

        if self.__extra_data != 'True':
            lnk_obj = {'NetBios': 'None'}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)

            return lnk_list

        machine_id = self.__extra_off + 16
        self.__file.seek(machine_id)
        machine_id = self.__file.read(16)
        netbios = machine_id.decode('utf8', 'ignore')
        netbios = netbios.replace('\x00', '')

        lnk_obj = {'NetBios': str(netbios)}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

    def __droid_value(self):
        self.__string_data()

        lnk_list = []

        if self.__extra_data != 'True':
            print('ExtraData: None')
            lnk_obj = {'Droid': 'None',
                       'DroidBirth': 'None'}
            json.dumps(lnk_obj)
            lnk_list.append(lnk_obj)

            return lnk_list
        droid = self.__extra_off + 32
        self.__file.seek(droid)
        droid = self.__file.read(32)
        droid = bytes.decode(binascii.hexlify(droid))

        droidbirth = self.__file.read(32)
        droidbirth= bytes.decode(binascii.hexlify(droidbirth))


        lnk_obj = {'Droid': str(droid),
                   'DroidBirth': str(droidbirth)}
        json.dumps(lnk_obj)
        lnk_list.append(lnk_obj)

        return lnk_list

################################################################################

    # calculate hash value after parsing
    def __cal_hash(self):
        lnk_list = []
        lnk_obj = dict()
        self.__hash_value.append(calc_hash.get_hash(self.__path))
        lnk_obj['before_sha1'] = self.__hash_value[0]['sha1']
        lnk_obj['before_md5'] = self.__hash_value[0]['md5']
        lnk_obj['after_sha1'] = self.__hash_value[1]['sha1']
        lnk_obj['after_md5'] = self.__hash_value[1]['md5']

        lnk_list.append(lnk_obj)
        self.__hash_value = lnk_list

    def get_hash(self):
        return self.__hash_value
#################################################################################

    def __make_json(self):
        info_list = []
        info = dict()
        file_attribute = self.__file_attribute()
        for i in range(0, len(file_attribute)):
            info["File Attributes"+ str(i)] = file_attribute[i]['File Attributes']
        t_creation_time = self.__creation_time()
        info["Target File Creation Time"] = t_creation_time[0]['Target File Creation Time']
        info['Target File Creation TimeZone'] = t_creation_time[0]['TimeZone']
        t_access_time = self.__access_time()
        info["Target File Access Time"] = t_access_time[0]['Target File Access Time']
        info['Target File Access TimeZone'] = t_access_time[0]['TimeZone']
        t_write_time = self.__write_time()
        info['Target File Write Time'] = t_write_time[0]['Target File Write Time']
        info['Target File Write TimeZone'] = t_write_time[0]['TimeZone']
        l_creation_time = self.__lnk_creation_time()
        info['Link File Creation Time'] = l_creation_time[0]['Link File Creation Time']
        info['Link File Creation TimeZone'] = l_creation_time[0]['TimeZone']
        l_access_time = self.__lnk_access_time()
        info['Link File Last Access Time'] = l_access_time[0]['Link File Last Access Time']
        info['Link File Last Access TimeZone'] = l_access_time[0]['TimeZone']
        l_write_time = self.__lnk_write_time()
        info['Link File Write Time'] = l_write_time[0]['Link File Write Time']
        info['Link File Write TimeZone'] = l_write_time[0]['TimeZone']
        info['Target File Size'] = self.__file_size()[0]['Target File Size']
        info["IconIndex"] = self.__iconindex()[0]['IconIndex']
        info["Show Command"] = self.__show_command()[0]['Show Command']
        volume = self.__volume()
        info['Drivetype'] = volume[0]['Drivetype']
        info["Driveserialnumber"] = volume[0]['Driveserialnumber']
        info["Volumelable"] = volume[0]['Volumelable']
        localbase = self.__localbase_path()
        info['Localbasepath Unicode'] = localbase[0]['Localbasepath Unicode']
        info['Localbasepath'] = localbase[0]['Localbasepath']
        network = self.__common_network_relative_link()
        info['NetName'] = network[0]['NetName']
        info['DeviceName'] = network[0]['DeviceName']
        info['NetworkProviderType'] = network[0]['NetworkProviderType']
        info["NetBios"] = self.__netbios()[0]['NetBios']
        machine = self.__droid_value()
        info["Droid"] = machine[0]['Droid']
        info["DroidBirth"] = machine[0]['DroidBirth']

        info_list.append(info)

        print('HasLinkInfo:' + self.__linkinfo_flag + '/ Tracker Data Block:' + self.__extra_data)

        return info_list

#####################################################################################

    def show_all_info(self):
        for i in range(0, len(self.__lnk_json)):
            print(self.__lnk_json[i])

    def get_all_info(self):
        return self.__lnk_json

    def get_info(self, list):
        result = []
        for i in self.__lnk_json:
            info = dict()
            try:
                for j in list:
                    info[j] = i[j]
                result.append(info)
            except KeyError:
                print("Plz check your key.")
                return -1
        return result

def convert_time(time):
    time = '%016x' % time
    time = int(time, 16) / 10.
    time = datetime(1601, 1, 1) + timedelta(microseconds=time)
    return time        
