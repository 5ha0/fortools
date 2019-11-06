from PIL.ExifTags import TAGS
import datetime
import os
from datetime import date, time, timedelta
from os import listdir
from os import path
import time
import json
from zipfile import ZipFile

# jpeg data: time, latitude, longitude
class JPEGAnalysis:
    def __init__(self, file):
        self.file = file
        self.jpeg_json = self.__make_json()

    def __make_json(self):
        files_obj = dict()
        info = self.file._getexif()
        exif = {}
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            exif[decoded] = value
        try:
            # from the exif data, extract gps
            exifGPS = exif['GPSInfo']
            latData = exifGPS[2]
            lonData = exifGPS[4]

            # calculate the lat / long
            latDeg = latData[0][0] / float(latData[0][1])
            latMin = latData[1][0] / float(latData[1][1])
            latSec = latData[2][0] / float(latData[2][1])
            lonDeg = lonData[0][0] / float(lonData[0][1])
            lonMin = lonData[1][0] / float(lonData[1][1])
            lonSec = lonData[2][0] / float(lonData[2][1])

            # correct the lat/lon based on N/E/W/S
            Lat = (latDeg + (latMin + latSec / 60.0) / 60.0)
            if exifGPS[1] == 'S': Lat = Lat * -1
            Lon = (lonDeg + (lonMin + lonSec / 60.0) / 60.0)
            if exifGPS[3] == 'W': Lon = Lon * -1
        except:
            Lat = "no Latitude info"
            Lon = "no Longitude info"

        try:
            # getTime
            createTime = info[0x9003]
            time = createTime[0:4] + "_" + createTime[5:7] + "_" + createTime[8:10] + "_" + createTime[11:13] + "_" + createTime[14:16] + "-" + createTime[17:19]
        except:
            time = "no time info"

        files_obj["time"] = time
        files_obj["Latitude"] = Lat
        files_obj["Longitude"] = Lon
        return files_obj

    def show_all_info(self):
        print(self.jpeg_json)


# pdf analysis: author, creator, create Time, modification Time, pdf Version
class PDFAnalysis:
    def __init__(self, file):
        self.file = file
        self.file_json = self.__make_json()

    def __make_json(self):
        info = self.file.getDocumentInfo()
        info_obj = dict()
        info_obj["author"] = info['/Author']
        info_obj["creator"] = info['/Creator']
        time_info = info['/CreationDate'].replace("'", ':', 1)
        info_obj["creation"] = datetime.datetime.strptime(time_info[2:-1], "%Y%m%d%H%M%S%z").isoformat()
        time_info = info['/ModDate'].replace("'", ':', 1)
        info_obj["modification"] = datetime.datetime.strptime(time_info[2:-1], "%Y%m%d%H%M%S%z").isoformat()
        info_obj["pdf version"] = info['/PDFVersion']
        return info_obj

    def pdf_info(self):
        return self.file_json


class HWPAnalysis:
    def __init__(self, file):
        self.file = file
        self.list = self.return_list

    def return_list(self):
        name = self.file.listdir(streams=True, storages=False)
        return name

    def get_info(self):
        meta = self.file.getproperties('\x05HwpSummaryInformation', convert_time=True, no_conversion=[10])
        file_obj = dict()
        file_obj["Author"] = meta[4]
        file_obj["Date"] = meta[20]
        file_obj["Last Save"] = meta[8]
        file_obj["Create Time"] = meta[12]
        file_obj["Last Save Time"] = meta[13]
        print(file_obj)
        return file_obj

    def get_prev(self):
        prev = self.file.openstream('PrvText').read().decode('utf-16')
        print(prev)
        return prev

    def show_bin(self, name):
        for i in range(0, len(self.list)):
            if name == self.list[i]:
                return i
        print(self.file.openstream(self.list[i].read()))

class MSOldAnalysis:
    def __init__(self, file):
        self.file = file

    def get_info(self):
        meta = self.file.get_metadata()
        file_obj = dict()
        try:
            file_obj["title"] = meta.title.decode('cp949')
        except:
            file_obj["title"] = 'no title'
        try:
            file_obj["Author"] = meta.author.decode('cp949')
        except:
            file_obj["Author"] = 'no author'
        try:
            file_obj["Create Time"] = meta.create_time.strftime('%Y-%m-%d %H:%M:%S')
        except:
            file_obj["Create Time"] = 'no creatTime'
        try:
            file_obj["Last Save"] = meta.last_saved_by.decode('cp949')
        except:
            file_obj["Last Save"] = 'no info'
        try:
            file_obj["Last Save Time"] = meta.last_saved_time.strftime('%Y-%m-%d %H:%M:%S')
        except:
            file_obj["Last Save Time"] = 'no info'
        try:
            file_obj["creating_application"] = meta.creating_application.decode()
        except:
            file_obj["creating_application"] = 'no info'
        print(file_obj)
        return file_obj

# zip analysis: filename, comment, MAC time, zip version, Compressed size, Uncompressed size, crc, Raw time
class ZIPAnalysis:
    def __init__(self, file):
        self.file = file

    def get_info(self):
        num = 1
        for info in self.file.infolist():
            print("[%d]FileName: " % num + os.path.basename(info.filename))
            print("\tComment: " + str(info.comment))
            print("\tModified: " + str(datetime.datetime(*info.date_time)))
            print("\tSystem: " + str(info.create_system) + "(0 = Windows, 3 = Unix)")
            print("\tZIP version: " + str(info.create_version))
            print("\tCompressed: " + str(info.compress_size) + " bytes")
            print("\tUncompressed: " + str(info.file_size) + " bytes")
            print("\tCRC: " + str(info.CRC))
            print("\tVolume: " + str(info.volume))
            print("\tInternal attr: " + str(info.internal_attr))
            print("\tExternal attr: " + str(info.external_attr))
            print("\tHeader offset: " + hex(info.header_offset))
            print("\tFlag bits: " + str(info.flag_bits))
            print("\tRaw time: " + str(info._raw_time))
            num += 1

# Print files in folder
def file_list(in_path):
    files = [f for f in listdir(in_path)]
    file_length = len(files)
    filename=[]

    for i in range(file_length):
        filename.append(0)

    for i in range(file_length):
        filename.append(files[i])
        mt = time.ctime(path.getmtime(in_path + '\\' + files[i]))
        ct = time.ctime(path.getctime(in_path + '\\' + files[i]))

        file_obj = {
            "no" + str(i+1) : {
                "Name" : files[i],
                "Modified TIme" : mt,
                "Created Time" : ct
            }
        }
        print(json.dumps(file_obj))
    print("Total: " + str(file_length))