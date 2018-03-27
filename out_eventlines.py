#!/usr/bin/python
# coding=utf-8
import monitor_func
import out_functions
import csv
import collections
import datetime as dt
from datetime import datetime
from datetime import timedelta
from colorama import Fore, Back, Style
import os
import time
import urwid
import logging
import mysql.connector

#logging.basicConfig(filename='out_chatlines.log',level=logging.DEBUG)
refreshTime = 10
eventFileName = "eventlines.csv"

EventLines   = collections.namedtuple('EventLines', 'DateTime SenderName EventText')

def unhandled_input(key):
    if key == 'q':
        raise urwid.ExitMainLoop()

def refresh(_loop,_data):
    #eventLines_list  = loadEventLinesFromFile(eventFileName)    
    eventLines_list  = loadEventLinesFromMysql()
    columnHeaders   = ['DateTime','User name','Text']
    columnWidth     = [20,15,0]
    outputList      = formatListToOutput(eventLines_list,columnHeaders,columnWidth)
    header_text      = makeHeaderTxt()

    bodytxt.set_text(outputList)
    loop.set_alarm_in(refreshTime,refresh)
        
def loadEventLinesFromFile( fileName ):
    eventLines_list = []
    with open(fileName, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        eventLines_list = []
        for row in spamreader:
            computer = EventLines(DateTime=row[0],
                                  SenderName=row[1],
                                  EventText=row[2])
            eventLines_list.append(computer)
    return eventLines_list

def loadEventLinesFromMysql():
    eventLines_list = []
    cnx = mysql.connector.connect(user='webLog', database='webLogSql')
    cursor = cnx.cursor()

    query = ("SELECT LogDate,LogType,LogText FROM WebLogTable")
    cursor.execute(query)

    for row in cursor:
        line = EventLines(DateTime=row[0].strftime('%d-%m-%Y %H:%M:%S'),
                          SenderName=row[1],
                          EventText=row[2])
        eventLines_list.append(line)
    return eventLines_list

def formatListToOutput(inputList,columnHeaders,columnWidth):
    outputList = []
    
    columnWidth     = out_functions.calculateColumnWidth(columnWidth)
    outputLineNums  = out_functions.calculateOutputLines()
    outputList      = out_functions.setHeader(columnWidth,['DateTime','Sender name','Text'])
    inputList       = out_functions.getLastLines(inputList,outputLineNums)
    inputList       = out_functions.fixColumnLen(inputList,columnWidth, 2)
    inputList       = out_functions.wordWrapColumn(inputList,columnWidth,2)
    outputList      = out_functions.getLastLines(inputList,outputLineNums,True)
    outputList      = out_functions.addEOL(outputList)
    outputList      = setColorsOnLines(outputList)
    
    return outputList

def setColorsOnLines(inputList):
    red_bg       = urwid.AttrSpec('default', 'dark red')
    green_bg     = urwid.AttrSpec('default', 'dark green')
    yellow_bg    = urwid.AttrSpec('black', 'yellow')
    outputList   = []
    lineDateTime = dt.datetime(2000, 1, 1, 12, 00, 00)
    for line in inputList:
        if(line[0].strip() != ""):
            lineDateTime    = datetime.strptime(line[0],'%d-%m-%Y %H:%M:%S ')
        today           = dt.date.today()
        thisWeek        = dt.date.today()-dt.timedelta(days=7)
        
        if(lineDateTime.date() == today):
            newLine = (green_bg,line)
        elif(lineDateTime.date() > thisWeek):
            newLine = (yellow_bg,line)
        else:
            newLine = line[::]

        outputList.append(newLine)
        
    return outputList
    
def makeHeaderTxt():
    screen_cols = monitor_func.get_screen_cols()

    txtTitle    = "Event lines"
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
    
#eventLines_list  = loadEventLinesFromFile(eventFileName)    
eventLines_list  = loadEventLinesFromMysql()

columnHeaders   = ['DateTime','Sender name','Text']
columnWidth     = [20,15,0]
outputList      = formatListToOutput(eventLines_list,columnHeaders,columnWidth)

header_text     = makeHeaderTxt()
palette         = makePalette()

header          = urwid.AttrMap(urwid.Text(header_text), 'header')
bodytxt         = urwid.Text(outputList)
view            = urwid.Frame(header=header,body=urwid.Filler(bodytxt, valign='top'),focus_part='header')
loop            = urwid.MainLoop(view, palette, unhandled_input=unhandled_input)
loop.set_alarm_in(refreshTime,refresh)
loop.run()
