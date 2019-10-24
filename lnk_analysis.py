from datetime import datetime,timedelta
import struct
from bitstring import BitArray
import binascii

class Lnk:

    global file
         
def file_open(path):
    global file
    file = open(path,'rb')

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
    
    for count, items in enumerate(attrib_to_parse):
        if int(items) == 1:
            print ('attrib: '+format(attrib[count]))
        else:
            continue

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

def parse_time(time):
    time = '%016x' %time
    time = int(time,16)/10.
    time =  datetime(1601, 1, 1) + timedelta(microseconds=time)+timedelta(hours=9)  
    print(time)

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
    parse_time(c_time)


def access_time():
    global file
    file.seek(36)
    a_time = file.read(8)
    a_time = struct.unpack_from('<q', a_time)[0]
    print(a_time)
    parse_time(a_time)

def write_time():
    global file
    file.seek(44)
    w_time = file.read(8)
    w_time = struct.unpack('<q', w_time)[0]
    print(w_time)
    parse_time(w_time)


def file_size():
    global file
    file.seek(52)
    file_size = struct.unpack('<l', file.read(4))[0]
    print('file_size : '+str(file_size)+'bytes')

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


def linkinfo_off():
    global file
    file.seek(76)
    items_hex = file.read(2)
    b = (b'\x00\x00')
    items_hex  = items_hex + b
    idlistsize = struct.unpack('<i', items_hex)[0]
    list_end = 78+idlistsize
    return list_end

def extra():
    global file
    info_off = linkinfo_off()

    file.seek(info_off)
    link_info_size= struct.unpack('<l', file.read(4))[0]

def volume():
    global file
    info_off = linkinfo_off()
    vol_off = info_off + 12
    file.seek(vol_off)
    volumeid_off = struct.unpack('<l', file.read(4))[0]

    volumeid_off = volumeid_off + info_off
    file.seek(volumeid_off)

    vol_size = struct.unpack('<i', file.read(4))[0]
    print(vol_size)
    
    drive_type = struct.unpack('<i', file.read(4))[0]
    drive_type_list(drive_type)

    driveserialnumber = struct.unpack('<l', file.read(4))[0]
    print('driveserialnumber'+str(driveserialnumber))
   
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
    info_off = linkinfo_off()
    loc_off = info_off + 16
    file.seek(loc_off)
    loc_off = struct.unpack('<l', file.read(4))[0]
    loc_off = loc_off + info_off
    file.seek(loc_off)
    temp = file.read(100)
    temp = temp.decode('utf-8')
    path = []
    for i in temp.split('\x00\x00'):
        path.append(i)
    print(path[0])
