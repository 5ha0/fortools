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
    'offset': 0}
    {
    'file_extension': 'prefetch',#magic : data
    'hex': ['0x41', '0x43', '0x43', '0x53'],#0x434353
    'len': 4,
    'offset': 4}
    {
    'file_extension': 'recycle_i',#magic : data
    'hex': ['0x01', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0'],
    'len': 8,
    'offset': 0}
    
    
]


def sig_check(path):
    with open(path, "rb") as f:
        header = f.read(32)

    for sig in signatures:
        for i in range(0, sig['len']):
            if sig['hex'][i] != hex(header[sig['offset']+i]):
                break
            return sig['file_extension']
