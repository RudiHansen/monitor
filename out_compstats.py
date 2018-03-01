#!/usr/bin/python
# coding=utf-8
import csv
import collections
from datetime import datetime
from datetime import timedelta
from colorama import Fore, Back, Style
import os
import time
import urwid


CompStats = collections.namedtuple('CompStats', 'ComputerName ComputerDescription ComputerOS Location IPInternal IPExternal LastOnlineDateTime UpdateIntervalSec CPUUtilization DiskUtilization')

def loadCompStatsFromCsv( fileName ):
    with open(fileName, 'rb') as csvfile:
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
    return computer_list
    
def printCompStats( computer_list):
    outputTxt = '';
    
    dateTimeNow = datetime.now()
    outString = '{0:<15} {1:20} {2:5} {3:5}'.format('ComputerName','LastOnlineDateTime','CPU','Disk')
    outputTxt += outString + '\n'
    for computer in computer_list:
        lastOnlineDateTime     = computer.LastOnlineDateTime + timedelta(seconds=computer.UpdateIntervalSec)
        lastOnlineDateTimeLong = computer.LastOnlineDateTime + timedelta(seconds=computer.UpdateIntervalSec*2)
    
        # Set Colors on ComputerName && LastOnlineDateTime
        if(dateTimeNow > lastOnlineDateTimeLong):
            ComputerName        = Back.RED + '{0:<15}'.format(computer.ComputerName) + Back.RESET
            LastOnlineDateTime  = Back.RED + '{0:20}'.format(str(computer.LastOnlineDateTime)) + Back.RESET
        elif(dateTimeNow > lastOnlineDateTime):
            ComputerName        = Back.YELLOW + '{0:<15}'.format(computer.ComputerName) + Back.RESET
            LastOnlineDateTime  = Back.YELLOW + '{0:20}'.format(str(computer.LastOnlineDateTime)) + Back.RESET
        else:
            ComputerName        = Back.GREEN + '{0:<15}'.format(computer.ComputerName) + Back.RESET
            LastOnlineDateTime  = Back.GREEN + '{0:20}'.format(str(computer.LastOnlineDateTime)) + Back.RESET
        
        # Set Colors on CPUUtilization
        if(computer.CPUUtilization >= 90):
            CPUUtilization = Back.RED + '{0:5}'.format(str(computer.CPUUtilization)) + Back.RESET
        elif(computer.CPUUtilization >= 80):
            CPUUtilization = Back.YELLOW + '{0:5}'.format(str(computer.CPUUtilization)) + Back.RESET
        else:
            CPUUtilization = Back.GREEN + '{0:5}'.format(str(computer.CPUUtilization)) + Back.RESET

        # Set Colors on DiskUtilization
        if(computer.DiskUtilization >= 90):
            DiskUtilization = Back.RED + '{0:5}'.format(str(computer.DiskUtilization)) + Back.RESET
        elif(computer.DiskUtilization >= 80):
            DiskUtilization = Back.YELLOW + '{0:5}'.format(str(computer.DiskUtilization)) + Back.RESET
        else:
            DiskUtilization = Back.GREEN + '{0:5}'.format(str(computer.DiskUtilization)) + Back.RESET
        
        outString = '{0:<15} {1:20} {2:5} {3:5}'.format(ComputerName,LastOnlineDateTime,CPUUtilization,DiskUtilization)
        outputTxt += outString + '\n'
        
    return outputTxt;

#while (1):
os.system('cls' if os.name == 'nt' else 'clear')
computer_list   = loadCompStatsFromCsv('compstats.csv')    
outputTxt       = printCompStats(computer_list)
#outputTxt       = "Test"
txt             = urwid.Text(outputTxt)
fill            = urwid.Filler(txt, 'top')
loop            = urwid.MainLoop(fill)
loop.run()
time.sleep(5)
