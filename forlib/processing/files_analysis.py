from PIL.ExifTags import TAGS
import datetime


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