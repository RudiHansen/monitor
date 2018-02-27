#!/usr/bin/python
import csv
import collections
from datetime import datetime
from datetime import timedelta
from colorama import Fore, Back, Style

CompStats = collections.namedtuple('CompStats', 'ComputerName ComputerDescription ComputerOS Location IPInternal IPExternal LastOnlineDateTime UpdateIntervalSec CPUUtilization DiskUtilization')

#print 'Type of CompStats', type(CompStats)

#datetime_object  = datetime.strptime('2015-08-15 20:40:00', '%Y-%m-%d %H:%M:%S')

#comp1 = CompStats(ComputerName='Test1',ComputerDescription='',ComputerOS='',Location='', IPInternal='',IPExternal='',LastOnlineDateTime=datetime_object,UpdateIntervalSec=0,CPUUtilization=0,DiskUtilization=0)
#comp2 = CompStats(ComputerName='Test2',ComputerDescription='',ComputerOS='',Location='', IPInternal='',IPExternal='',LastOnlineDateTime='',UpdateIntervalSec=0,CPUUtilization=0,DiskUtilization=0)

#print 'Comp1 = ', comp1.ComputerName
#print 'Comp1 = ', comp1.LastOnlineDateTime
#print 'Type',type(comp1.LastOnlineDateTime)
#print 'Comp2 = ', comp2.ComputerName
#print 'Comp2 = ', comp2.LastOnlineDateTime

with open('compstats.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
    rowcount = 1
    computer_list = []
    for row in spamreader:
        if(rowcount <> 1):
            computer = CompStats(ComputerName=row[0],
                                 ComputerDescription=row[1],
                                 ComputerOS=row[2],
                                 Location=row[3], 
                                 IPInternal=row[4],
                                 IPExternal=row[5],
                                 LastOnlineDateTime=datetime.strptime(row[6], '%d-%m-%Y %H:%M:%S'),
                                 UpdateIntervalSec=int(row[7]),
                                 CPUUtilization=int(row[8]),
                                 DiskUtilization=int(row[9]))
            computer_list.append(computer)
        rowcount+=1
        

dateTimeNow = datetime.now()
outString = '{0:<15} {1:20} {2:5} {3:5}'.format('ComputerName','LastOnlineDateTime','CPU','Disk')
print outString
for computer in computer_list:
    lastOnlineDataTime     = computer.LastOnlineDateTime + timedelta(seconds=computer.UpdateIntervalSec)
    lastOnlineDataTimeLong = computer.LastOnlineDateTime + timedelta(seconds=computer.UpdateIntervalSec*5)
    
    if(dateTimeNow > lastOnlineDataTimeLong):
	outString = Back.RED + '{0:<15}'.format(computer.ComputerName) + Back.RESET
    elif(dateTimeNow > lastOnlineDataTime):
	outString = Back.YELLOW + '{0:<15}'.format(computer.ComputerName) + Back.RESET
    else:
	outString = Back.GREEN + '{0:<15}'.format(computer.ComputerName) + Back.RESET
        
    outString += ' {0:20} {1:5} {2:5}'.format(str(computer.LastOnlineDateTime),str(computer.CPUUtilization),str(computer.DiskUtilization))
    print outString
