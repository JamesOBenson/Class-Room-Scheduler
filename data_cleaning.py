import csv		# USED IN FINAL STEP
import sys		# USED TO GET USER INPUTS
import os		# USED TO DELETE TEMP FILES
import re		# REGEX TESTING - CONVERTING 12HR TIME TO 24HR TIME
import subprocess #Calls next python script.


# Run this file first, then MakeTAList.py
# This file requires you to download the ASAP file from UTSA.
# It will then remove classes that are no available to students ever (Cancelled classes)
# Append a header to the new temp file for debugging purposes
# Then from the command prompt, the courses you entered will be searched for and put into 
# another new temp file and unnecessary columns will be removed.
# The time slot column will then be split and put into 24hr scheme.
# Below is example command to run the file.
#
# python data_cleaning 1611 1631 1951 1971
#
# This file will automatically execute the next python script to create the databases automatically:
# MakeTAList.py

Classes = len(sys.argv)
#  REMOVE CANCELED CLASSES
with open("xwskschd.CSV") as f:		#SOURCE FILE
    with open("temp.CSV", "w") as f1:		#OUTPUT FILE
        for line in f:
            if "OPEN" in line:
                f1.write(line)
            elif "CLOSED" in line:
                f1.write(line)

#  APPEND HEADER TO FILE
searchquery = '"Status","Subject","Course",'		# LEGACY, helps in debug
with open('xwskschd.CSV') as f1:
    with open('temp2.CSV', 'w') as f2:
        lines = f1.readlines()
        for i, line in enumerate(lines):
            if line.startswith(searchquery):
                f2.write(line.replace(" ", ""))	   #REMOVE WHITESPACE SO IMPORTS INTO SQL NICELY

#  LOOK FOR ONLY SECTIONS WE WANT				
with open("temp.CSV") as f1:			#SOURCE FILE
    with open("temp2.CSV", "a") as f2:		#OUTPUT FILE
        for line in f1:
            if sys.argv == "":
                f2.write(line)
            else:
                for i in range(0,len(sys.argv)):
                    if sys.argv[i] in line:
                        f2.write(line)




# DELETE UNNECESSARY COLUMNS - ***DATA CLEANED***
with open("temp2.CSV") as source:
    rdr= csv.reader( source )	# Get rid of "" around values
    with open("temp3.csv","w") as result:
        wtr= csv.writer( result, lineterminator='\n')   #removed unwanted new lines from csv.writer  lineterminator='\n'
        for r in rdr:
            wtr.writerow( (r[4], r[1], r[2], r[3], r[5], r[7], r[8], r[10]) )  # rearrange columns for desired output

with open("temp3.CSV") as source:
	rdr= csv.reader( source )
	with open("result.csv","w") as results:
		next(rdr)
		p = re.compile('pm')
		results.write('CRN,Subject,Course,Section,Title,MeetingDays,StartTime, EndTime,Location\n')
		for r in rdr:
			startTime, endTime = r[6].split('-')
			#print(startTime)	#Test to verify column split into 2
			#print(endTime)		#Test to verify column split into 2
			wtr= csv.writer( results, lineterminator='\n')
			#CONVERT ENDTIME TO 24HR SYSTEM
			if(endTime[-2:] == "am"):
				endTime = endTime[:-2]
			else:
				endTime[:-2].split(':')
				if (int(endTime[:-5])<12):
					temp = int(endTime[:-5])+12
					endTime = str(temp)+endTime[-5:-2]
			if(endTime[:2] =="12"):
				endTime = endTime[:-2]

			#CONVERT START TIME TO 24HR SYSTEM
			if((int(endTime[:2]) -int(startTime[:-3])) >=4):
				startTime.split(':')
				temp = int(startTime[0])+12
				startTime = str(temp)+startTime[-3:]
			wtr.writerow( (r[0], r[1], r[2], r[3], r[4], r[5], startTime+":00", endTime+":00",r[7]) )
			
			


########### REMOVED SINCE WE ARE USING SQL NOW.  THIS WILL CREATE AN EXTRA ROW IN THE SQL DB.#############
# MUST ADD LAST BECAUSE NO COLUMNS, THIS WILL INTERFERE WITH COLUMN REARRANGING AND CAUSE IT TO FAIL.
#  APPEND SEMESTER TO END OF FILE
#searchquery = '"Term: '
#with open('xwskschd.CSV') as f1:
#    with open('result.csv', 'a') as f2:
#        lines = f1.readlines()
#        for i, line in enumerate(lines):
#            if line.startswith(searchquery):
#                f2.write(line)		
###########################################################################################################


# DELETE TEMP FILES
os.remove("temp.CSV")
os.remove("temp2.CSV")
os.remove("temp3.CSV")

print("data cleaning is complete")

subprocess.call("python MakeTAList.py", shell = True)