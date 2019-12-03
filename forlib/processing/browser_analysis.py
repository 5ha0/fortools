import sqlite3
import binascii
import re
from datetime import *
from forlib.processing.filter import *
import forlib.calc_hash as calc_hash


class Chrome:
    class History:
        def __init__(self, file, hash_v):
            self.file = file
            self.conn = sqlite3.connect(self.file)
            self.history_list = []
            if self.__parse() == -1:
                self.history_list=""
            self.__sort()
            self.__hash_value = [hash_v]
            self.__path = file
            self.__cal_hash()

        def __parse(self):
            try:
                history_cursor = self.conn.cursor()
            except:
                print("please check your file")
                return -1
            try:
                visits_open = history_cursor.execute("SELECT visits.from_visit, visits.visit_time, visits.transition, urls.url, urls.title, urls.visit_count, urls.id FROM urls, visits WHERE urls.id = visits.url")
            except:
                print("This file does not have such tables")
                return -1
            no = 0
            for visit in visits_open:
                no += 1
                mkdict = dict()
                mkdict["index"] = no
                mkdict["type"] = "history"
                mkdict["browser"] = "chrome"
                mkdict["timezone"] = "UTC"
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
                get_keyword = keyword_cursor.execute(
                    "SELECT keyword_search_terms.term FROM keyword_search_terms WHERE keyword_search_terms.url_id= " + str(
                        visit[6])).fetchall()

                keyword_list=[]
                for i in get_keyword:
                    for j in range(0, len(get_keyword)):
                        keyword_list.append(i[j])

                mkdict["keyword_search"]=keyword_list

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
                        if keyword in j:
                            result.append(i)
                            break
                    if i in result: #중복방지
                        break
            return result

        def __cal_hash(self):
            self.__hash_value.append(calc_hash.get_hash(self.__path))

        def get_hash(self):
            return self.__hash_value


    class Download:
        def __init__(self, file, hash_v):
            self.file = file
            self.conn = sqlite3.connect(self.file)
            self.download_list = []
            self.__parse()
            if self.__parse() == -1:
                self.download_list=""
            self.__sort()
            self.__hash_value = [hash_v]
            self.__path = file
            self.__cal_hash()

        def __parse(self):
            try:
                downloads_cursor = self.conn.cursor()
                downloads_cursor_row = self.conn.cursor()
            except:
                print("please check your file")
                return -1
            try:
                downloads_open = downloads_cursor.execute("SELECT downloads.* FROM downloads")
            except:
                print("This file does not have such tables")
                return -1
            downloads_get_row = sqlite_get_schema("downloads", downloads_cursor_row)

            for row in downloads_get_row:
                if row[1]=="current_path":
                    current_path=row[0]
                elif row[1]=="start_time":
                    start_time=row[0]
                elif row[1]=="received_bytes":
                    received_bytes=row[0]
                elif row[1]=="end_time":
                    end_time=row[0]
                elif row[1]=="id":
                    download_id=row[0]
                elif row[1]=="guid":
                    guid=row[0]
                elif row[1] == "opened":
                    opened=row[0]
                elif row[1]=="state":
                    state=row[0]

            no = 0
            for download in downloads_open:
                no += 1
                mkdict = dict()
                mkdict["index"] = no
                mkdict["type"] = "downloads"
                mkdict["browser"] = "chrome"
                mkdict["timezone"]="UTC"
                mkdict["file_name"] = download[current_path].split("\\")[-1]
                mkdict["download_path"] = download[current_path]
                mkdict["download_start_time"] = int2date1(download[start_time])
                mkdict["download_end_time"] = int2date1(download[end_time])
                mkdict["file_size"] = download[received_bytes]
                downloads_url_chains_cursor = self.conn.cursor()
                mkdict["url"] = downloads_url_chains_cursor.execute(
                    "SELECT downloads_url_chains.chain_index,downloads_url_chains.url FROM downloads_url_chains WHERE downloads_url_chains.id=" + str(
                        download[download_id])).fetchall()
                downloads_url_chains_cursor.close()
                try:
                    mkdict["guid"] = download[guid]
                except:
                    mkdict["guid"] = ""
                mkdict["opened"] = download[opened]
                mkdict["state"] = download[state]
                self.download_list.append(mkdict)

        def get_info(self):
            return self.download_list

        def __sort(self):
            self.download_list=time_sort('download_start_time', self.download_list)

        def time_sort(self, key):
            data_list = self.download_list
            data_list=time_sort(key, data_list)
            return data_list

        def __cal_hash(self):
            self.__hash_value.append(calc_hash.get_hash(self.__path))

        def get_hash(self):
            return self.__hash_value

    class Cache:
        def __init__(self, file):
            self.file = file
            self.__path = file
            self.cache_list = []
            if self.__parse() ==-1:
                self.cache_list==""

        def __get_block_info(self,url_record):
            if url_record == 1:
                block_size = 0x100
            elif url_record == 2:
                block_size = 0x400
            elif url_record == 3:
                block_size = 0x1000
            return block_size

        def __parse(self):
            no = 0
            try:
                data_0_open = open(self.__path + "\\data_0", 'rb')
            except:
                print("please check your folder")
                return -1
            data_0_open.seek(0x2000)
            while True:
                no += 1
                mkdict = dict()

                mkdict["index"] = no
                mkdict["type"] = "cache"
                mkdict["browser"] = "Chrome"
                mkdict["timezone"] = "UTC"
                # url record location
                url_record_info = data_0_open.read(0x24)[0x18:0x18 + 0x04]
                # no information in block size 0x24
                if bytes.decode(binascii.hexlify(url_record_info)) == "00000000":
                    continue
                # end of file
                elif bytes.decode(binascii.hexlify(url_record_info)) == "":
                    break
                # calculate block index
                block_index = int(bytes.decode(binascii.hexlify(url_record_info[:0x02][::-1])), 16)
                # file index/ block size
                file_index = url_record_info[0x02]
                block_size = self.__get_block_info(url_record_info[0x02])
                # get url_record_location
                url_record_location = block_index * block_size + 0x2000
                # open block which has url record
                data_file_open = open(self.__path + "\\data_" + str(file_index), 'rb')
                data_file_open.seek(url_record_location)
                url_record = data_file_open.read(0x60)
                url_size = int(bytes.decode(binascii.hexlify(url_record[0x20:0x20 + 0x04][::-1])), 16)
                meta_data_size = int(bytes.decode(binascii.hexlify(url_record[0x28:0x28 + 0x04][::-1])), 16)
                data_size = int(bytes.decode(binascii.hexlify(url_record[0x2C:0x2C + 0x04][::-1])), 16)

                # get url
                try:
                    url = data_file_open.read(url_size)
                    url = url.decode()
                except:
                    url_file_index = url_record[0x24 + 0x02]
                    url_block_size = self.__get_block_info(url_record[0x24 + 0x02])
                    url_block_index = int(bytes.decode(binascii.hexlify(url_record[0x24:0x24 + 0x02][::-1])), 16)

                    go_to_url_location = url_block_size * url_block_index + 0x2000
                    url_data_file_open = open(self.__path + "\\data_" + str(url_file_index), 'rb')
                    url_data_file_open.seek(go_to_url_location)
                    url = url_data_file_open.read(url_size)
                    url = url.decode()

                # get metadata(access_time,expiry_time,last_modified_time,server_info)
                status=""
                access=""
                expiry=""
                last_modify=""
                week = re.compile('\s?Mon,?|\s?Tue,?|\s?Wed,?|\s?Thu,?|\s?Fri,?|\s?Sat,?|\s?Sun,?')
                meta_data_file_index = url_record[0x38:0x38 + 0x04][0x02]
                if meta_data_size != 0:
                    meta_data_block_index = int(bytes.decode(binascii.hexlify(url_record[0x38:0x38 + 0x02][::-1])), 16)
                    if meta_data_block_index != 0:
                        meta_data_block_size = self.__get_block_info(meta_data_file_index)
                        meta_data_location = meta_data_block_size * meta_data_block_index + 0x2000
                        meta_data_open = open(self.__path + "\\data_" + str(meta_data_file_index), 'rb')
                        meta_data_open.seek(meta_data_location)
                        meta_data = meta_data_open.read(meta_data_size)
                        meta_data = bytes.decode(binascii.hexlify(meta_data))
                        status_regex=re.search("7374617475733a+\w{6}", meta_data)
                        if status_regex:
                            status=bytes.fromhex(status_regex.group()).decode().split(":")[-1]
                        date_regex=re.search("(44|64)+6174653a(20)?\w{50}",meta_data)
                        if date_regex:
                            if week.search(bytes.fromhex(date_regex.group()).decode()[5:9]):
                                access=" ".join(bytes.fromhex(date_regex.group()).decode().split(" ")[-4:])
                                access=str(datetime.datetime.strptime(access,'%d %b %Y %H:%M:%S'))
                        expires_regex=re.search("657870697265733a+\w{50}",meta_data)
                        if expires_regex:
                            if week.search(bytes.fromhex(expires_regex.group()).decode()[8:12]):
                                expiry = " ".join(bytes.fromhex(expires_regex.group()).decode().split(" ")[-4:])
                                expiry = str(datetime.datetime.strptime(expiry, '%d %b %Y %H:%M:%S'))
                        last_modified_regex=re.search("6c6173742d6d6f6469666965643a+\w{50}",meta_data)
                        if last_modified_regex:
                            if week.search(bytes.fromhex(last_modified_regex.group()).decode()[14:18]):
                                last_modify=" ".join(bytes.fromhex(last_modified_regex.group()).decode().split(" ")[-4:])
                                last_modify = str(datetime.datetime.strptime(last_modify, '%d %b %Y %H:%M:%S'))
                # get data/file_path and file_name
                file_path=""
                file_name=""
                if url_record[0x3c:0x3c + 0x04][0x03] == 0x80:
                    try:
                        get_another_file = "f_" + str(
                            bytes.decode(binascii.hexlify(url_record[0x3c:0x3c + 0x04][:0x03][::-1])))
                        file_path=get_another_file
                        file_name= (url.split("/")[-1]).split("?")[0]

                    except:
                        file_path=""
                        file_name=""
                else:
                    data_file_index = url_record[0x3c:0x3c + 0x04][0x02]
                    if data_size != 0:
                        data_block_size = self.__get_block_info(data_file_index)
                        data_block_index = int(bytes.decode(binascii.hexlify(url_record[0x3C:0x3C + 0x02][::-1])), 16)
                        data_location = data_block_size * data_block_index + 0x2000
                        data_open = open(self.__path + "\\data_" + str(data_file_index), 'rb')
                        file_path = "data_"+str(data_file_index)+" "+str(data_location)
                        file_name = (url.split("/")[-1]).split("?")[0]
                        data_open.seek(data_location)

                mkdict["file_name"]=file_name
                mkdict["url"] = url
                mkdict["access_time"]=access
                mkdict["creation_time"]=""
                mkdict["file_size"]=data_size
                mkdict["file_path"]=file_path
                mkdict["expiry_time"]=expiry
                mkdict["last_modified_time"]=last_modify
                mkdict["server_info"]=status
                self.cache_list.append(mkdict)

        def get_info(self):
            return self.cache_list

    class Cookie:
        def __init__(self, file, hash_v):
            self.file = file
            self.conn = sqlite3.connect(self.file)
            self.cookie_list = []
            if self.__parse() == -1:
                self.cookie_list == ""
            self.__sort()
            self.__hash_value = [hash_v]
            self.__path = file
            self.__cal_hash()

        def __parse(self):
            self.cookie_list = []
            try:
                cookies_cursor = self.conn.cursor()
                cookies_cursor_row = self.conn.cursor()
            except:
                print("please check your file")
                return -1
            try:
                cookies_open = cookies_cursor.execute("SELECT * FROM cookies")
            except:
                print("This file does not have such tables")
                return -1
            cookies_get_row = sqlite_get_schema("cookies", cookies_cursor_row)

            for row in cookies_get_row:
                if row[1] == "name":
                    name = row[0]
                elif row[1] == "value":
                    value = row[0]
                elif row[1] == "creation_utc":
                    creation_utc = row[0]
                elif row[1] == "last_access_utc":
                    last_access_utc = row[0]
                elif row[1] == "expires_utc":
                    expires_utc = row[0]
                elif row[1] == "host_key":
                    host_key = row[0]
                elif row[1] == "path":
                    cookie_path = row[0]
                elif row[1] == "secure" or row[1] == "is_secure":
                    secure = row[0]
                elif row[1] == "httponly" or row[1] == "is_httponly":
                    httponly = row[0]

            no = 0
            for cookie in cookies_open:
                no += 1
                mkdict = dict()
                mkdict["index"] = no
                mkdict["type"] = "cookies"
                mkdict["browser"] = "chrome"
                mkdict["timezone"]="UTC"
                mkdict["name"] = cookie[name]
                mkdict["value"] = cookie[value]
                mkdict["creation_time"] = int2date1(cookie[creation_utc])
                mkdict["last_accessed_time"] = int2date1(cookie[last_access_utc])
                mkdict["expiry_time"] = int2date1(cookie[expires_utc])
                mkdict["host"] = cookie[host_key]
                mkdict["path"] = cookie[cookie_path]
                mkdict["is_secure"] = cookie[secure]
                mkdict["is_httponly"] = cookie[httponly]

                self.cookie_list.append(mkdict)

        def get_info(self):
            return self.cookie_list

        def __sort(self):
            self.cookie_list=time_sort('creation_time', self.cookie_list)

        def time_sort(self, key):
            date_list=self.cookie_list
            sort_date = time_sort(key, date_list)
            return sort_date

        def __cal_hash(self):
            self.__hash_value.append(calc_hash.get_hash(self.__path))

        def get_hash(self):
            return self.__hash_value


