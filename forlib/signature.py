from forlib import decompress
import os

signatures = [{
     'file_extension': 'Zip archive data',
     'hex': ['0x50', '0x4b', '0x3', '0x4'],
     'len': 4,
     'offset': 0},
    {
    'file_extension': 'JPEG image data',
    'hex': ['0xff', '0xd8', '0xff', '0xe0'],
    'len': 4,
    'offset': 0},
    {
    'file_extension': 'JPEG image data',
    'hex': ['0xff', '0xd8', '0xff', '0xe1'],
    'len': 4,
    'offset': 0},
    {
    'file_extension': 'JPEG image data',
    'hex': ['0xff', '0xd8', '0xff', '0xe8'],
    'len': 4,
    'offset': 0},
    {
    'file_extension': 'gif',
    'hex': ['0x47', '0x49', '0x46', '0x38', '0x37', '0x61'],
    'len': 6,
    'offset': 0},
    {
    'file_extension': 'gif',
    'hex': ['0x47', '0x49', '0x46', '0x38', '0x39', '0x61'],
    'len': 6,
    'offset': 0},
    {
    'file_extension': 'MS Windows shortcut',
    'hex': ['0x4c', '0x0', '0x0', '0x0', '0x01', '0x14', '0x02', '0x0'],
    'len': 8,
    'offset': 0},
    {
    'file_extension': 'MS Windows Vista Event Log',
    'hex': ['0x45', '0x6c', '0x66', '0x46', '0x69', '0x6c', '0x65', '0x0'],
    'len': 8,
    'offset': 0},
    {
    'file_extension': 'regf',
    'hex': ['0x72', '0x65', '0x67', '0x66'],
    'len': 4,
    'offset': 0},
    {
    'file_extension': 'prefetch',
    'hex': ['0x53', '0x43', '0x43', '0x41'],
    'len': 4,
    'offset': 4},
    {
    'file_extension': 'recycle_i',
    'hex': ['0x1', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0'],
    'len': 8,
    'offset': 0},
    {
    'file_extension': 'recycle_i',
    'hex': ['0x2', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0'],
    'len': 8,
    'offset': 0},
    {
    'file_extension': 'MAM',#magic : data
    'hex': ['0x4d', '0x41', '0x4d'],
    'len': 3,
    'offset': 0},
    {
        'file_extension': 'Thumb_Icon', 
        'hex': ['0x43', '0x4d', '0x4d', '0x4d'],
        'len': 4,
        'offset': 0},
    {
        'file_extension': 'Icon', 
        'hex': ['0x57', '0x69', '0x6e', '0x34'],
        'len': 4,
        'offset': 4},
    {
        'file_extension': 'LogFile',
        'hex': ['0x52', '0x53', '0x54', '0x52'],
        'len': 4,
        'offset': 0
    },
    {
        'file_extension': 'MFT',
        'hex': ['0x46', '0x49', '0x4C', '0x45'],
        'len': 4,
        'offset': 0
    },
    {
        'file_extension': 'Bitmap image',
        'hex': ['0x42', '0x4D'],
        'len': 2,
        'offset': 0},
    {
        'file_extension': 'bzip2 archive',
        'hex': ['0x42', '0x5A', '0x68'],
        'len': 3,
        'offset': 0},
    {
        'file_extension': 'EnCase case file',
        'hex': ['0x5F', '0x43', '0x41', '0x53', '0x45', '0x5F'],
        'len': 6,
        'offset': 0},
    {
        'file_extension': 'PDF document',
        'hex': ['0x25', '0x50', '0x44', '0x46'],
        'len': 4,
        'offset': 0},
     {
        'file_extension': 'Data',
        'hex': ['0xd0', '0xcf', '0x11', '0xe0', '0xa1', '0xb1', '0x1a', '0xe1'],
        'len': 8,
        'offset': 0},
    # {
    #     'file_extension': 'Windows executable file',
    #     'hex': ['0xE8'],
    #     'len': 1,
    #     'offset': 0},
    # {
    #     'file_extension': 'Windows executable file',
    #     'hex': ['0xE9'],
    #     'len': 1,
    #     'offset': 0},
    # {
    #     'file_extension': 'Windows executable file',
    #     'hex': ['0xEB'],
    #     'len': 1,
    #     'offset': 0},
    # {
    #     'file_extension': 'EXE file',
    #     'hex': ['0x4D', '0x5A'],
    #     'len': 2,
    #     'offset': 0},
    # {
    #     'file_extension': 'MSWorks DB file',
    #     'hex': ['0xD0', '0xCF', '0x11', '0xE0', '0xA1', '0xB1', '0x1A', '0xE1'],
    #     'len': 8,
    #     'offset': 0},
    # {
    #     'file_extension': 'DLL file',
    #     'hex': ['0x4D', '0x5A'],
    #     'len': 2,
    #     'offset': 0},
    # {
    #     'file_extension': 'Windows dump file',
    #     'hex': ['0x4D', '0x44', '0x4D', '0x50', '0x93', '0xA7'],
    #     'len': 6,
    #     'offset': 0},
    # {
    #     'file_extension': 'docx file',
    #     'hex': ['0x50', '0x4B', '0x3', '0x4'],
    #     'len': 4,
    #     'offset': 0},
    # {
    #     'file_extension': 'Windows memory dump',
    #     'hex': ['0x50', '0x41', '0x47', '0x45', '0x44', '0x55'],
    #     'len': 6,
    #     'offset': 0},
    # {
    #     'file_extension': 'doc file',
    #     'hex': ['0xDB', '0xA5', '0x2D', '0x0'],
    #     'len': 4,
    #     'offset': 0},
    # {
    #     'file_extension': 'docx file',
    #     'hex': ['0x50', '0x4B', '0x3', '0x4', '0x14', '0x0', '0x6', '0x0'],
    #     'len': 8,
    #     'offset': 0}
]


def sig_check(path):
    with open(path, "rb") as f:
        header = f.read(32)
    for sig in signatures:
        for i in range(0, sig['len']):
            if sig['hex'][i] != hex(header[sig['offset']+i]):
                break
            elif i == sig['len']-1:
                if sig['file_extension'] == 'MAM':
                    path = prefetch(path, f)
                    extension = sig_check(path)
                    return extension

                return sig['file_extension']
    return -1


def prefetch(path, f):
    f.close()
    decompressed = decompress.decompress(path)

    dirname = os.path.dirname(path)
    basename = os.path.basename(path)
    base = os.path.splitext(basename)
    basename = base[0]
    exetension = base[-1]
            
    prefetch_file = open(dirname+'\\'+basename+'-1'+exetension, 'wb')
    prefetch_file.write(decompressed)
    prefetch_file.close()

    return dirname+'\\'+basename+'-1'+exetension
