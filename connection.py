import sqlite3
import config
conn=sqlite3.connect(config._DB)

c = conn.cursor()
c.execute("INSERT INTO users VALUES (:Bname, :web, :number, :contact, :cnumber)"
c.fetchall()

conn.commit()
