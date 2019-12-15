import os
import chardet

def convert_endian(bytesArr, bytesCount, isLittleEndian, str_form):
    if bytesArr == b'' or bytesCount == 0:
        return None

    bytesArray = bytesArr

    if str_form == "unicode":
        bytesArray = bytesArr.decode('utf-16', 'ignore')
    elif str_form == "s":
        bytesArray = bytesArr.decode(chardet.detect(bytesArr)['encoding'])

    listData = list(bytesArray)
    listData = listData[0:len(listData)]

    if isLittleEndian == True:
        listData.reverse()

    tupleData = tuple(listData)
    if str_form == "b":
        num = '%08b'
    elif str_form == "x" or str_form == "d":
        num = '%02X'
    elif str_form == "s" or str_form == "unicode":
        num = '%c'

    fmt = num * len(listData)
    result = fmt % tupleData
    if str_form == "d":
        if len(listData) > 0:
            result = str(int(result, 16))

    return result

def check_signature(path, extension):
    if(type(path) == str) and (os.path.isfile(path) == True):
        size = os.path.getsize(path)
        file = open(path, "rb")
        if size > 40:
            file.seek(0)
            file_header = file.read(20)

            file.seek(-20, 2)
            file_footer = file.read(20)
        elif 10 < size <= 40:
            file.seek(0)
            file_header = file.read(5)

            file.seek(-5, 2)
            file_footer = file.read(5)
        elif 4 < size <= 10:
            file.seek(0)
            file_header = file.read(4)

            file.seek(-4, 2)
            file_footer = file.read(4)
        else:
            file_header = None

        file.close()
    elif (type(path) == bytes) or (type(path) == bytearray):
        size = len(path)
        if size > 40:
            file_header = path[:20]
            file_footer = path[-20:]
        elif 10 < size <= 40:
            file_header = path[:5]
            file_footer = path[-5:]
        elif 4 < size <= 10:
            file_header = path[:4]
            file_footer = path[-4:]
        else:
            file_header = None
    else:
        return False

    if file_header == None:
        return False

    sig_list = [
        {"extension": "jpg",
         "header": [b"\xFF\xD8\xFF\xE0", None, None, b"\x4A\x46\x49\x46"],
         "footer": None},
        {"extension": "jpg",
         "header": [b"\xFF\xD8\xFF\xE1", None, None, b"\x45\x78\x69\x66"],
         "footer": None},
        {"extension": "jpg",
         "header": [b"\xFF\xD8\xFF\xE8", None, None, b"\x53\x50\x49\x46\x46\x00"],
         "footer": None},
        {"extension": "png",
         "header": [b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"],
         "footer": None},
        {"extension": "bmp",
         "header": [b"\x42\x4D"],
         "footer": None},
    ]

    check = False
    for ex in sig_list:
        if ex["extension"] == extension.lower():
            check = False
            file_header_idx = 0
            for h in ex["header"]:
                if h == None:
                    file_header_idx += 1
                    continue

                if file_header_idx + len(h) < len(file_header):
                    idx = file_header[file_header_idx:file_header_idx + len(h)].find(h)
                    if idx != 0:
                        break
                    else:
                        file_header_idx = file_header_idx + idx + len(h)
                        if ex["header"].index(h) == (len(ex["header"]) -1):
                            check = True
                        continue
                else:
                    break

            if check == False:
                continue

            check = False
            file_header_idx = 0
            if ex["footer"] == None:
                check = True
            else:
                for f in ex["footer"]:
                    if f == None:
                        file_header_idx += 1
                        continue

                    if file_header_idx + len(f) < len(file_header):
                        idx = file_header[file_header_idx:file_header_idx + len(f)].find(f)
                        if idx != 0:
                            break
                        else:
                            file_header_idx = file_header_idx + idx + len(f)
                            if ex["footer"].index(f) == len(f):
                                check = True
                            continue
                    else:
                        break
            if check == True:
                break
    return check

def find_signature(path, start_offset = 0, in_chunk_size = 32768, signature = b''):
    if os.path.isfile(path) == False:
        return -1

    size = os.path.getsize(path)
    if size < start_offset:
        return -1
    else:
        start_offset = start_offset

    if size < in_chunk_size:
        return -1
    elif in_chunk_size == 0:
        chunk_size = 32768
    else:
        chunk_size = in_chunk_size

    if signature == b'':
        return -1
    else:
        sig = signature

    file = open(path, "rb")
    cur_offset = start_offset
    while True:
        file.seek(cur_offset)
        buf = file.read(chunk_size)

        cur_offset = 0
        size = len(buf)
        if(size > 4) and buf[cur_offset:cur_offset+len(sig)] != sig:
            size -= 1
            cur_offset += 1
        else:
            break

        if size < 4:
            continue
        else:
            cur_offset += start_offset
            break

    file.close()
    return cur_offset





