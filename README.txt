**********************************************
This program is still in testing mode and may not work for all universities.
Currently this program is designed to work on UTSA's ASAP class room scheduler.
**********************************************
FILES NECESSARY TO DOWNLOAD:
To begin, download the schedule from ASAP (xwskschd) 

FILES TO MAKE:
You will need to create a TA schedule file as well (BusyTASchedule). 

EXECUTION:
Download all three py files, and you will first need to clean the data from ASAP.  The three files will run automatically so be sure they are all there.  This process will remove any class that isn't of interest.

data_cleaning.py:
Execute:  python data_cleaning 1611 1631 1951 1971
This will filter out the file finding only classes that are within these sections.

MakeTAList.py:
Execute:  python MakeTAList.py  (Complete prompts)
Then the file will create two SQL databases, one for the classes, one for the TA's.

3Possibilities.py
Execute:  python 3Possibilities.py F14
This file will preform greedy method to find a schedule for your TA's so that they all will teach.  This file is still being debugged to allow for multiple rooms without conflict along with a maximum of teaching.
