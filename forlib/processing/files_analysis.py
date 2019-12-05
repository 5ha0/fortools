from PIL.ExifTags import TAGS
import os
from datetime import *
import forlib.calc_hash as calc_hash
from os.path import getmtime, getctime, getatime
from datetime import timezone, timedelta, datetime, date, time
from os import listdir, path
import json
import sys
from zipfile import ZipFile
from forlib import signature as sig
import magic


def sig_check(path):
    extension = magic.from_file(path).split(',')[0]
    if extension[:11] == 'cannot open' or extension == 'data':
        extension = sig.sig_check(path)
    return extension


# jpeg data: time, latitude, longitude
class JPEGAnalysis:
    def __init__(self, file, path, hash_v):
        self.__file = file
        self.__jpeg_json = self.__make_json()
        self.__hash_value = [hash_v]
        self.__path = path
        self.__cal_hash()

    def __make_json(self):
        files_obj = dict()
        info = self.__file._getexif()
        exif = {}
        if info == None:
            print('There is not information of this picture.')
            return -1
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
            time = createTime[0:4] + "-" + createTime[5:7] + "-" + createTime[8:10] + " " + createTime[11:13] + ":" + createTime[14:16] + ":" + createTime[17:19]
        except:
            time = "no time info"

        files_obj["time"] = time
        files_obj["Latitude"] = Lat
        files_obj["Longitude"] = Lon
        return files_obj

    def __cal_hash(self):
        self.__hash_value.append(calc_hash.get_hash(self.__path))

    def get_hash(self):
        return self.__hash_value

    def show_info(self):
        print(self.__jpeg_json)

    def get_info(self):
        return [self.__jpeg_json]


# pdf analysis: author, creator, create Time, modification Time, pdf Version
class PDFAnalysis:
    def __init__(self, file, path, hash_v):
        self.__file = file
        self.__pdf_json = self.__make_json()
        self.__hash_value = [hash_v]
        self.__path = path
        self.__cal_hash()

    def __make_json(self):
        info = self.__file.getDocumentInfo()
        info_obj = dict()
        try:
            info_obj["author"] = info['/Author']
        except KeyError:
            info_obj["author"] = 'None'
        try:
            info_obj["creator"] = info['/Creator']
        except KeyError:
            info_obj["creator"] = 'None'
        try:
            time_info = info['/CreationDate'].replace("'", ':', 1)
        except KeyError:
            time_info = "None"
        try:
            time_info = datetime.strptime(time_info[2:-1], "%Y%m%d%H%M%S%z")
            info_obj["creation"] = time_info.strftime("%Y-%m-%d %H:%M:%S")
        except KeyError:
            info_obj["creation"] = 'None'
        try:
            time_info = info['/ModDate'].replace("'", ':', 1)
            mod_time = datetime.strptime(time_info[2:-1], "%Y%m%d%H%M%S%z")
            info_obj["modification"] = mod_time.strftime("%Y-%m-%d %H:%M:%S")
        except KeyError:
            info_obj["modification"] = 'None'
        try:
            info_obj["TimeZone"] = mod_time.strftime("%Z")
        except KeyError:
            info_obj["TimeZone"] = 'None'
        return info_obj

    def __cal_hash(self):
        self.__hash_value.append(calc_hash.get_hash(self.__path))

    def get_hash(self):
        return self.__hash_value

    def get_info(self):
        return [self.__pdf_json]

    def show_info(self):
        print(self.__pdf_json)


class HWPAnalysis:
    def __init__(self, file, path, hash_v):
        self.__file = file
        self.list = self.__return_list
        self.__hwp_info = self.__make_json()
        self.__hash_value = [hash_v]
        self.__path = path
        self.__cal_hash()

    def __return_list(self):
        name = self.__file.listdir(streams=True, storages=False)
        return name

    def __make_json(self):
        meta = self.__file.getproperties('\x05HwpSummaryInformation', convert_time=True, no_conversion=[10])
        file_obj = dict()
        file_obj["Author"] = meta[4].replace('\x00','')
        file_obj["Date"] = meta[20].replace('\x00','')
        file_obj["Last Save"] = meta[8].replace('\x00','')
        file_obj["Create Time"] = meta[12].strftime("%Y-%m-%d %H:%M:%S")
        file_obj["Last Save Time"] = meta[13].strftime("%Y-%m-%d %H:%M:%S")
        return file_obj

    def __cal_hash(self):
        self.__hash_value.append(calc_hash.get_hash(self.__path))

    def get_hash(self):
        return self.__hash_value

    def show_info(self):
        print(self.__hwp_info)

    def get_info(self):
        return [self.__hwp_info]

    def get_prev(self):
        prev = self.__file.openstream('PrvText').read().decode('utf-16')
        print(prev)
        return prev

    def show_bin(self, name):
        for i in range(0, len(self.list)):
            if name == self.list[i]:
                return i
            print(self.__file.openstream(self.list[i].read()))


