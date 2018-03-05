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

def unhandled_input(key):
    if key == 'q':
        raise urwid.ExitMainLoop()

def refresh(_loop,_data):
    computer_list    = loadCompStatsFromCsv('compstats.csv')    
    outputList       = printCompStats(computer_list)

    txt.set_text(outputList)
    loop.set_alarm_in(5,refresh)
        
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
    red_bg = urwid.AttrSpec('default', 'dark red')
    green_bg = urwid.AttrSpec('default', 'dark green')
    yellow_bg = urwid.AttrSpec('black', 'yellow')
    
    colLen_ComputerName         = 15
    colLen_LastOnlineDateTime   = 20
    colLen_CPUUtilization       = 5
    colLen_DiskUtilization      = 5

    dateTimeNow = datetime.now()
    col1Str     = 'Computer name'.ljust(colLen_ComputerName)[:colLen_ComputerName]
    col2Str     = 'Last online'.ljust(colLen_LastOnlineDateTime)[:colLen_LastOnlineDateTime]
    col3Str     = 'CPU'.ljust(colLen_CPUUtilization)[:colLen_CPUUtilization]
    col4Str     = 'Disk'.ljust(colLen_DiskUtilization)[:colLen_DiskUtilization]
    outList     = [col1Str,col2Str,col3Str,col4Str+'\n']
    
	
    for computer in computer_list:
        lastOnlineDateTime     = computer.LastOnlineDateTime + timedelta(seconds=computer.UpdateIntervalSec)
        lastOnlineDateTimeLong = computer.LastOnlineDateTime + timedelta(seconds=computer.UpdateIntervalSec*2)
    
        col1Str     = computer.ComputerName.ljust(colLen_ComputerName)[:colLen_ComputerName]
        col2Str     = str(computer.LastOnlineDateTime).ljust(colLen_LastOnlineDateTime)[:colLen_LastOnlineDateTime]
        col3Str     = str(computer.CPUUtilization).ljust(colLen_CPUUtilization)[:colLen_CPUUtilization]
        col4Str     = str(computer.DiskUtilization).ljust(colLen_DiskUtilization)[:colLen_DiskUtilization] + '\n'

        # Set Colors on ComputerName && LastOnlineDateTime
        if(dateTimeNow > lastOnlineDateTimeLong):
            col1    = (red_bg, col1Str)
            col2    = (red_bg, col2Str)
        elif(dateTimeNow > lastOnlineDateTime):
            col1    = (yellow_bg, col1Str)
            col2    = (yellow_bg, col2Str)
        else:
            col1    = (green_bg, col1Str)
            col2    = (green_bg, col2Str)
        
        # Set Colors on CPUUtilization
        if(computer.CPUUtilization >= 90):
            col3    = (red_bg, col3Str)
        elif(computer.CPUUtilization >= 80):
            col3    = (yellow_bg, col3Str)
        else:
            col3    = (green_bg, col3Str)

        # Set Colors on DiskUtilization
        if(computer.DiskUtilization >= 90):
            col4    = (red_bg, col4Str)
        elif(computer.DiskUtilization >= 80):
            col4    = (yellow_bg, col4Str)
        else:
            col4    = (green_bg, col4Str)
        
        outList.append(col1)
        outList.append(col2)
        outList.append(col3)
        outList.append(col4)
        
    return outList;

computer_list   = loadCompStatsFromCsv('compstats.csv')    
outputList      = printCompStats(computer_list)
txt             = urwid.Text(outputList)
fill            = urwid.Filler(txt, 'top')
loop            = urwid.MainLoop(fill, unhandled_input=unhandled_input)
loop.set_alarm_in(5,refresh)
loop.run()
