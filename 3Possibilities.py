#
# Works only for F14 semester.  Hard coded in.
# To run: python 3Possibilities.py F14

import csv
import sqlite3 as sql
import operator
import sys
from operator import itemgetter

semester = sys.argv[1]

OrigTAs = ['Sushil', 'Clarissa', 'Anwar', 'Daniel', 'Brennan']
OrigCRNs = ['17381','17382','17384','17385','17387','17388','17398','17391','17389','18043']
print("\nTAs")
TAs = list(OrigTAs)

print(TAs)
		
qry = open('FindBusyTAs.sql', 'r').read()
conn = sql.connect('TAList.db')
print("\nOpened database successfully")
c = conn.cursor()
options = c.execute('''
SELECT name,CRN
	FROM %s INNER JOIN %sTA ON 
		(CAST(%s.StartTime as TIME) < CAST(%sTA.BusyEnd1 as TIME) and
		CAST(%s.EndTime as TIME)  >= CAST(%sTA.BusyStart1 as TIME) and
		%s.MeetingDays = %sTA.Busy1Day)

OR
		(CAST(%s.StartTime as TIME) < CAST(%sTA.BusyEnd2 as TIME) and
		CAST(%s.EndTime as TIME)  >= CAST(%sTA.BusyStart2 as TIME) and
		%s.MeetingDays =%sTA.Busy2Day)

OR
		(CAST(%s.StartTime as TIME) < CAST(%sTA.BusyEnd3 as TIME) and
		CAST(%s.EndTime as TIME)  >= CAST(%sTA.BusyStart3 as TIME) and
		%s.MeetingDays =%sTA.Busy3Day)

OR
		(CAST(%s.StartTime as TIME) < CAST(%sTA.BusyEnd4 as TIME) and
		CAST(%s.EndTime as TIME)  >= CAST(%sTA.BusyStart4 as TIME) and
		%s.MeetingDays =%sTA.Busy4Day)
OR
		(CAST(%s.StartTime as TIME) < CAST(%sTA.BusyEnd5 as TIME) and
		CAST(%s.EndTime as TIME)  >= CAST(%sTA.BusyStart5 as TIME) and
		%s.MeetingDays =%sTA.Busy5Day)
OR
		(CAST(%s.StartTime as TIME) < CAST(%sTA.BusyEnd6 as TIME) and
		CAST(%s.EndTime as TIME)  >= CAST(%sTA.BusyStart6 as TIME) and
		%s.MeetingDays =%sTA.Busy6Day)
OR
		(CAST(%s.StartTime as TIME) < CAST(%sTA.BusyEnd7 as TIME) and
		CAST(%s.EndTime as TIME)  >= CAST(%sTA.BusyStart7 as TIME) and
		%s.MeetingDays =%sTA.Busy7Day)
OR
		(CAST(%s.StartTime as TIME) < CAST(%sTA.BusyEnd8 as TIME) and
		CAST(%s.EndTime as TIME)  >= CAST(%sTA.BusyStart8 as TIME) and
		%s.MeetingDays =%sTA.Busy8Day)
		
		
''' % (semester, semester, semester, semester, semester, semester, semester, semester, semester, semester, semester, semester,semester, semester, semester, semester, semester, semester,semester, semester, semester, semester, semester, semester,semester, semester, semester, semester, semester, semester,semester, semester, semester, semester, semester, semester,semester, semester, semester, semester, semester, semester,semester, semester, semester, semester, semester, semester,semester, semester)  )

sqlList = c.fetchall()

