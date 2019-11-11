import json
import sqlite3
import binascii
from datetime import *
import re
from forlib.processing.filter import *


class Chrome:
    class History:
        def __init__(self, file):
            self.file = file
            self.conn = sqlite3.connect(self.file)
            self.history_list = []
            self.__parse()
            self.__sort()

        def __parse(self):
            history_cursor = self.conn.cursor()
            visits_open = history_cursor.execute(
                "SELECT visits.from_visit, visits.visit_time, visits.transition, urls.url, urls.title, urls.visit_count, urls.id FROM urls, visits WHERE urls.id = visits.url")
            no = 0
            for visit in visits_open:
                no += 1
                mkdict = dict()
                mkdict["index"] = no
                mkdict["type"] = "history"
                mkdict["browser"] = "chrome"
                mkdict["title"] = visit[4]
                mkdict["url"] = visit[3]
                # if there is data, get from_visit data
                if visit[0] == 0:
                    mkdict["from_visit"] = visit[0]
                else:
                    from_visit_cursor = self.conn.cursor()
                    get_url_cursor = self.conn.cursor()
                    url_id = from_visit_cursor.execute(
                        "SELECT visits.url FROM visits WHERE visits.id=" + str(visit[0])).fetchone()[0]
                    mkdict["from_visit"] = \
                    get_url_cursor.execute("SELECT urls.url FROM urls WHERE urls.id=" + str(url_id)).fetchone()[0]

                keyword_cursor = self.conn.cursor()
                mkdict["keyword_search"] = keyword_cursor.execute(
                    "SELECT keyword_search_terms.term FROM keyword_search_terms WHERE keyword_search_terms.url_id= " + str(
                        visit[6])).fetchall()
                if mkdict["keyword_search"] == []:
                    mkdict["keyword_search"] = ""
                mkdict["visit_time"] = int2date1(visit[1])
                mkdict["visit_count"] = visit[5]
                mkdict["visit_type"] = visit[2]

                self.history_list.append(mkdict)

        def get_info(self):
            return self.history_list

        def __sort(self):
            self.history_list=time_sort('visit_time', self.history_list)

        def time_sort(self,key):
            data_list = self.history_list
            data_list=time_sort(key, data_list)
            return data_list

        def cnt_sort(self):
            json_list = self.history_list
            json_list = sorted(json_list, key=lambda list_info: (list_info["visit_count"]))
            return json_list

        def keyword_search(self, keyword):
            result = []
            json_list=self.history_list
            for i in json_list:
                for j in i["keyword_search"]: #j: keyword서치튜플
                    for k in range (0,len(j)):
                        if keyword in j[k]:
                            result.append(i)
                            break
                    if i in result: #중복방지
                        break
            return result


    class Download:
        def __init__(self, file):
            self.file = file
            self.conn = sqlite3.connect(self.file)
            self.download_list = []
            self.__parse()
            self.__sort()

        def __parse(self):
            downloads_cursor = self.conn.cursor()
            downloads_open = downloads_cursor.execute("SELECT downloads.* FROM downloads")
            no = 0
            for download in downloads_open:
                no += 1
                mkdict = dict()
                mkdict["index"] = no
                mkdict["type"] = "downloads"
                mkdict["browser"] = "chrome"
                mkdict["file_name"] = download[3].split("\\")[-1]
                mkdict["download_path"] = download[2]
                mkdict["download_start_time"] = int2date1(download[4])
                mkdict["download_end_time"] = int2date1(download[11])
                mkdict["file_size"] = download[6]
                downloads_url_chains_cursor = self.conn.cursor()
                mkdict["url"] = downloads_url_chains_cursor.execute(
                    "SELECT downloads_url_chains.chain_index,downloads_url_chains.url FROM downloads_url_chains WHERE downloads_url_chains.id=" + str(
                        download[0])).fetchall()
                mkdict["guid"] = download[1]
                mkdict["opened"] = download[12]
                mkdict["state"] = download[7]

                # mkdictno = dict()
                # mkdictno["no" + str(no)] = mkdict
                self.download_list.append(mkdict)
                # print(mkdict)

        def get_info(self):
            return self.download_list

        def __sort(self):
            self.download_list=time_sort('download_start_time', self.download_list)

        def time_sort(self, key):
            data_list = self.download_list
            data_list=time_sort(key, data_list)
            return data_list


    class Cookie:
        def __init__(self, file):
            self.file = file
            self.conn = sqlite3.connect(self.file)
            self.cookie_list = []
            self.__parse()
            self.__sort()

        def __parse(self):
            self.cookie_list = []
            cookies_cursor = self.conn.cursor()
            cookies_open = cookies_cursor.execute("SELECT * FROM cookies")
            no = 0
            for cookie in cookies_open:
                no += 1
                mkdict = dict()
                mkdict["index"] = no
                mkdict["type"] = "cookies"
                mkdict["browser"] = "chrome"
                mkdict["name"] = cookie[2]
                mkdict["value"] = cookie[3]
                mkdict["creation_time"] = int2date1(cookie[0])
                mkdict["last_accessed_time"] = int2date1(cookie[8])
                mkdict["expiry_time"] = int2date1(cookie[5])
                mkdict["host"] = cookie[1]
                mkdict["path"] = cookie[4]
                mkdict["is_secure"] = cookie[6]
                mkdict["is_httponly"] = cookie[7]

                # mkdictno = dict()
                # mkdictno["no" + str(no)] = mkdict
                self.cookie_list.append(mkdict)

        def get_info(self):
            return self.cookie_list

        def __sort(self):
            self.cookie_list=time_sort('creation_time', self.cookie_list)

        def time_sort(self, key):
            date_list=self.cookie_list
            data_list=sort_date = time_sort(key, date_list)
            return sort_date


