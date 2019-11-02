import json
import sqlite3
import win32crypt #pip install pywin32
import pyesedb
import binascii
import base64
from datetime import *


class Chrome:
    def __init__(self, file):
        self.file = file
        self.conn = sqlite3.connect(self.file)

    def __int2date(self,time):
        #1601년 1월 1일부터
        from_date=datetime(1601,1,1)
        passing_time=timedelta(microseconds=time)
        get_date=from_date+passing_time
        return get_date.strftime("%Y-%m-%d %H:%M:%S")

    def cache(self):
        pass

    def cookies(self):
        cookies_cursor = self.conn.cursor()
        cookies = []
        cookies_open = cookies_cursor.execute("SELECT * FROM cookies")
        no = 0
        for cookie in cookies_open:
            no += 1
            mkdict = dict()
            mkdict["type"] = "cookies"
            mkdict["browser"] = "chrome"
            mkdict["name"]=cookie[2]
            mkdict["value"]=cookie[3]
            mkdict["creation_time"]=self.__int2date(cookie[0])
            mkdict["last_accessed_time"]=self.__int2date(cookie[8])
            mkdict["expiry_time"]=self.__int2date(cookie[5])
            mkdict["host"]=cookie[1]
            mkdict["path"]=cookie[4]
            mkdict["is_secure"]=cookie[6]
            mkdict["is_httponly"]=cookie[7]

            mkdictno = dict()
            mkdictno["no" + str(no)] = mkdict
            cookies.append(mkdictno)
        print(json.dumps(cookies,indent=4))

    def history(self):
        history=[]
        history_cursor=self.conn.cursor()
        visits_open=history_cursor.execute("SELECT visits.from_visit, visits.visit_time, visits.transition, urls.url, urls.title, urls.visit_count, urls.id FROM urls, visits WHERE urls.id = visits.url")
        no=0
        for visit in visits_open:
            no += 1
            mkdict = dict()
            mkdict["type"] = "history"
            mkdict["browser"] = "chrome"
            mkdict["title"]=visit[4]
            mkdict["url"]=visit[3]
            if visit[0]==0:
                mkdict["from_visit"]=visit[0]
            else:
                from_visit_cursor = self.conn.cursor()
                get_url_cursor=self.conn.cursor()
                url_id=from_visit_cursor.execute("SELECT visits.url FROM visits WHERE visits.id="+str(visit[0])).fetchone()[0]
                mkdict["from_visit"]=get_url_cursor.execute("SELECT urls.url FROM urls WHERE urls.id="+ str(url_id)).fetchone()[0]
            keyword_cursor = self.conn.cursor()
            mkdict["keyword_search"]=keyword_cursor.execute("SELECT keyword_search_terms.term FROM keyword_search_terms WHERE keyword_search_terms.url_id= "+ str(visit[6])).fetchall()
            if mkdict["keyword_search"]== []:
                mkdict["keyword_search"]= ""
            mkdict["visit_time"]=self.__int2date(visit[1])
            mkdict["visit_count"]=visit[5]
            mkdict["visit_type"]=visit[2]

            mkdictno = dict()
            mkdictno["no" + str(no)] = mkdict
            history.append(mkdictno)
        print(json.dumps(history,indent=4))

    def downloads(self):
        downloads = []
        downloads_cursor = self.conn.cursor()
        downloads_open = downloads_cursor.execute("SELECT downloads.* FROM downloads")
        no = 0
        for download in downloads_open:
            no += 1
            mkdict = dict()
            mkdict["type"] = "downloads"
            mkdict["browser"] = "chrome"
            mkdict["file_name"] = download[3].split("\\")[-1]
            mkdict["download_path"] = download[2]
            mkdict["download_start_time"] = self.__int2date(download[4])
            mkdict["download_end_time"] = self.__int2date(download[11])
            mkdict["file_size"] = download[6]
            downloads_url_chains_cursor = self.conn.cursor()
            mkdict["url"] = downloads_url_chains_cursor.execute("SELECT downloads_url_chains.chain_index,downloads_url_chains.url FROM downloads_url_chains WHERE downloads_url_chains.id=" + str(download[0])).fetchall()
            mkdict["guid"] = download[1]
            mkdict["opened"] = download[12]
            mkdict["state"] = download[7]

            mkdictno = dict()
            mkdictno["no" + str(no)] = mkdict
            downloads.append(mkdictno)
        print(json.dumps(downloads, indent=4))


