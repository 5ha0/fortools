import sqlite3

def chrome_open(path):
    open_chrome_file = open(path, "rb")
    format=open_chrome_file.read(15).decode()

    if format=="SQLite format 3":
        conn=sqlite3.connect(path)
        db_cursor=conn.cursor()
        return db_cursor
    else:
        return open_chrome_file
