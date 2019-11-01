from datetime import datetime,timedelta
import struct
from bitstring import BitArray
import binascii

class Lnk:

    global file
    global lnk_flag
    global locbase_path_uni
    global start_off
    global info_size
    global info_flag
    global extra_off
    global extra_data
    
def file_open(path):
    global file
    file = open(path,'rb')
    file.seek(4)
    check = file.read(16)
##    if check!= '\x01\x14\x02\x00\x00\x00\x00\x00\xc0\x00\x00\x00\x00\x00\x00F':
##        print('this kind of lnk file do not analysis')
##        return 0
    return file

def link_flag(flags_to_parse):
    global lnk_flag
    
    flags = { 0: "HasLinkTargetIDList",
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
             26: "KeepLocalIDListForUNCTarget"}

    lnk_flag = []
    for count, items in enumerate(flags_to_parse):
        if int(items) == 1:
            print ('Link flag : '+format(flags[count]))
            lnk_flag.append(format(flags[count]))
        else:
            continue

    return lnk_flag
        
def lnk_attrib(attrib_to_parse):
    
    attrib = { 0: "FILE_ATTRIBUTE_READONLY",
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
              14: "FILE_ATTRIBUTE_ENCRYPTED" }

    lnk_attributes = []
    for count, items in enumerate(attrib_to_parse):
        if int(items) == 1:
            print ('attrib: '+format(attrib[count]))
            lnk_attributes.append(format(attrib[count]))
        else:
            continue
                          
    return lnk_attributes

def drive_type_list(drive):
    drive_type = {
        0: 'DRIVE_UNKNOWN',
        1: 'DRIVE_NO_ROOT_DIR',
        2: 'DRIVE_REMOVABLE',
        3: 'DRIVE_FIXED',
        4: 'DRIVE_REMOTE',
        5: 'DRIVE_CDROM',
        6: 'DRIVE_RAMDISK'
        }
    
    if drive != 0:
        print ('drive_type: '+format(drive_type[drive]))
    else:
        return none

def convert_time(time):
    time = '%016x' %time
    time = int(time,16)/10.
    time =  datetime(1601, 1, 1) + timedelta(microseconds=time)+timedelta(hours=9)  
    print(time)

## has link target id list has link info -- linkinfo flags
def link_flags():
    global file
    file.seek(20)
    flags = struct.unpack('<i', file.read(4))
    file_flags = BitArray(hex(flags[0]))
    link_flag(file_flags.bin)
    
def file_attribute():
    global file
    file.seek(24)
    attributes = struct.unpack('<i', file.read(4))
    flag_atributes = BitArray(hex(attributes[0]))
    lnk_attrib(flag_atributes.bin)

def creation_time():
    global file
    file.seek(28)
    c_time = file.read(8)
    c_time = struct.unpack('<q', c_time)
    print(c_time)
    convert_time(c_time)


def access_time():
    global file
    file.seek(36)
    a_time = file.read(8)
    a_time = struct.unpack_from('<q', a_time)[0]
    print(a_time)
    convert_time(a_time)

def write_time():
    global file
    file.seek(44)
    w_time = file.read(8)
    w_time = struct.unpack('<q', w_time)[0]
    print(w_time)
    convert_time(w_time)


def file_size():
    global file
    file.seek(52)
    file_size = struct.unpack('<l', file.read(4))[0]
    print('targrt_file_size : '+str(file_size)+'bytes')

def iconindex():
    global file
    file.seek(56)
    iconindex = struct.unpack('<l', file.read(4))[0]
    print('iconindex : '+ str(iconindex))


def show_command():
    global file
    file.seek(60)
    showcomand = struct.unpack('<i', file.read(4))[0]
    showcomand = hex(showcomand)
    if showcomand == hex(0x1):
        print ('SW_SHOWNORMAL')
    elif showcomand == hex(0x3):
        print ('SW_SHOWMAXIMIZED') 
    elif showcomand == hex(0x7):
        print ('SW_SHOWMINNOACTIVE') 
    else:
        print ('SW_SHOWNORMAL(default)')
        
############################################

def linkinfo_off():
    global file
    global start_off
    global info_size
    global lnk_flag
    global locbase_path_uni
    global info_flag
    
    link_flags()
    
    if 'HasLinkInfo' not in lnk_flag:
        return print('this file does not have link info')
    if 'HasLinkTargetIDList' not in lnk_flag:
        start_off = 76
    else:    
        file.seek(76)
        items_hex = file.read(2)
        b = (b'\x00\x00')
        items_hex  = items_hex + b
        idlistsize = struct.unpack('<i', items_hex)[0]
        start_off = 78+idlistsize

    file.seek(start_off)
    info_size = struct.unpack('<i', file.read(4))[0]
    info_header_size = struct.unpack('<i', file.read(4))[0]
    if info_header_size == '\x00\x00\x00\x1C':
        info_option = 'False'
    else:
        info_option = 'True'              
##생각하기 24보다 작으면 어쩔? 에러지 뭐
    info_flag = file.read(4)
    if info_flag == '\x00\x00\x00\x01':
        info_flag = 'A'
        volume = 'True'
        locbase_path = 'True'
        net = None
        if info_option == 'True':
            locbase_path_uni ='True'
        else:
            locbase_path_uni = None 
    else:
        info_flag = 'B'
        volume = None
        locbase_path = None
        net = 'True'
        locbase_path_uni = None
    