class Firefox:
    class History:
        def __init__(self, file):
            self.file = file
            self.conn = sqlite3.connect(self.file)
            self.history_list=[]
            self.__parse()
            self.__sort()

        def __parse(self):
            visits_cursor = self.conn.cursor()
            visits_open = visits_cursor.execute(
                "SELECT moz_places.title, moz_places.url,moz_historyvisits.from_visit,moz_historyvisits.visit_date,moz_places.visit_count,moz_historyvisits.visit_type FROM moz_historyvisits, moz_places WHERE moz_places.id = moz_historyvisits.place_id")
            no = 0
            for visit in visits_open:
                no += 1
                mkdict = dict()
                mkdict["index"] = no
                mkdict["type"] = "history"
                mkdict["browser"] = "firefox"
                mkdict["title"] = visit[0]
                if mkdict["title"] is None:
                    mkdict["title"]=""
                mkdict["url"] = visit[1]
                if visit[2] == 0:
                    mkdict["from_visit"] = visit[2]
                else:
                    from_visit_cursor = self.conn.cursor()
                    get_url_cursor = self.conn.cursor()
                    url_id = from_visit_cursor.execute(
                        "SELECT moz_historyvisits.place_id FROM moz_historyvisits WHERE moz_historyvisits.id=" + str(
                            visit[2])).fetchone()[0]
                    mkdict["from_visit"] = get_url_cursor.execute(
                        "SELECT moz_places.url FROM moz_places WHERE moz_places.id=" + str(url_id)).fetchone()[0]

                mkdict["keyword_search"] = ""
                mkdict["visit_time"] = int2date2(visit[3])
                mkdict["visit_count"] = visit[4]
                mkdict["visit_type"] = visit[5]
                self.history_list.append(mkdict)

        def get_info(self):
            return self.history_list

        def __sort(self):
            self.history_list=time_sort('visit_time', self.history_list)

        def time_sort(self, key):
            data_list = self.history_list
            data_list=time_sort(key, data_list)
            return data_list

        def cnt_sort(self):
            json_list = self.history_list
            json_list = sorted(json_list, key=lambda list_info: (list_info["visit_count"]))
            return json_list

        def keyword_search(self, keyword):
            result = []
            json_list=self.history_list
            for i in json_list:
                if keyword in i["title"]:
                    result.append(i)
            return result


    class Cookie:
        def __init__(self, file):
            self.file = file
            self.conn = sqlite3.connect(self.file)
            self.cookie_list=[]
            self.__parse()
            self.__sort()

        def __parse(self):
            cookies_cursor = self.conn.cursor()
            cookies_open = cookies_cursor.execute("SELECT * FROM moz_cookies")
            no = 0
            for cookie in cookies_open:
                no += 1
                mkdict = dict()
                mkdict["index"] = no
                mkdict["type"] = "cookies"
                mkdict["browser"] = "firefox"
                mkdict["name"] = cookie[3]
                mkdict["value"] = cookie[4]
                mkdict["creation_time"] = int2date2(cookie[9])
                mkdict["last_accessed_time"] = int2date2(cookie[8])
                mkdict["expiry_time"] = int2date3(cookie[7])
                mkdict["host"] = cookie[5]
                mkdict["path"] = cookie[6]
                mkdict["is_secure"] = cookie[10]
                mkdict["is_httponly"] = cookie[11]
                self.cookie_list.append(mkdict)

        def get_info(self):
            return self.cookie_list

        def __sort(self):
            self.cookie_list=time_sort('creation_time', self.cookie_list)

        def time_sort(self, key):
            data_list = self.cookie_list
            data_list=time_sort(key, data_list)
            return data_list

    class Download:
        def __init__(self, file):
            self.file = file
            self.conn = sqlite3.connect(self.file)
            self.download_list = []
            self.__parse()
            self.__sort()

        def __parse(self):
            moz_places_cursor = self.conn.cursor()
            place_id_open = moz_places_cursor.execute(
                "SELECT moz_historyvisits.place_id FROM moz_historyvisits WHERE moz_historyvisits.visit_type=7")
            no = 0
            for moz_place in place_id_open:
                no += 1
                mkdict = dict()
                mkdict["index"] = no
                mkdict["type"] = "downloads"
                mkdict["browser"] = "firefox"
                downloads_cursor = self.conn.cursor()
                downloads_open = downloads_cursor.execute(
                    "SELECT moz_annos.anno_attribute_id, moz_annos.content,moz_annos.dateAdded FROM moz_annos WHERE moz_annos.place_id=" + str(
                        moz_place[0])).fetchall()
                anno_attribute_cursor = self.conn.cursor()
                anno_attribute_open = anno_attribute_cursor.execute(
                    "SELECT moz_anno_attributes.* FROM moz_anno_attributes")
                for anno_attribute in anno_attribute_open:
                    for i in range(0, len(downloads_open)):
                        if anno_attribute[0] == downloads_open[i][0]:
                            if anno_attribute[1] == "downloads/destinationFileURI":
                                mkdict["file_name"] = downloads_open[i][1].split('/')[-1]
                                mkdict["download_path"] = downloads_open[i][1]
                                mkdict["download_start_time"] = int2date2(downloads_open[i][2])
                            elif anno_attribute[1] == "downloads/metaData":
                                tempdict = eval(downloads_open[i][1])
                                mkdict["download_end_time"] = int2date3(tempdict["endTime"])
                                mkdict["file_size"] = tempdict["fileSize"]
                url_guid_cursor = self.conn.cursor()
                url_guid = url_guid_cursor.execute(
                    "SELECT moz_places.url, moz_places.guid FROM moz_places WHERE moz_places.id=" + str(
                        moz_place[0])).fetchone()
                mkdict["url"] = url_guid[0]
                mkdict["guid"] = url_guid[1]
                mkdict["opened"] = ""
                mkdict["state"] = ""
                self.download_list.append(mkdict)

        def get_info(self):
            return self.download_list

        def __sort(self):
            self.download_list=time_sort('download_start_time', self.download_list)

        def time_sort(self, key):
            data_list = self.download_list
            data_list=time_sort(key, data_list)
            return data_list


