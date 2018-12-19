import mysql.connector
import config


def makedatabase():
	mydb = mysql.connector.connect(host=config.Config.MYSQL_DATABASE_HOST,user=config.Config.MYSQL_DATABASE_USER,passwd=config.Config.MYSQL_DATABASE_PASSWORD)
	mycursor = mydb.cursor()
	mycursor.execute('CREATE DATABASE Artemis;USE Artemis;')
	fin = open('databasecode.txt','r')
	mycursor.execute(fin)