class Firefox:
    def __init__(self, file):
        self.file = file
        self.conn = sqlite3.connect(self.file)

    def __int2date1(self,time):
        #1970년 1월 1일부터
        get_date=datetime.fromtimestamp(time / 1000000)
        return get_date.strftime("%Y-%m-%d %H:%M:%S")

    def __int2date2(self,time):
        #1970년 1월 1일부터
        get_date=datetime.fromtimestamp(time / 1000)
        return get_date.strftime("%Y-%m-%d %H:%M:%S")

    def cache(self):
        pass

    def cookies(self):
        cookies_cursor = self.conn.cursor()
        cookies = []
        cookies_open = cookies_cursor.execute("SELECT * FROM moz_cookies")
        no = 0
        for cookie in cookies_open:
            no += 1
            mkdict = dict()
            mkdict["type"] = "cookies"
            mkdict["browser"] = "firefox"
            mkdict["name"] = cookie[3]
            mkdict["value"] = cookie[4]
            mkdict["creation_time"] = self.__int2date1(cookie[9])
            mkdict["last_accessed_time"] = self.__int2date1(cookie[8])
            mkdict["expiry_time"] =self.__int2date2(cookie[7])
            mkdict["host"] = cookie[5]
            mkdict["path"] = cookie[6]
            mkdict["is_secure"] = cookie[10]
            mkdict["is_httponly"] = cookie[11]
            mkdictno = dict()
            mkdictno["no" + str(no)] = mkdict
            cookies.append(mkdictno)
        print(json.dumps(cookies, indent=4))

    def history(self):
        history = []
        visits_cursor = self.conn.cursor()
        visits_open = visits_cursor.execute("SELECT moz_places.title, moz_places.url,moz_historyvisits.from_visit,moz_historyvisits.visit_date,moz_places.visit_count,moz_historyvisits.visit_type FROM moz_historyvisits, moz_places WHERE moz_places.id = moz_historyvisits.place_id")
        no = 0
        for visit in visits_open:
            no += 1
            mkdict = dict()
            mkdict["type"] = "history"
            mkdict["browser"] = "firefox"
            mkdict["title"] = visit[0]
            mkdict["url"] = visit[1]
            if visit[2] == 0:
                mkdict["from_visit"] = visit[2]
            else:
                from_visit_cursor = self.conn.cursor()
                get_url_cursor = self.conn.cursor()
                print(visit[2])
                url_id = from_visit_cursor.execute("SELECT moz_historyvisits.place_id FROM moz_historyvisits WHERE moz_historyvisits.id=" + str(visit[2])).fetchone()[0]
                mkdict["from_visit"] = get_url_cursor.execute("SELECT moz_places.url FROM moz_places WHERE moz_places.id=" + str(url_id)).fetchone()[0]

            mkdict["keyword_search"] = ""
            mkdict["visit_time"] = self.__int2date1(visit[3])
            mkdict["visit_count"] = visit[4]
            mkdict["visit_type"] = visit[5]

            mkdictno = dict()
            mkdictno["no" + str(no)] = mkdict
            history.append(mkdictno)
        print(json.dumps(history, indent=4))

    def downloads(self):
        downloads = []
        moz_places_cursor=self.conn.cursor()
        place_id_open = moz_places_cursor.execute("SELECT moz_historyvisits.place_id FROM moz_historyvisits WHERE moz_historyvisits.visit_type=7")
        no = 0
        for moz_place in place_id_open:
            no += 1
            mkdict = dict()
            mkdict["type"] = "downloads"
            mkdict["browser"] = "firefox"
            downloads_cursor = self.conn.cursor()
            downloads_open=downloads_cursor.execute("SELECT moz_annos.anno_attribute_id, moz_annos.content,moz_annos.dateAdded FROM moz_annos WHERE moz_annos.place_id="+str(moz_place[0])).fetchall()
            anno_attribute_cursor=self.conn.cursor()
            anno_attribute_open=anno_attribute_cursor.execute("SELECT moz_anno_attributes.* FROM moz_anno_attributes")
            for anno_attribute in anno_attribute_open:
                for i in range (0,len(downloads_open)):
                    if anno_attribute[0]==downloads_open[i][0]:
                        if anno_attribute[1]=="downloads/destinationFileURI":
                            mkdict["file_name"] = downloads_open[i][1].split('/')[-1]
                            mkdict["download_path"]= downloads_open[i][1]
                            mkdict["download_start_time"] = self.__int2date1(downloads_open[i][2])
                        elif anno_attribute[1]=="downloads/metaData":
                            tempdict=eval(downloads_open[i][1])
                            mkdict["download_end_time"] =self.__int2date2(tempdict["endTime"])
                            mkdict["file_size"] = tempdict["fileSize"]
            url_guid_cursor= self.conn.cursor()
            url_guid=url_guid_cursor.execute("SELECT moz_places.url, moz_places.guid FROM moz_places WHERE moz_places.id="+str(moz_place[0])).fetchone()
            mkdict["url"] = url_guid[0]
            mkdict["guid"] = url_guid[1]
            mkdict["opened"] = ""
            mkdict["state"] = ""

            mkdictno = dict()
            mkdictno["no" + str(no)] = mkdict
            downloads.append(mkdictno)
        print(json.dumps(downloads, indent=4))