class MSOldAnalysis:
    def __init__(self, file, path, hash_v):
        self.__file = file
        self.__ms_json = self.__make_json()
        self.__hash_value = [hash_v]
        self.__path = path
        self.__cal_hash()

    def __make_json(self):
        meta = self.__file.get_metadata()
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
        return file_obj

    def __cal_hash(self):
        self.__hash_value.append(calc_hash.get_hash(self.__path))

    def get_hash(self):
        return self.__hash_value

    def show_info(self):
        print(self.__ms_json)

    def get_info(self):
        return [self.__ms_json]


# zip analysis: filename, comment, MAC time, zip version, Compressed size, Uncompressed size, crc, Raw time
class ZIPAnalysis:
    def __init__(self, file):
        self.file = file
        self.__info = self.__parse()

    def __parse(self):
        json_list = []
        num = 1
        for info in self.file.infolist():
            file_obj = dict()
            file_name = os.path.basename(info.filename)
            file_obj['num'] = num
            file_obj['FileName'] = file_name
            file_obj['Comment'] = str(info.comment)

            mod_time = datetime(*info.date_time)

            mtime = str(mod_time.astimezone()).split('+')[1]
            file_obj['TimeZone'] = "UTC+"+str(mtime)
            file_obj['Modified'] = str(mod_time)
            file_obj['System'] = str(info.create_system) + "(0 = Windows, 3 = Unix)"
            file_obj['version'] = str(info.create_version)
            file_obj['Compressed'] = str(info.compress_size) + " bytes"
            file_obj['Uncompressed'] = str(info.file_size) + " bytes"
            file_obj['CRC'] = str(info.CRC)
            file_obj['Volume'] = str(info.volume)
            file_obj['Internal attr'] = str(info.internal_attr)
            file_obj['External attr'] = str(info.external_attr)
            file_obj['Header offset'] = str(info.header_offset)
            file_obj['Flag bits'] = str(info.flag_bits)
            file_obj['Raw time'] = str(info._raw_time)


            json_list.append(file_obj)
            num += 1
        return json_list

    def get_info(self):
        return self.__info

    def show_info(self):
        for i in self.__info:
            print(i)

    # def last_modtime(self):
    #     num = 1
    #     for info in self.file.infolist():
    #         file_name = os.path.basename(info.filename)
    #         #print(str(num) + "\tFilename: " + file_name + '\t '+ "Modified Time: " + str(datetime(*info.date_time)))
    #         print(file_name)
    #         num += 1


# Print files in folder
def file_list(in_path):
    try:
        files = [f for f in listdir(in_path)]
        file_length = len(files)
        filename = []
        folder_list = []
        sig_type = None

        for i in range(file_length):
            filename.append(0)

        for i in range(file_length):
            filename.append(files[i])
            abs_path = in_path + '\\' + str(files[i])
            folder_check = os.path.isdir(abs_path)
            if folder_check is True:
                folder_list.append(abs_path)
            elif folder_check is False:
                sig_type = sig_check(abs_path)

            #print('-' * 20 + abs_path + '-' * 20)
            mt = datetime.fromtimestamp(getmtime(in_path)).strftime('%Y-%m-%d %H:%M:%S')
            ct = datetime.fromtimestamp(getctime(in_path)).strftime('%Y-%m-%d %H:%M:%S')
            at = datetime.fromtimestamp(getatime(in_path)).strftime('%Y-%m-%d %H:%M:%S')

            file_obj = {
                "Modified Time": mt,
                "Created Time": ct,
                "Access Time": at,
                "Folder": folder_check,
                "Type": sig_type
            }
            print('[' + str(i + 1) + '] FileNanme: ' + str(files[i]) + ' ' + json.dumps(file_obj))
            #print('[' + str(i + 1) + '] FileNanme: ' + abs_path + " " + json.dumps(file_obj))
        if file_length != 0:
            print("Total: " + str(file_length))
            print("Folder path : " + os.path.abspath(os.path.join(abs_path, os.pardir)) + "\n")


        for i in range(0, len(folder_list)):
            file_list(folder_list[i])

    except:
        print("[Error] Path is not found. Check your input")




