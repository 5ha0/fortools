from PIL.ExifTags import TAGS


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


class HWPAnalysis:
    def __init__(self, file):
        self.file = file

    def showlist(self):
        print(self.file.listdir(streams=True, storages=False))