for x in range(1,11,1):
	TAs = list(OrigTAs)
	#print(sqlList)   #DEBUG : TO SEE WHO LIST OF POSSIBLE TA'S UNABLE TO TEACH AND THE CORRESPONDING CRN NUMBERS.
	print("*********************************************************")
	print("\nTA & # of sections unable to teach:")
	dNoTeach = dict()
	for x in sqlList:
		key = x[0]
		if key in dNoTeach:
			dNoTeach[key] +=1
		else:
			dNoTeach[key] = 1
	for key, value in dNoTeach.items():
		print(str(key)+"\t"+str(value))

	print("\n\nCRN & # of TA's who can't teach it (5 = no one can teach, 0 = everyone can teach it):")
	dCRNNoTeach = dict()
	for x in sqlList:
		key = x[1]
		if key in dCRNNoTeach:
			dCRNNoTeach[key] +=1
		else:
			dCRNNoTeach[key] = 1
	for key, value in dCRNNoTeach.items():
		print(key, value)

	print("\n\nCRN with fewest available TAs who can teach")
	tempCRN = max(dCRNNoTeach.items(), key=operator.itemgetter(1))[0]
	print(tempCRN)  #"max" CRN value
	tempTA = max(dNoTeach)

	#########################################################################################
	####     FIND NEXT TA TO TEACH BASED OFF AVAILABILITY 
	#########################################################################################
	print("\n\nShow available TA's for section and section number.")
	for x in sqlList:
		if x[1] == tempCRN:  #go through sqlList and look at the CRN's.  If they match continue with if statement.
			#print(x[0])  #DEBUG - show me the TA's who can't teach it.
			ditch = TAs.index(x[0])  #try to remove the TA's who can't teach and leave only those who can.
			TAs.pop(ditch)
	print(TAs)	#List of TA's who can teach this section.
	print(tempCRN)  #reminder of section.
	
	print("Max function:")
	print(max(dNoTeach))
	#Need to get biggest TA from TAs
	#print("TESTING ")
	#print("dNoTeach")
	#print(dNoTeach)
	#print("TAs")
	#print(TAs)
	#print("tempDict")
	# This creates a temp. Dictionary which contains all of the available TA's and how busy they are to teach.
	tempDict = {k: dNoTeach.get(k, 0) for k in TAs}
	#print(tempDict)
	#print("max value")
	#	print(max(tempDict.iterkeys(),key=(lambda key: tempDict[key])))
	tempTA = max(tempDict, key=tempDict.get)
	#print(tempTA)
	#print("DONE TESTING")	
	
	
	#update SQL database with who is teaching that section and add one to how many TA is teaching.
	c.execute("UPDATE F14 SET SetTA = ? WHERE CRN = ?", (tempTA, tempCRN))
	c.execute("SELECT nTeaching FROM F14TA WHERE Name = ?", (tempTA,))
	nTeachings = c.fetchall()
	tempNTeaching = nTeachings[0][0]
	tempNTeaching += 1
	c.execute("UPDATE F14TA SET nTeaching =? WHERE Name = ?", (tempNTeaching, tempTA))
	c.execute("SELECT nTeaching FROM F14TA WHERE Name = ?", (tempTA,))
	worked = c.fetchall()
	print("Now Teaching (# of sections): %s" %worked[0][0])	
	conn.commit()
#	if tempNTeaching >=2:
#		nIndex = OrigTAs.index(tempTA)
		
		
		# NEED TO REMOVE TAs who teach more than 2 sections...
#		print(" TESTING TESTING TESTING TESTING *******************")
#		print(dNoTeach)
		#dNoTeach.pop(dNoTeach.index(tempTA))
#		print(nIndex)
#		print(TAs)
		#OrigTAs.pop(nIndex)
#		print(TAs)
#		print("TA removed from options - teaching 2 sections")
	#########################################################################################
	# print("\n\n REMOVE USED CRN FROM SQL LIST")
	for x in sqlList:
		for x in sqlList:
			if x[1] == tempCRN:  #go through sqlList and look at the CRN's.  If they match continue with if statement.
				#print(x[0], x[1])  #DEBUG - show me the TA's who can't teach it.
				nIndex = sqlList.index(x)  #try to remove the TA's who can't teach and leave only those who can.
				sqlList.pop(nIndex)
#	print("\n\nnew sqlList")
	
#	print("CRN & # of TA's who can't teach it (5 = no one can teach, 0 = everyone can teach it):")
	dCRNNoTeach = dict()
	for x in sqlList:
		key = x[1]
		if key in dCRNNoTeach:
			dCRNNoTeach[key] +=1
		else:
			dCRNNoTeach[key] = 1
#	for key, value in dCRNNoTeach.items():
#		print(key, value)
	#########################################################################################	

	print("**********************************")


c.close()
conn.close()
print("\nClosed database successfully")