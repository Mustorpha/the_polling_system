"""Import all the database scheema and
data stored from a SQL dump file (.sql...)
into a sqlite db using the sqlite3 module
"""

import sqlite3

conn = sqlite3.connect("db.sqlite3")

cur = conn.cursor

with open('bincom_test.sql') as dump_file:
    sql = dump_file.read()

cur.executrscript(sql)
conn.commit()
conn.close()


# Run `Python manage.py inspectdb > collation/models.py`
# To generate the django model classes for the imported
# databse schema
