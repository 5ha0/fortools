import json
import sqlite3
import win32crypt #pip install pywin32
import binascii


#time수정필요->int2datetime
class Chrome:
    def __init__(self, file):
        self.file = file
        self.conn = sqlite3.connect(self.file)

    def __get_schema(self,table,cursor):
        col_info=[]
        query='PRAGMA table_info(' +table+')'
        for info in cursor.execute(query):
            col_info.append((info[1], info[2]))
        return col_info

    def urls(self):
        urls_cursor = self.conn.cursor()
        urls=[]
        col_name=self.__get_schema("urls", urls_cursor)
        urls_open=urls_cursor.execute("SELECT * FROM urls")
        no=0
        for url in urls_open:
            no += 1
            mkdict=dict()
            mkdict["type"]="url"
            mkdict["browser"]="chrome"
            for i in range (0,len(col_name)):
                mkdict[col_name[i][0]] = url[i]
            mkdictno = dict()
            mkdictno["no" + str(no)] = mkdict
            urls.append(mkdict)
        print("urls")
        print(urls)

    def cookies(self):
        cookies_cursor = self.conn.cursor()
        cookies = []
        col_name = self.__get_schema("cookies", cookies_cursor)
        cookies_open = cookies_cursor.execute("SELECT * FROM cookies")
        no = 0
        for cookie in cookies_open:
            no += 1
            mkdict = dict()
            mkdict["type"] = "cookies"
            mkdict["browser"] = "chrome"
            for i in range(0, len(col_name)):
                if col_name[i][0] == "encrypted_value":
                    mkdict[col_name[i][0]] = win32crypt.CryptUnprotectData(cookie[i], None, None, None, 0)[1].decode()
                else: mkdict[col_name[i][0]] = cookie[i]
            mkdictno = dict()
            mkdictno["no" + str(no)] = mkdict
            cookies.append(mkdictno)
        print("cookies")
        print(cookies)

    def visit_history(self):
        visits = []
        visits_cursor = self.conn.cursor()
        col_name = self.__get_schema("visits", visits_cursor)
        visits_open=visits_cursor.execute("SELECT visits.*, urls.url FROM urls, visits WHERE urls.id = visits.url")
        no=0
        for visit in visits_open:
            no += 1
            mkdict = dict()
            mkdict["type"] = "visits"
            mkdict["browser"] = "chrome"
            for i in range(0, len(col_name)):
                if col_name[i][0]=="url":
                    mkdict[col_name[i][0]] = visit[len(visit)-1]
                else: mkdict[col_name[i][0]] = visit[i]
            mkdictno = dict()
            mkdictno["no" + str(no)] = mkdict
            visits.append(mkdictno)
        print("visits")
        print(visits)

    def search_history(self):
        keyword_search_terms = []
        keyword_search_terms_cursor = self.conn.cursor()
        col_name = self.__get_schema("keyword_search_terms", keyword_search_terms_cursor)
        keyword_search_terms_open = keyword_search_terms_cursor.execute("SELECT keyword_search_terms.*, urls.url FROM urls, keyword_search_terms WHERE urls.id = keyword_search_terms.url_id")
        no = 0
        for keyword_search_term in keyword_search_terms_open:
            no += 1
            mkdict = dict()
            mkdict["type"] = "keyword_search_terms"
            mkdict["browser"] = "chrome"
            for i in range(0, len(col_name)):
                if col_name[i][0] == "url_id":
                    mkdict[col_name[i][0]] = keyword_search_term[len(keyword_search_term) - 1]
                else:
                    mkdict[col_name[i][0]] = keyword_search_term[i]
            mkdictno = dict()
            mkdictno["no" + str(no)] = mkdict
            keyword_search_terms.append(mkdictno)
        print("keyword_search_terms")
        print(keyword_search_terms)

    def downloads(self):
        downloads = []
        downloads_cursor = self.conn.cursor()
        col_name_downloads = self.__get_schema("downloads", downloads_cursor)
        col_name_chain = self.__get_schema("downloads_url_chains", downloads_cursor)
        downloads_open = downloads_cursor.execute("SELECT downloads.*, downloads_url_chains.* FROM downloads, downloads_url_chains WHERE downloads.id=downloads_url_chains.id")
        no = 1
        for download in downloads_open:
            if download[len(download)-len(col_name_chain)+1]==0:
                if no !=1:
                    downloads[no-2]["url_chain"]=temp
                mkdict = dict()
                mkdict["type"] = "downloads"
                mkdict["browser"] = "chrome"
                for i in range(0, len(col_name_downloads)):
                        mkdict[col_name_downloads[i][0]] = download[i]
                mkdictno = dict()
                mkdictno["no" + str(no)] = mkdict
                downloads.append(mkdictno)
                no += 1
                temp=dict()
            temp[download[len(download)-len(col_name_chain)+1]] = download[len(download)-len(col_name_chain)+2]
        downloads[no - 2]["url_chain"] = temp
        print("downloads")
        print(downloads)

    def cache(self):
        pass


    def login(self):
        login_open=self.__db_open("logins")
        json_list = []
        no = 0
        for row in login_open:
            no += 1
            mkdict = dict(row)
            mkdict["password_value"] = win32crypt.CryptUnprotectData(row['password_value'], None, None, None, 0)[1].decode()
            #mkdict["form_data"]=win32crypt.CryptUnprotectData(row['form_data'], None, None, None, 0)[1].decode()
            #mkdict["possible_username_pairs"]=win32crypt.CryptUnprotectData(row['possible_username_pairs'], None, None, None, 0)[1].decode()
            mkdictno = dict()
            mkdictno["no" + str(no)] = mkdict
            json_list.append(mkdictno)
        print("login")
        print(json_list)

    def session(self):
        pass


class Ie:
    def __init__(self, file):
        self.file = file


class Firefox:
    def __init__(self, file):
        self.file = file


class Edge:
    def __init__(self, file):
        self.file = file