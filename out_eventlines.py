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

#logging.basicConfig(filename='out_chatlines.log',level=logging.DEBUG)
refreshTime = 10
eventFileName = "eventlines.csv"

EventLines   = collections.namedtuple('EventLines', 'DateTime SenderName EventText')

def pause():
    raw_input("Press Enter to continue...")

def unhandled_input(key):
    if key == 'q':
        raise urwid.ExitMainLoop()

def refresh(_loop,_data):
    computer_list    = loadEventLinesFromFile(eventFileName)    
    outputList       = printCompStats(computer_list)
    header_text      = makeHeaderTxt()

    bodytxt.set_text(outputList)
    loop.set_alarm_in(refreshTime,refresh)
        
def loadEventLinesFromFile( fileName ):
    eventLines_list = []
    with open(fileName, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        eventLines_list = []
        for row in spamreader:
            computer = EventLines(DateTime=datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'),
                                 SenderName=row[1],
                                 EventText=row[2])
            eventLines_list.append(computer)
    return eventLines_list

def printCompStats(eventLines_list):
    red_bg      = urwid.AttrSpec('default', 'dark red')
    green_bg    = urwid.AttrSpec('default', 'dark green')
    yellow_bg   = urwid.AttrSpec('black', 'yellow')
    
    screen_rows     = monitor_func.get_screen_rows() - 3
    screen_cols     = monitor_func.get_screen_cols()
    #colLenFactor    = screen_cols/10
    #colLen_DateTime = colLenFactor * 2
    #colLen_UserName = colLenFactor * 1
    #colLen_ChatText = colLenFactor * 4
    colLen_DateTime     = 20
    colLen_SenderName   = 15
    colLen_EventText    = screen_cols - 35

    col1Str     = 'DateTime'.ljust(colLen_DateTime)[:colLen_DateTime]
    col2Str     = 'User name'.ljust(colLen_SenderName)[:colLen_SenderName]
    col3Str     = 'Text'.ljust(colLen_EventText)[:colLen_EventText]
    outList     = [col1Str,col2Str,col3Str+'\n']
	
    numLines = len(eventLines_list)
    idx      = numLines - screen_rows
    if(idx < 0):
        eventLines_list = eventLines_list[idx:numLines]

    idx             = len(eventLines_list)-1
    idxTmpOutLine   = 1
    outPutLine      = 1
    tmpOutList      = []
    while(outPutLine < screen_rows and idx > 0):
        eventLine   = eventLines_list[idx]
        dateTimeStr = str(eventLine.DateTime)
        senderNameStr = eventLine.SenderName
        eventTextStr = eventLine.EventText

        while(eventTextStr != ''):
            if(len(eventTextStr) > colLen_EventText):
                col1Str = dateTimeStr.ljust(colLen_DateTime)[:colLen_DateTime]
                col2Str = senderNameStr.ljust(colLen_SenderName)[:colLen_SenderName]
                col3Str = eventTextStr.ljust(colLen_EventText)[:colLen_EventText] + '\n'
                dateTimeStr = ''
                senderNameStr = ''
                eventTextStr = eventTextStr[colLen_EventText:]
            else:
                col1Str = dateTimeStr.ljust(colLen_DateTime)[:colLen_DateTime]
                col2Str = senderNameStr.ljust(colLen_SenderName)[:colLen_SenderName]
                col3Str = eventTextStr.ljust(colLen_EventText)[:colLen_EventText] + '\n'
                eventTextStr = ''
            outPutLine += 1
        
            tmpOutList.append([idxTmpOutLine,col1Str,col2Str,col3Str])
        idx           -= 1
        idxTmpOutLine += 1
    
    new_list    = []
    numRecords  = idxTmpOutLine-1
    tmpLen      = numRecords
    tmpIdx      = 1
    while(tmpIdx <= numRecords):
        part_list   = [x for x in tmpOutList if x[0] == tmpLen]

        for newLine in part_list:
            insertLine = [newLine[1],newLine[2],newLine[3]]
            new_list.append(insertLine)
        tmpIdx += 1
        tmpLen -= 1

    return new_list;

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
    
    
eventLines_list  = loadEventLinesFromFile(eventFileName)    
outputList      = printCompStats(eventLines_list)
header_text     = makeHeaderTxt()
palette         = makePalette()

header          = urwid.AttrMap(urwid.Text(header_text), 'header')
bodytxt         = urwid.Text(outputList)
view            = urwid.Frame(header=header,body=urwid.Filler(bodytxt, valign='top'),focus_part='header')
loop            = urwid.MainLoop(view, palette, unhandled_input=unhandled_input)
loop.set_alarm_in(refreshTime,refresh)
loop.run()
