#!/usr/bin/python
# coding=utf-8
import monitor_func
import csv
import collections
from datetime import datetime
from datetime import timedelta
from colorama import Fore, Back, Style
import os
import time
import urwid
import logging
import mysql.connector

#logging.basicConfig(filename='out_compstats.log',level=logging.DEBUG)
refreshTime = 10
CompStats = collections.namedtuple('CompStats', 'ComputerName ComputerDescription ComputerOS Location IPInternal IPExternal LastOnlineDateTime UpdateIntervalSec CPUUtilization DiskUtilization')

def unhandled_input(key):
    if key == 'q':
        raise urwid.ExitMainLoop()

def refresh(_loop,_data):
    computer_list    = loadCompStatsFromMysql()
    outputList       = printCompStats(computer_list)
    header_text      = makeHeaderTxt()

    bodytxt.set_text(outputList)
    loop.set_alarm_in(refreshTime,refresh)
        
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
                                     LastOnlineDateTime=datetime.strptime(row[0], '%d-%m-%Y %H:%M:%S'),
                                     UpdateIntervalSec=int(row[7]),
                                     CPUUtilization=int(row[8]),
                                     DiskUtilization=int(row[9]))
                computer_list.append(computer)
            rowcount+=1
    return computer_list

def loadCompStatsFromMysql():
    computer_list = []
    cnx = mysql.connector.connect(user='compstatus', database='computerStatus')
    cursor = cnx.cursor()

    query = ("SELECT B.* FROM(select ComputerName,max(LogDate) as LogDate from ComputerStatus group by ComputerName) A INNER JOIN ComputerStatus B USING (ComputerName,LogDate) ORDER BY LogDate")
    cursor.execute(query)

    for row in cursor:
        computer = CompStats(ComputerName=row[1],
                             ComputerDescription=row[2],
                             ComputerOS=row[3],
                             Location=row[4], 
                             IPInternal=row[5],
                             IPExternal=row[6],
                             LastOnlineDateTime=row[0],
                             UpdateIntervalSec=int(row[7]),
                             CPUUtilization=int(row[8]),
                             DiskUtilization=int(row[9]))
        computer_list.append(computer)
    return computer_list
    
def printCompStats( computer_list):
    red_bg      = urwid.AttrSpec('default', 'dark red')
    green_bg    = urwid.AttrSpec('default', 'dark green')
    yellow_bg   = urwid.AttrSpec('black', 'yellow')
    
    screen_cols                 = monitor_func.get_screen_cols()
    colLenFactor                = screen_cols/10
    colLen_ComputerName         = colLenFactor * 3  #15
    colLen_LastOnlineDateTime   = colLenFactor * 4  #20
    colLen_CPUUtilization       = colLenFactor * 1  #5
    colLen_DiskUtilization      = colLenFactor * 2  #5

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

def makeHeaderTxt():
    screen_cols = monitor_func.get_screen_cols()

    txtTitle    = "Computer Status"
    fillerLen   = screen_cols - len(txtTitle) - 10
    txtFiller   = " ".ljust(fillerLen)[:fillerLen]
    header_text = [
        ('title', txtTitle), txtFiller,
        ('key', "Q"), " exits",
        ]
        
    #logging.debug(header_text)
    return header_text

def makePalette():
    palette = [
        ('body','default','default', 'standout'),
        ('header','white','dark blue', 'bold'),
        ('key','white', 'dark blue', 'underline'),
        ('title', 'white', 'dark blue',),
        ]    
    return palette
    
    
#computer_list   = loadCompStatsFromCsv('compstats.csv')    
computer_list   = loadCompStatsFromMysql()
outputList      = printCompStats(computer_list)
header_text     = makeHeaderTxt()
palette         = makePalette()

header          = urwid.AttrMap(urwid.Text(header_text), 'header')
bodytxt         = urwid.Text(outputList)
view            = urwid.Frame(header=header,body=urwid.Filler(bodytxt, valign='top'),focus_part='header')
loop            = urwid.MainLoop(view, palette, unhandled_input=unhandled_input)
loop.set_alarm_in(refreshTime,refresh)
loop.run()