class Ie_Edge:
    def __init__(self, file):
        self.file = file

    def __get_ContainerID(self,group):
        ContainerID = dict()
        Containers = self.file.get_table_by_name("Containers")
        for record in Containers.records:
            if record.get_value_data_as_string(8) == group:
                #containerid랑directory
                ContainerID["Container_" + str(record.get_value_data_as_integer(0))] = record.get_value_data_as_string(10)
        print("a",ContainerID)
        return ContainerID

    #column이름이랑 형식
    def __get_schema(self, table):
        col_infos=[]
        get_container = self.file.get_table_by_name(table)
        if get_container == None: #container가 없을 때
            return get_container
        for column in get_container.columns:
            col_info = []
            col_info.append(column.name)
            col_info.append(column.get_type())
            col_infos.append(col_info)
        print(table)
        print(col_infos)
        return col_infos

    def __int2date(self, time):
        # 1601년 1월 1일부터
        from_date = datetime(1601, 1, 1)
        passing_time = timedelta(microseconds=(time/10))
        get_date = from_date + passing_time
        return get_date.strftime("%Y-%m-%d %H:%M:%S")


#     def cache(self):
#         cache=[]
#         cache_container_id= self.__get_ContainerID("Content")
#         no = 1
#         for containerid in cache_container_id.keys():
#             col_name = self.__get_schema(containerid)
#             cache_container = self.file.get_table_by_name(containerid)
#             if col_name == None: continue #없는경우