class Firefox:
    class History:
        def __init__(self, file, hash_v):
            self.file = file
            self.conn = sqlite3.connect(self.file)
            self.history_list=[]
            if self.__parse() == -1:
                self.history_list == ""
            self.__sort()
            self.__hash_value = [hash_v]
            self.__path = file
            self.__cal_hash()

        def __parse(self):
            try:
                visits_cursor = self.conn.cursor()
            except:
                print("please check your file")
                return -1
            try:
                visits_open = visits_cursor.execute("SELECT moz_places.title, moz_places.url,moz_historyvisits.from_visit,moz_historyvisits.visit_date,moz_places.visit_count,moz_historyvisits.visit_type FROM moz_historyvisits, moz_places WHERE moz_places.id = moz_historyvisits.place_id")
            except:
                print("This file does not have such tables")
                return -1
            no = 0
            for visit in visits_open:
                no += 1
                mkdict = dict()
                mkdict["index"] = no
                mkdict["type"] = "history"
                mkdict["browser"] = "firefox"
                mkdict["timezone"] = "UTC"
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

        def __cal_hash(self):
            self.__hash_value.append(calc_hash.get_hash(self.__path))

        def get_hash(self):
            return self.__hash_value

    class Cookie:
        def __init__(self, file, hash_v):
            self.file = file
            self.conn = sqlite3.connect(self.file)
            self.cookie_list=[]
            if self.__parse() == -1:
                self.cookie_list == ""
            self.__sort()
            self.__hash_value = [hash_v]
            self.__path = file
            self.__cal_hash()

        def __parse(self):
            try:
                cookies_cursor = self.conn.cursor()
                cookies_cursor_row = self.conn.cursor()
            except:
                print("please check your file")
                return -1
            try:
                cookies_open = cookies_cursor.execute("SELECT * FROM moz_cookies")
            except:
                print("This file does not have such tables")
                return -1

            cookies_get_row = sqlite_get_schema("moz_cookies", cookies_cursor_row)

            for row in cookies_get_row:
                if row[1] == "name":
                    name = row[0]
                elif row[1] == "value":
                    value = row[0]
                elif row[1] == "creationTime":
                    creationTime = row[0]
                elif row[1] == "lastAccessed":
                    lastAccessed = row[0]
                elif row[1] == "expiry":
                    expiry = row[0]
                elif row[1] == "host":
                    host = row[0]
                elif row[1] == "path":
                    cookie_path = row[0]
                elif row[1] == "secure" or row[1] == "isSecure":
                    isSecure = row[0]
                elif row[1] == "isHttpOnly" or row[1] == "is_httponly":
                    httponly = row[0]

            no = 0
            for cookie in cookies_open:
                no += 1
                mkdict = dict()
                mkdict["index"] = no
                mkdict["type"] = "cookies"
                mkdict["browser"] = "firefox"
                mkdict["timezone"] = "UTC"
                mkdict["name"] = cookie[name]
                mkdict["value"] = cookie[value]
                mkdict["creation_time"] = cookie[creationTime]
                mkdict["last_accessed_time"] = cookie[lastAccessed]
                mkdict["expiry_time"] = cookie[expiry]
                mkdict["host"] = cookie[host]
                mkdict["path"] = cookie[cookie_path]
                mkdict["is_secure"] = cookie[isSecure]
                mkdict["is_httponly"] = cookie[httponly]
                self.cookie_list.append(mkdict)

        def get_info(self):
            return self.cookie_list

        def __sort(self):
            self.cookie_list=time_sort('creation_time', self.cookie_list)

        def time_sort(self, key):
            data_list = self.cookie_list
            data_list=time_sort(key, data_list)
            return data_list

        def __cal_hash(self):
            self.__hash_value.append(calc_hash.get_hash(self.__path))

        def get_hash(self):
            return self.__hash_value

    class Download:
        def __init__(self, file, hash_v):
            self.file = file
            self.conn = sqlite3.connect(self.file)
            self.download_list = []
            if self.__parse() == -1:
                self.download_list == ""
            self.__sort()
            self.__hash_value = [hash_v]
            self.__path = file
            self.__cal_hash()

        def __parse(self):
            try:
                moz_places_cursor = self.conn.cursor()
            except:
                print("please check your file")
                return -1
            try:
                place_id_open = moz_places_cursor.execute("SELECT moz_historyvisits.place_id FROM moz_historyvisits WHERE moz_historyvisits.visit_type=7")
            except:
                print("This file does not have such tables")
                return -1
            no = 0
            for moz_place in place_id_open:
                no += 1
                mkdict = dict()
                mkdict["index"] = no
                mkdict["type"] = "downloads"
                mkdict["browser"] = "firefox"
                mkdict["timezone"] = "UTC"
                try:
                    downloads_cursor = self.conn.cursor()
                    downloads_open = downloads_cursor.execute("SELECT moz_annos.anno_attribute_id, moz_annos.content,moz_annos.dateAdded FROM moz_annos WHERE moz_annos.place_id=" + str(moz_place[0])).fetchall()
                    anno_attribute_cursor = self.conn.cursor()
                    anno_attribute_open = anno_attribute_cursor.execute("SELECT moz_anno_attributes.* FROM moz_anno_attributes")
                except:
                    print("This file does not have such tables")
                    return -1
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
                try:
                    url_guid = url_guid_cursor.execute("SELECT moz_places.url, moz_places.guid FROM moz_places WHERE moz_places.id=" + str(moz_place[0])).fetchone()
                except:
                    print("This file does not have such tables")
                    return -1
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

        def __cal_hash(self):
            self.__hash_value.append(calc_hash.get_hash(self.__path))

        def get_hash(self):
            return self.__hash_value