class Ie_Edge:
    class Cache:
        def __init__(self, file):
            self.file = file
            self.cache_list = []
            self.__parse()
            self.__sort()

        def __parse(self):
            cache_noContainer = []  # 없는 container 저장하는 list
            cache_emptyContainer = []  # 빈 container 저장하는 list
            cache_container_id = get_ContainerID(self.file, "Content")
            no = 0
            for containerid in cache_container_id.keys():
                col_name = get_schema(self.file, containerid)
                cache_container = self.file.get_table_by_name(containerid)
                if col_name == None:
                    cache_noContainer.append(containerid)
                    continue
                if cache_container.number_of_records == 0:
                    cache_emptyContainer.append(containerid)
                    continue

                for cache in cache_container.records:
                    no += 1
                    mkdict = dict()
                    mkdict["index"] = no
                    mkdict["type"] = "cache"
                    mkdict["browser"] = "IE10+ Edge"

                    mkdict["file_name"] = cache.get_value_data_as_string(18)
                    mkdict["url"] = cache.get_value_data_as_string(17)
                    mkdict["access_time"] = int2date4(cache.get_value_data_as_integer(13))
                    mkdict["creation_time"] = int2date4(cache.get_value_data_as_integer(10))
                    mkdict["file_size"] = cache.get_value_data_as_integer(5)
                    mkdict["file_path"] = cache.get_value_data_as_integer(4)
                    if cache.get_value_data_as_integer(11) == 0:
                        mkdict["expiry_time"] = 0
                    else:
                        mkdict["expiry_time"] = int2date4(cache.get_value_data_as_integer(11))
                    mkdict["last_modified_time"] = int2date4(cache.get_value_data_as_integer(13))
                    if cache.get_value_data(21) is not None:
                        mkdict["server_info"] = cache.get_value_data(21).decode().split(" ")[1]
                    else:
                        mkdict["server_info"] = ""

                    self.cache_list.append(mkdict)

        def get_info(self):
            return self.cache_list

        def __sort(self):
            self.cache_list=time_sort('creation_time', self.cache_list)

        def time_sort(self, key):
            data_list = self.cache_list
            data_list=time_sort(key, data_list)
            return data_list

    class Cookie:
        def __init__(self, file):
            self.file = file
            self.cookie_list=[]
            self.__parse()
            self.__sort()

        def __parse(self):
            cookies_no_container = []  # 없는 container 저장하는 list
            cookies_empty_container = []  # 빈 container 저장하는 list
            cookies_container_id = get_ContainerID(self.file, "Cookies")
            no = 0
            for containerid in cookies_container_id.keys():
                col_name = get_schema(self.file, containerid)
                cookies_container = self.file.get_table_by_name(containerid)
                if col_name is None:
                    cookies_no_container.append(containerid)
                    continue
                if cookies_container.number_of_records == 0:
                    cookies_empty_container.append(containerid)
                    continue
                for cookie in cookies_container.records:
                    no += 1
                    mkdict = dict()
                    mkdict["index"] = no
                    mkdict["type"] = "cookies"
                    mkdict["browser"] = "IE10+ Edge"
                    mkdict["name"] = cookie.get_value_data_as_stirng(18)
                    mkdict["value"] = ""
                    mkdict["creation_time"] = int2date4(cookie.get_value_data_as_integer(10))
                    mkdict["last_accessed_time"] = int2date4(cookie.get_value_data_as_integer(13))
                    mkdict["expiry_time"] = int2date4(cookie.get_value_data_as_integer(11))
                    mkdict["host"] = cookie.get_value_data_as_string(17)
                    mkdict["path"] = ""
                    mkdict["is_secure"] = ""
                    mkdict["is_httponly"] = ""

                    self.cookie_list.append(mkdict)

        def get_info(self):
            return self.cookie_list

        def __sort(self):
            self.cookie_list=time_sort('creation_time', self.cookie_list)

        def time_sort(self,key):
            data_list = self.cookie_list
            data_list=time_sort(key, data_list)
            return data_list

    class Download:
        def __init__(self, file):
            self.file = file
            self.download_list=[]
            self.__parse()
            self.__sort()

        def __parse(self):
            downloads_no_container = []  # 없는 container 저장하는 list
            downloads_empty_container = []  # 빈 container 저장하는 list
            downloads_container_id = get_ContainerID(self.file, "iedownload")
            no = 0
            for containerid in downloads_container_id.keys():
                col_name = get_schema(self.file, containerid)
                downloads_container = self.file.get_table_by_name(containerid)

                if col_name is None:
                    downloads_no_container.append(containerid)
                    continue

                if downloads_container.number_of_records == 0:
                    downloads_empty_container.append(containerid)
                    continue

                for download in downloads_container.records:
                    no += 1
                    mkdict = dict()
                    mkdict["index"] = no
                    mkdict["type"] = "download"
                    mkdict["browser"] = "IE10+ Edge"

                    # get binary data
                    binary_data = download.get_value_data(21)

                    # get file size
                    try:
                        size_a = bytes.decode(binascii.hexlify(binary_data[0x48:0x4F][::-1]))
                        size = int(size_a, 16)
                    except:
                        size = ""

                    # get filename/filepath/fileurl
                    path = ""
                    name = ""
                    url = ""
                    try:
                        data = bytes.decode(binascii.hexlify(binary_data[0x148:]))
                        path = bytes.fromhex(data).decode("utf-16").split("\x00")[-2]
                        name = path.split("\\")[-1]
                        url = bytes.fromhex(data).decode("utf-16").split("\x00")[-3]
                    except:
                        pass

                    mkdict["file name"] = name
                    mkdict["download_path"] = path
                    mkdict["download_start_time"] = int2date4(download.get_value_data_as_integer(13))
                    mkdict["download_end_time"] = ""
                    mkdict["file_size"] = size
                    mkdict["url"] = url
                    mkdict["guid"] = download.get_value_data_as_string(17)
                    mkdict["opened"] = ""
                    mkdict["state"] = ""

                    # mkdictno = dict()
                    # mkdictno["no" + str(no)] = mkdict
                    self.download_list.append(mkdict)

        def get_info(self):
            return self.download_list

        def __sort(self):
            self.download_list=time_sort('download_start_time', self.download_list)

        def time_sort(self,key):
            data_list = self.download_list
            data_list=time_sort(key, data_list)
            return data_list

    class History:
        def __init__(self, file):
            self.file = file
            self.history_list=[]
            self.__parse()
            self.__sort()

        def __parse(self):
            history_no_container = []  # 없는 container 저장하는 list
            history_empty_container = []  # 빈 container 저장하는 list

            history_container_id = get_ContainerID(self.file, "Hist")
            no = 0
            for containerid in history_container_id.keys():
                col_name = get_schema(self.file,containerid)
                history_container = self.file.get_table_by_name(containerid)

                if col_name is None:
                    history_no_container.append(containerid)
                    continue
                if history_container.number_of_records == 0:
                    history_empty_container.append(containerid)
                    continue
                # get only Histroy.IE5, MSHist###
                directory = re.compile('^MSHist|History.IE5')
                if directory.search(history_container_id.get(containerid).split("\\")[-2]) is None:
                    continue

                for visit in history_container.records:
                    no += 1
                    mkdict = dict()
                    mkdict["index"] = no
                    mkdict["type"] = "history"
                    mkdict["browser"] = "IE10+ Edge"
                    # get title from response header
                    try:
                        binary_data = visit.get_value_data(21)
                        size_a = bytes.decode(binascii.hexlify(binary_data[58:62][::-1]))
                        size = int(size_a, 16) * 2

                        if size > len(binary_data):
                            raise Exception
                        title = bytes.decode(binascii.hexlify(binary_data[62:62 + size]))
                        mkdict["title"] = bytes.fromhex(title).decode("utf-16").rstrip("\x00")
                    except:
                        mkdict["title"] = ""

                    mkdict["url"] = visit.get_value_data_as_string(17)
                    mkdict["from_visit"] = ""
                    mkdict["keyword_search"] = ""
                    mkdict["visit_time"] = int2date4(visit.get_value_data_as_integer(13))
                    mkdict["visit_count"] = visit.get_value_data_as_integer(8)
                    mkdict["visit_type"] = ""

                    # mkdictno = dict()
                    # mkdictno["no" + str(no)] = mkdict
                    self.history_list.append(mkdict)

        def get_info(self):
            return self.history_list

        def __sort(self):
            self.history_list=time_sort('visit_time', self.history_list)

        def time_sort(self,key):
            data_list = self.history_list
            data_list=time_sort(key, data_list)
            return data_list

        def cnt_sort(self):
            json_list = self.history_list
            json_list = sorted(json_list, key=lambda list_info: (list_info["visit_count"]))
            return json_list

        def keyword_search(self, keyword):
            result = []
            json_list=self.history_list
            for i in json_list:
                if keyword in i["title"]:
                    result.append(i)
            print(result)
            return result