#             mkdict = dict()
#             mkdict["group"] = "cache"
#             mkdict["browser"] = "IE10+ Edge"
#             mkdict["containerid"]=containerid
#             if (cache_container.number_of_records == 0):
#                 mkdict["containerEmpty"] = 0
#             else:
#                 mkdict["containerEmpty"] = 0
#             for row in cache_container.records:
#                 for i in range(0, len(col_name)):
#                     if row.get_value_data(i)==None:
#                         mkdict[col_name[i][0]]=None
#                     else:  mkdict[col_name[i][0]] = str(row.get_value_data(i))
#             mkdictno = dict()
#             mkdictno["no" + str(no)] = mkdict
#             cache.append(mkdictno)
#             no += 1
#         print(json.dumps(cache,indent=4))

    def cookies(self):
        cookies=[]
        cookies_noContainer=[]#없는 container 저장하는 list
        cookies_emptyContainer=[]#빈 container 저장하는 list
        cookies_container_id = self.__get_ContainerID("Cookies")
        no=0
        for containerid in cookies_container_id.keys():
            col_name=self.__get_schema(containerid)
            cookies_container = self.file.get_table_by_name(containerid)
            if col_name==None:
                cookies_noContainer.append(containerid)
                continue
            if (cookies_container.number_of_records == 0):
                cookies_emptyContainer.append(containerid)
                continue
            for cookie in cookies_container.records:
                no += 1
                mkdict = dict()
                mkdict["type"] = "cookies"
                mkdict["browser"] = "IE10+ Edge"
                mkdict["name"] = cookie.get_value_data_as_stirng(18)
                mkdict["value"] = ""
                mkdict["creation_time"] = self.__int2date(cookie.get_value_data_as_integer(10))
                mkdict["last_accessed_time"] = self.__int2date(cookie.get_value_data_as_integer(13))
                mkdict["expiry_time"] = self.__int2date(cookie.get_value_data_as_integer(11))
                mkdict["host"] = cookie.get_value_data_as_string(17)
                mkdict["path"] = ""
                mkdict["is_secure"] = ""
                mkdict["is_httponly"] = ""

                mkdictno = dict()
                mkdictno["no" + str(no)] = mkdict
                cookies.append(mkdictno)

        print(cookies_noContainer)
        print(cookies_emptyContainer)
        print(cookies)

    def history(self):
        history=[]
        history_noContainer=[]
        history_emptyContainer=[]
        history_container_id= self.__get_ContainerID("History")
        no = 0
        for containerid in history_container_id.keys():
            col_name = self.__get_schema(containerid)
            history_container = self.file.get_table_by_name(containerid)

            if col_name == None:
                history_noContainer.append(containerid)
                continue
            if (history_container.number_of_records == 0):
                history_emptyContainer.append(containerid)
                continue

            for visit in history_container.records:
                no += 1
                mkdict = dict()
                mkdict["type"] = "history"
                mkdict["browser"] = "IE10+ Edge"
                mkdict["title"] = str(visit.get_value_data(21))
                mkdict["url"] = visit.get_value_data_as_string(17)
                mkdict["from_visit"] = ""
                mkdict["keyword_search"] = ""
                mkdict["visit_time"] = self.__int2date(visit.get_value_data_as_integer(13))
                mkdict["visit_count"] = visit.get_value_data_as_integer(8)
                mkdict["visit_type"] = ""

                mkdictno = dict()
                mkdictno["no" + str(no)] = mkdict
                history.append(mkdictno)
        print(json.dumps(history, indent=4))
        print(history_noContainer)
        print(history_emptyContainer)

    def downloads(self):
       downloads = []
       downloads_noContainer = []
       downloads_emptyContainer = []
       downloads_container_id= self.__get_ContainerID("iedownload")
       no = 0
       for containerid in downloads_container_id.keys():
           col_name = self.__get_schema(containerid)
           downloads_container = self.file.get_table_by_name(containerid)
           if col_name == None:
               downloads_noContainer.append(containerid)
               continue
           if (downloads_container.number_of_records == 0):
               downloads_emptyContainer.append(containerid)
               continue

           for download in downloads_container.records:
               no+=1
               mkdict = dict()
               mkdict["type"] = "download"
               mkdict["browser"] = "IE10+ Edge"

               mkdict["file_name"] = str(download.get_value_data(21))
               mkdict["download_path"] = str(download.get_value_data(21))
               mkdict["download_start_time"] = self.__int2date(download.get_value_data_as_integer(13))
               mkdict["download_end_time"] = ""
               mkdict["file_size"] = str(download.get_value_data(21))
               mkdict["url"] = str(download.get_value_data(21))
               mkdict["guid"] = download.get_value_data_as_string(17)
               mkdict["opened"] = ""
               mkdict["state"] = ""

               mkdictno = dict()
               mkdictno["no" + str(no)] = mkdict
               downloads.append(mkdictno)
       print(json.dumps(downloads, indent=4))
       print(downloads_noContainer)
       print(downloads_emptyContainer)



class Favorite:
    def common(self):
        pass

    def keyword_search(self):
        pass

    def timeline(self):
        pass