class Ie_Edge:
    class Cache:
        def __init__(self, file, path,hash_v):
            self.file = file
            self.cache_list = []
            if self.file==-1:
                self.cache_list == ""
            else:
                self.__parse()
            self.__sort()
            self.__hash_value = [hash_v]
            self.__path = path
            self.__cal_hash()

        def __parse(self):
            cache_noContainer = []  # 없는 container 저장하는 list
            cache_emptyContainer = []  # 빈 container 저장하는 list
            cache_container_id = get_ContainerID(self.file, "Content")
            no = 0
            for containerid in cache_container_id.keys():
                col_name = esedb_get_schema(self.file, containerid)
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
                    mkdict["timezone"] = "UTC"
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
                    try:
                        if cache.get_value_data(21) is not None:
                            mkdict["server_info"] = cache.get_value_data(21).decode().split(" ")[1]
                        else:
                            mkdict["server_info"] = ""
                    except:
                        mkdict["server_info"]=""
                    self.cache_list.append(mkdict)

        def get_info(self):
            return self.cache_list

        def __sort(self):
            self.cache_list=time_sort('creation_time', self.cache_list)

        def time_sort(self, key):
            data_list = self.cache_list
            data_list=time_sort(key, data_list)
            return data_list

        def __cal_hash(self):
            self.__hash_value.append(calc_hash.get_hash(self.__path))

        def get_hash(self):
            return self.__hash_value

    class Cookie:
        def __init__(self, file, path,hash_v):
            self.file = file
            self.cookie_list=[]
            if self.file == -1:
                self.cookie_list == ""
            else:
                self.__parse()
            self.__sort()
            self.__hash_value = [hash_v]
            self.__path = path
            self.__cal_hash()

        def __parse(self):
            cookies_no_container = []  # 없는 container 저장하는 list
            cookies_empty_container = []  # 빈 container 저장하는 list
            cookies_container_id = get_ContainerID(self.file, "Cookies")
            no = 0
            for containerid in cookies_container_id.keys():
                col_name = esedb_get_schema(self.file, containerid)
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
                    mkdict["timezone"] = "UTC"
                    mkdict["name"] = cookie.get_value_data_as_string(18)
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

        def __cal_hash(self):
            self.__hash_value.append(calc_hash.get_hash(self.__path))

        def get_hash(self):
            return self.__hash_value

    class Download:
        def __init__(self, file, path, hash_v):
            self.file = file
            self.download_list=[]
            if self.file == -1:
                self.download_list == ""
            else:
                self.__parse()
            self.__sort()
            self.__hash_value = [hash_v]
            self.__path = path
            self.__cal_hash()

        def __parse(self):
            downloads_no_container = []  # 없는 container 저장하는 list
            downloads_empty_container = []  # 빈 container 저장하는 list
            downloads_container_id = get_ContainerID(self.file, "iedownload")
            no = 0
            for containerid in downloads_container_id.keys():
                col_name = esedb_get_schema(self.file, containerid)
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
                    mkdict["timezone"] = "UTC"
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
                    except:
                        pass
                    try:
                        data = bytes.decode(binascii.hexlify(binary_data[0x148:]))
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

                    self.download_list.append(mkdict)

        def get_info(self):
            return self.download_list

        def __sort(self):
            self.download_list=time_sort('download_start_time', self.download_list)

        def time_sort(self,key):
            data_list = self.download_list
            data_list=time_sort(key, data_list)
            return data_list

        def __cal_hash(self):
            self.__hash_value.append(calc_hash.get_hash(self.__path))

        def get_hash(self):
            return self.__hash_value

    class History:
        def __init__(self, file, path,hash_v):
            self.file = file
            self.history_list=[]
            if self.file == -1:
                self.history_list == ""
            else:
                self.__parse()
            self.__sort()
            self.__hash_value = [hash_v]
            self.__path = path
            self.__cal_hash()

        def __parse(self):
            history_no_container = []  # 없는 container 저장하는 list
            history_empty_container = []  # 빈 container 저장하는 list

            history_container_id = get_ContainerID(self.file, "Hist")
            no = 0
            for containerid in history_container_id.keys():
                col_name = esedb_get_schema(self.file,containerid)
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
                    mkdict["timezone"] = "UTC"
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
            return result

        def __cal_hash(self):
            self.__hash_value.append(calc_hash.get_hash(self.__path))

        def get_hash(self):
            return self.__hash_value

