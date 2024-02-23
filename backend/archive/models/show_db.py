import sqlite3


conn = sqlite3.connect(
    r'D:\Dropbox\programing\MyPython\futures_curve_cme\app\src\tools\models\data.db')
c = conn.cursor()

c.execute("SELECT * FROM sqlite_master where type='table'")
for row in c.fetchall():
    print(row)

c.execute("SELECT * FROM crude_oil")
for row in c.fetchall():
    print(row)

c.close()
conn.close()
