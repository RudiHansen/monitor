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


# **************************************** Formatting Functions ****************************************
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

def addEOL(inputList):
    outputList = []
    idxLine    = 0
    while(idxLine < len(inputList)):
        addLine         = inputList[idxLine]
        lastColumn      = len(addLine)-1
        columnString    = addLine[lastColumn]
        columnString   += "\n"
        addLine[lastColumn] = columnString
        outputList.append(addLine)
        idxLine += 1
        
    return outputList

def fixColumnLen(inputList,columnWidth,wordWrapColumn):
    outputList = []
    idxLine    = 0
    while(idxLine < len(inputList)):
        outputLine      = []
        columnFields    = []
        inputLine       = inputList[idxLine]
        idxColumn       = 0
        lineNum         = 1
        
        while(idxColumn < len(columnWidth)):
            columnField     = inputLine[idxColumn]
            thisColumnWidth = columnWidth[idxColumn]
            if(idxColumn == wordWrapColumn):
                outputLine.append(columnField)
            else:
                outputLine.append(columnField.ljust(thisColumnWidth)[:thisColumnWidth])
            
            idxColumn += 1
        idxLine += 1
        outputList.append(outputLine)
        
    return outputList

def wordWrapColumn(inputList,columnWidth, wordWrapColumn):
    outputList      = []
    thisColumnWidth = columnWidth[wordWrapColumn]
    idxLine         = 0
    while(idxLine < len(inputList)):
        inputLine       = inputList[idxLine]
        first           = True
        
        wordWrapField   = inputLine[wordWrapColumn]
        while(len(wordWrapField) > thisColumnWidth):
            inputLine[wordWrapColumn]   = wordWrapField.ljust(thisColumnWidth)[:thisColumnWidth]
            addLine                     = inputLine[::]
            if(not first):
                addLine = blankColumn(addLine,wordWrapColumn)
            outputList.append(addLine)
            wordWrapField               = wordWrapField[thisColumnWidth:]
            first                       = False

        inputLine[wordWrapColumn]   = wordWrapField.ljust(thisColumnWidth)[:thisColumnWidth]
        addLine                     = inputLine[::]
        if(not first):
            addLine = blankColumn(addLine,wordWrapColumn)
        outputList.append(addLine)
        idxLine += 1

    return outputList
    
def blankColumn(addLine,wordWrapColumn):
    colIdx = 0
    while(colIdx < len(addLine)):
        if(colIdx != wordWrapColumn):
            oldFieldLen     = len(addLine[colIdx])
            addLine[colIdx] = "".ljust(oldFieldLen)
        colIdx += 1
            
    return addLine

# **************************************** Screen Functions ****************************************
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


# **************************************** General Functions ****************************************
def pause():
    raw_input("Press Enter to continue...")

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
