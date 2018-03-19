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

logging.basicConfig(filename='out_chatlines.log',level=logging.DEBUG)
refreshTime = 10
logFileName = "/home/rsh/.weechat/logs/irc.labitat.#labitat.weechatlog"

ChatLines   = collections.namedtuple('ChatLines', 'DateTime UserName ChatText')

def pause():
    raw_input("Press Enter to continue...")

def unhandled_input(key):
    if key == 'q':
        raise urwid.ExitMainLoop()

def refresh(_loop,_data):
    computer_list    = loadChatLinesFromFile(logFileName)    
    outputList       = printCompStats(computer_list)
    header_text      = makeHeaderTxt()

    bodytxt.set_text(outputList)
    loop.set_alarm_in(refreshTime,refresh)
        
def loadChatLinesFromFile( fileName ):
    chatLines_list = []
    with open(fileName, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        chatLines_list = []
        for row in spamreader:
            if(row[1] != '-->' and row[1] != '<--'):
                computer = ChatLines(DateTime=row[0],
                                     UserName=row[1],
                                     ChatText=row[2])
                chatLines_list.append(computer)
    return chatLines_list

def formatListToOutput(inputList,columnHeaders,columnWidth):
    outputList = []
    
    columnWidth     = calculateColumnWidth(columnWidth)
    outputLineNums  = calculateOutputLines()
    outputList      = setHeader(columnWidth,['DateTime','User name','Text'])
    inputList       = getLastLines(inputList,outputLineNums)
    inputList       = fixColumnLen(inputList,columnWidth,3)
    outputList      = getLastLines(inputList,outputLineNums,True)
	
    return outputList
    
def printList(inputList):
    print "List length = ",len(inputList)
    idx = 0
    while(idx < len(inputList)-1):
        print inputList[idx]
        idx += 1
    print "----------------------------------------"
    
def printListDebug(inputList):
    logging.debug("List length = ",len(inputList))
    idx = 0
    while(idx < len(inputList)-1):
        logging.debug(inputList[idx])
        idx += 1
    logging.debug("----------------------------------------")

def calculateColumnWidth(columnWidth):
    screen_cols     = monitor_func.get_screen_cols()
    sumColumnWidth  = sum(columnWidth)
    listOf0         = [s for s in columnWidth if s==0]
    columns2Calc    = len(listOf0)

    if(columns2Calc):
        remainColumnWidth   = (screen_cols - sumColumnWidth) / columns2Calc
        idx = 0
        while idx < len(columnWidth):
            if(columnWidth[idx] == 0):
                columnWidth[idx] = remainColumnWidth
            idx += 1
    
    return columnWidth
    
def calculateOutputLines():
    return monitor_func.get_screen_rows() - 3

def setHeader(columnWidth,headerText):
    idx = 0
    while idx < len(columnWidth):
        headerText[idx] = headerText[idx].ljust(columnWidth[idx])[:columnWidth[idx]]
        idx += 1
        
    headerText[idx-1] = headerText[idx-1] + '\n'
    
    return headerText
    
def getLastLines(inputList,getNumLines,removeFirstBlank = False):
    numLines    = len(inputList)
    fromLine    = numLines - getNumLines
    outputList  = inputList[fromLine:numLines]
    
    if(removeFirstBlank):
        idx = 0
        first = True
        while(idx <= len(outputList)-1):
            line  = outputList[idx]
            if(first and line[0] == ""):
                outputList.remove(line)
            else:
                first = False
            idx += 1
        
    return outputList

def fixColumnLen(inputList,columnWidth,wrapColNr=0):
    outputList = []
    idxLine    = 0
    while(idxLine < len(inputList)):
        outputLine = []
        inputLine = inputList[idxLine]
        idxColumn = 0
        lineNum   = 1
        while(idxColumn < len(columnWidth)):
            columnTxt = inputLine[idxColumn]
            if(idxColumn == wrapColNr-1):
                while(columnTxt):
                    thisColumnWidth = columnWidth[idxColumn]
                    if(len(columnTxt) > thisColumnWidth):
                        if(lineNum == 1):
                            outputLine.append(columnTxt.ljust(thisColumnWidth)[:thisColumnWidth])
                            outputList.append(outputLine)
                        else:
                            extraLine       = ['','',columnTxt.ljust(thisColumnWidth)[:thisColumnWidth]]
                            outputList.append(extraLine)
                        columnTxt       = columnTxt[thisColumnWidth:]
                        lineNum += 1
                    else:
                        if(lineNum == 1):
                            outputLine.append(columnTxt.ljust(thisColumnWidth)[:thisColumnWidth])
                            outputList.append(outputLine)
                        else:
                            extraLine       = ['','',columnTxt.ljust(thisColumnWidth)[:thisColumnWidth]]
                            outputList.append(extraLine)
                        columnTxt       = columnTxt[thisColumnWidth:]
            else:
                outputLine.append(columnTxt.ljust(columnWidth[idxColumn])[:columnWidth[idxColumn]])
                if(idxColumn+1 == len(columnWidth) and lineNum == 1):
                    outputList.append(outputLine)
            idxColumn += 1
                
        idxLine += 1
        
    return outputList
    
def printCompStats( chatLines_list):
    red_bg      = urwid.AttrSpec('default', 'dark red')
    green_bg    = urwid.AttrSpec('default', 'dark green')
    yellow_bg   = urwid.AttrSpec('black', 'yellow')
    
    screen_rows     = monitor_func.get_screen_rows() - 3
    screen_cols     = monitor_func.get_screen_cols()
    #colLenFactor    = screen_cols/10
    #colLen_DateTime = colLenFactor * 2
    #colLen_UserName = colLenFactor * 1
    #colLen_ChatText = colLenFactor * 4
    colLen_DateTime = 20
    colLen_UserName = 15
    colLen_ChatText = screen_cols - 35

    col1Str     = 'DateTime'.ljust(colLen_DateTime)[:colLen_DateTime]
    col2Str     = 'User name'.ljust(colLen_UserName)[:colLen_UserName]
    col3Str     = 'Text'.ljust(colLen_ChatText)[:colLen_ChatText]
    outList     = [col1Str,col2Str,col3Str+'\n']
    
    numLines = len(chatLines_list)
    idx      = numLines - screen_rows
    chatLines_list = chatLines_list[idx:numLines]

    idx             = len(chatLines_list)-1
    idxTmpOutLine   = 1
    outPutLine      = 1
    tmpOutList      = []
    while(outPutLine < screen_rows):
        chatLine    = chatLines_list[idx]
        dateTimeStr = str(chatLine.DateTime)
        userNameStr = chatLine.UserName
        chatTextStr = chatLine.ChatText

        while(chatTextStr != ''):
            if(len(chatTextStr) > colLen_ChatText):
                col1Str = dateTimeStr.ljust(colLen_DateTime)[:colLen_DateTime]
                col2Str = userNameStr.ljust(colLen_UserName)[:colLen_UserName]
                col3Str = chatTextStr.ljust(colLen_ChatText)[:colLen_ChatText] + '\n'
                dateTimeStr = ''
                userNameStr = ''
                chatTextStr = chatTextStr[colLen_ChatText:]
            else:
                col1Str = dateTimeStr.ljust(colLen_DateTime)[:colLen_DateTime]
                col2Str = userNameStr.ljust(colLen_UserName)[:colLen_UserName]
                col3Str = chatTextStr.ljust(colLen_ChatText)[:colLen_ChatText] + '\n'
                chatTextStr = ''
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

    txtTitle    = "Chat lines"
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
    
    
chatLines_list  = loadChatLinesFromFile(logFileName)    
outputList      = printCompStats(chatLines_list)

columnHeaders   = ['DateTime','User name','Text']
columnWidth     = [20,15,0]
outputList2     = formatListToOutput(chatLines_list,columnHeaders,columnWidth)

header_text     = makeHeaderTxt()
palette         = makePalette()

header          = urwid.AttrMap(urwid.Text(header_text), 'header')
bodytxt         = urwid.Text(outputList)
view            = urwid.Frame(header=header,body=urwid.Filler(bodytxt, valign='top'),focus_part='header')
loop            = urwid.MainLoop(view, palette, unhandled_input=unhandled_input)
loop.set_alarm_in(refreshTime,refresh)
loop.run()