# chrome change int to date
def int2date1(date_time):
    # 1601년 1월 1일부터
    from_date = datetime.datetime(1601, 1, 1)
    passing_time = timedelta(microseconds=date_time)
    get_date = from_date+passing_time
    return get_date.strftime("%Y-%m-%d %H:%M:%S")

# firefox change int to date
def int2date2(date_time):
    #1970년 1월 1일부터
    get_date=datetime.datetime.fromtimestamp(date_time / 1000000)
    return get_date.strftime("%Y-%m-%d %H:%M:%S")

# firefox change int to date
def int2date3(date_time):
    #1970년 1월 1일부터
    get_date=datetime.datetime.fromtimestamp(date_time / 1000)
    return get_date.strftime("%Y-%m-%d %H:%M:%S")

# IE_Edge change in to date
def int2date4(date_time):
    # 1601년 1월 1일부터
    from_date = datetime.datetime(1601, 1, 1)
    passing_time = timedelta(microseconds=(date_time*0.1))
    get_date = from_date + passing_time
    return get_date.strftime("%Y-%m-%d %H:%M:%S")

# get containerid, directory of IE_Edge
def get_ContainerID(file, name):
    ContainerID = dict()
    Containers = file.get_table_by_name("Containers")
    for record in Containers.records:
        if name=="Hist":
            regex=re.compile('^MSHist|History')
            if regex.search(record.get_value_data_as_string(8)) is not None:
                ContainerID["Container_" + str(record.get_value_data_as_integer(0))] = record.get_value_data_as_string(10)
        elif record.get_value_data_as_string(8) == name:
                ContainerID["Container_" + str(record.get_value_data_as_integer(0))] = record.get_value_data_as_string(10)
    return ContainerID

#column name and type of IE_Edge
def get_schema(file, table):
    col_infos=[]
    get_container = file.get_table_by_name(table)
    if get_container == None: #container가 없을 때
        return get_container
    for column in get_container.columns:
        col_info = []
        col_info.append(column.name)
        col_info.append(column.get_type())
        col_infos.append(col_info)
    return col_infos