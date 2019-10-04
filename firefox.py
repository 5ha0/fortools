import sqlite3

def firefox_open(path):
    open_firefox_file = open(path, "rb")
    format=open_firefox_file.read(15).decode()

    if format=="SQLite format 3":
        conn=sqlite3.connect(path)
        db_cursor=conn.cursor()
        return db_cursor
    else:
        return open_firefox_file   