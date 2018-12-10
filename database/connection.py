import sqlite3

conn = sqlite3.connect('da1.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE user (fname TEXT, lname TEXT, age INT, email TEXT, password TEXT)')
print ("Table created successfully")
conn.close()
