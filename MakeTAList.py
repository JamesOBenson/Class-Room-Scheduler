import csv
import sqlite3 as sql
import subprocess #Calls next python script.

# This file creates the DB and the tables used in the query's for scheduling.
# If the table exists it will delete old tables.
#
# python MakeTAList.py

con = sql.connect('TAList.db')
cur = con.cursor() 
semester = ""
print("Note: If the semester already exists it will be deleted.")
semester = input('Please enter the semester (F14, S14, S2014)')
cur.execute("DROP TABLE IF EXISTS %s" %semester)
cur.execute("CREATE TABLE %s (CRN INTEGER UNIQUE PRIMARY KEY,Subject TEXT,Course TEXT,Section INTEGER,Title TEXT,MeetingDays TEXT,StartTime TEXT, EndTime TEXT,Location, SetTA TEXT);" % semester) #CRN,Subject,Course,Section,Title,Meeting Days,Times,Location, SetTA


with open('result.csv', 'r') as res:
	reader = csv.reader(res)
	columns = next(reader)
	query = 'INSERT INTO %s({0}) VALUES ({1})' %semester
	query = query.format(','.join(columns), ','.join('?' * len(columns)))
	for data in reader:
		cur.execute(query, data)
	con.commit()

print("Class DB is complete")	
#Name, Busy1Day, BusyStart1, BusyEnd1, Busy2Day, BusyStart2, BusyEnd2, Busy3Day, BusyStart3, BusyEnd3, Busy4Day, BusyStart4, BusyEnd4,Busy5Day, BusyStart5, BusyEnd5, Busy6Day, BusyStart6, BusyEnd6, Busy7Day, BusyStart7, BusyEnd7, Busy8Day, BusyStart8, BusyEnd8

cur.execute("DROP TABLE IF EXISTS %sTA" %semester)
cur.execute("CREATE TABLE %sTA (Name TEXT, Busy1Day TEXT, BusyStart1 TEXT, BusyEnd1 TEXT, Busy2Day TEXT, BusyStart2 TEXT, BusyEnd2 TEXT, Busy3Day TEXT, BusyStart3 TEXT, BusyEnd3 TEXT, Busy4Day TEXT, BusyStart4 TEXT, BusyEnd4 TEXT,Busy5Day TEXT, BusyStart5 TEXT, BusyEnd5 TEXT, Busy6Day TEXT, BusyStart6 TEXT, BusyEnd6 TEXT, Busy7Day TEXT, BusyStart7 TEXT, BusyEnd7 TEXT, Busy8Day TEXT, BusyStart8 TEXT, BusyEnd8 TEXT, nTeaching INTEGER DEFAULT 0);" % semester)   #CRN,Subject,Course,Section,Title,Meeting Days,Times,Location
with open('demoTAList.CSV', 'r') as res:
	reader = csv.reader(res)
	columns = next(reader)
	query = 'INSERT INTO %sTA({0}) VALUES ({1})' %semester
	query = query.format(','.join(columns), ','.join('?' * len(columns)))
	for data in reader:
		cur.execute(query, data)
	con.commit()
con.close()

print("TA DB is complete")
subprocess.call("python 3Possibilities.py "+ semester, shell = True)
#subprocess.Popen(["python", "3Possibilities.py", semester])