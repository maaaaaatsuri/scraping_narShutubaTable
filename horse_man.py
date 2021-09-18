

import sqlite3
from contextlib import closing

with closing(sqlite3.connect('Horse_man.db')) as db_connect:
    db_curs = db_connect.cursor()
    sql = 'SELECT * FROM test001'
    db_curs.execute(sql)

    print(db_curs.fetchall())


