def volume():
    global file
    global info_flag
    global start_off
                          
    linkinfo_off()
    print(info_flag)                      
    if info_flag != 'A':
        return print('do not have volumeid')
                          
    vol_off = start_off + 12
    file.seek(vol_off)
    volumeid_off = struct.unpack('<l', file.read(4))[0]

    volumeid_off = volumeid_off + start_off
    file.seek(volumeid_off)

    vol_size = struct.unpack('<i', file.read(4))[0]
    print(vol_size)
    
    drive_type = struct.unpack('<i', file.read(4))[0]
    drive_type_list(drive_type)

    driveserialnumber = struct.unpack('<l', file.read(4))[0]
    print('driveserialnumber: '+str(driveserialnumber))
   
    volumelable_off = file.read(4)
    if volumelable_off != '0x00000014':
        volumelable_off = struct.unpack('<l', volumelable_off)[0]
        vol_lable_off = volumelable_off
        volumelable_off = volumeid_off + volumelable_off
    else:
        volumelable_off_uni = struct.unpack('<l', file.read(4))[0]
        vol_lable_off = volumelable_off_uni
        volumelable_off = volumeid_off + volumelable_off_uni
    file.seek(volumelable_off)
    volumelable_size = vol_size - vol_lable_off
    volumelable = file.read(volumelable_size)
    volumelable = volumelable.decode('cp1252')
    print('volumelable: ' + volumelable)

def localbase_path():
    global file
    global info_flag
    global start_off
    global locbase_path_uni
    
    linkinfo_off()
                          
    if info_flag != 'A':
        return print('do not have locabasepath, locabasepathunicode')
    elif locbase_path_uni != 'True':
        print('locbasepathoffsetunicode : 0\n locbasepathunicode : do not know')
    else:
        locbase_path_off_uni = start_off + 28
        file.seek(locbase_path_off_uni)
        locbase_path_off_uni = struct.unpack('<l', file.read(4))[0]
        locbase_path_uni = locbase_path_off_uni + start_off
        file.seek(locbase_path_uni)
        locbase_path_uni = file.read(100)
        locbase_path_uni = locbase_path_uni.decode('utf-8')
        locbase_path_uni = []
        for i in locbase_path_uni.split('\x00\x00'):
            locbase_path_uni.append(i)
        print('localbasepathunicode: ' + locbase_path_uni[0])

    locbasepath_off = start_off + 16
    file.seek(locbasepath_off)
    locbasepath_off = struct.unpack('<l', file.read(4))[0]
    locbasepath_off = locbasepath_off + start_off
                          
    file.seek(locbasepath_off)
    locbasepath = file.read(100)
    locbasepath = locbasepath.decode('utf-8')
    locbasepath = []
    for i in locbasepath.split('\x00\x00'):
        locbasepath.append(i)
    print('localbasepath: ' + locbasepath[0])

############################################
    
def extradata():
    global file
    global start_off
    global info_size
    global lnk_flag
    global extra_off
    global extra_data
    
    linkinfo_off()
    
    string_off = start_off + info_size
    
    if 'HasName' in lnk_flag:
        file.seek(string_off)
        string_size = file.read(2)
        b = (b'\x00\x00')
        string_size  = string_size + b
        string_size = struct.unpack('<i', string_size)[0]
        string_off = string_size + string_off + 2
    elif 'HasRelativePath' in lnk_flag:
        file.seek(string_off)
        string_size = file.read(2)
        b = (b'\x00\x00')
        string_size  = string_size + b
        string_size = struct.unpack('<i', string_size)[0]
        string_off = string_size + string_off + 2
##        relative_path = str(file.read(string_size))
##        relative_path = relative_path.replace('\x00','').encode('utf-8', 'ignore').decode('utf-8')
    elif 'HasWorkingDir' in lnk_flag:
        file.seek(string_off)
        string_size = file.read(2)
        b = (b'\x00\x00')
        string_size  = string_size + b
        string_size = struct.unpack('<i', string_size)[0]
        string_off = string_size + string_off + 2
    elif 'HasArguments' in lnk_flag:
        file.seek(string_off)
        string_size = file.read(2)
        b = (b'\x00\x00')
        string_size  = string_size + b
        string_size = struct.unpack('<i', string_size)[0]
        string_off = string_size + string_off + 2
    elif 'HasIconLocation' in lnk_flag:
        file.seek(string_off)
        string_size = file.read(2)
        b = (b'\x00\x00')
        string_size  = string_size + b
        string_size = struct.unpack('<i', string_size)[0]
        string_off = string_size + string_off + 2
        
    extra_off = string_off
    block_signature = extra_off + 4
    file.seek(block_signature)
    block_signature = file.read(4)
    if block_signature == '\xA0\x00\x00\x03':
        extra_data = 'True'
    else:
        extra_data = None

def netbios():
    global file
    global extra_data
    global extra_off
    extradata()
    if extra_data != 'True':
        return print('not have extra data')
    netbios = string_off + 16
    file.seek(netbios)
    netbios = str(file.read(16))
    netbios = netbios.replace('\x00','').encode('utf-8', 'ignore').decode('utf-8')
    print('netbios: ' + str(netbios))

def machine_id():
    global file
    global extra_data
    global extra_off
    extradata()
    if extra_data != 'True':
        return print('not have extra data')
    netbios = string_off + 32
    file.seek(netbios)
    droid = str(file.read(32))
    droid = droid.replace('\x00','').encode('utf-8', 'ignore').decode('utf-8')
    print('droid' + str(droid))
    droidbirth = str(file.read(32))
    droidbirth = droidbirth.replace('\x00','').encode('utf-8', 'ignore').decode('utf-8')
    print('droidbirth' + str(droidbirth))
    
        
    
    
##def favorite():
##    timestamp
##    volume
##    netbios
##    