# chrome change int to date
def int2date1(date_time):
    # 1601년 1월 1일부터
    from_date = datetime.datetime(1601, 1, 1)
    passing_time = timedelta(microseconds=date_time)
    get_date = from_date+passing_time
    return get_date.strftime("%Y-%m-%d %H:%M:%S")

# firefox change int to date
def int2date2(date_time):
    # 1970년 1월 1일부터
    get_date=datetime.datetime.fromtimestamp(date_time / 1000000)
    return get_date.strftime("%Y-%m-%d %H:%M:%S")

# firefox change int to date
def int2date3(date_time):
    # 1970년 1월 1일부터
    get_date=datetime.datetime.fromtimestamp(date_time / 1000)
    return get_date.strftime("%Y-%m-%d %H:%M:%S")

# IE_Edge change in to date
def int2date4(date_time):
    # 1601년 1월 1일부터
    try:
        from_date = datetime.datetime(1601, 1, 1)
        passing_time = timedelta(microseconds=(date_time*0.1))
        get_date = from_date + passing_time
        return get_date.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return 0

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

# get schema of sqlite db
def sqlite_get_schema(table, cursor):
    col_infos = []
    query = 'PRAGMA table_info(' + table + ')'
    n = 0
    for info in cursor.execute(query):
        col_infos.append((n, info[1], info[2]))
        n += 1
    cursor.close()
    return col_infos

# column name and type of IE_Edge
def esedb_get_schema(file, table):
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
