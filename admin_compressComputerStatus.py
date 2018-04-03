#!/usr/bin/python
# coding=utf-8
import collections
import mysql.connector
import datetime

ComputerStatus = collections.namedtuple('ComputerStatus', 'Id LogDate ComputerName Location IPInternal IPExternal CPUUtilization DiskUtilization')

def pause():
    raw_input("Press Enter to continue...")
    
def loadComputerNamesFromMysql():
    output_list = []
    cnx = mysql.connector.connect(user='compstatus', database='computerStatus')
    cursor = cnx.cursor()

    query = ("SELECT DISTINCT ComputerName FROM ComputerStatus ORDER BY ComputerName;")
    cursor.execute(query)

    for row in cursor:
        output_list.append(row[0])

    return output_list

def loadComputerStatusFromMysql(ComputerName):
    output_list = []
    cnx = mysql.connector.connect(user='compstatus', database='computerStatus')
    cursor = cnx.cursor()

    query = "SELECT Id, LogDate, ComputerName, Location, IPInternal,IPExternal, CPUUtilization, DiskUtilization FROM ComputerStatus WHERE ComputerName='" + ComputerName + "' ORDER BY Id;"
    
    cursor.execute(query)

    for row in cursor:
        line = ComputerStatus(Id=row[0],
                              LogDate=row[1] ,
                              ComputerName=row[2],
                              Location=row[3], 
                              IPInternal=row[4],
                              IPExternal=row[5],
                              CPUUtilization=row[6],
                              DiskUtilization=row[7])
        output_list.append(line)

    return output_list

def deleteComputerStatusFromMysql(IdRemoveList):
    output_list     = []
    IdRemoveListStr = ""

    if(len(IdRemoveList) == 0):
        return
    
    for Id in IdRemoveList:
        IdRemoveListStr += str(Id)
        IdRemoveListStr += ","
        
    IdRemoveListStr = IdRemoveListStr[:len(IdRemoveListStr)-1]
        
    cnx = mysql.connector.connect(user='compstatus', database='computerStatus')
    cursor = cnx.cursor()

    query = "DELETE FROM ComputerStatus WHERE Id in (" + IdRemoveListStr +");"
    cursor.execute(query)
    cnx.commit()
    
def findIdToRemove(inputList):
    outputList = []
    lastDate = datetime.date(1970,1,1)
    lastLocation = ""
    lastIPInternal = ""
    lastIPExternal = ""
    lastCPUUtilization = 0
    lastDiskUtilization = 0

    for item in inputList:
        if(item.LogDate.date()    == lastDate
        and item.Location         == lastLocation
        and item.IPInternal       == lastIPInternal
        and item.IPExternal       == lastIPExternal
        and item.CPUUtilization   == lastCPUUtilization
        and item.DiskUtilization  == lastDiskUtilization):
            outputList.append(item.Id)
            
        lastDate            = item.LogDate.date()
        lastLocation        = item.Location
        lastIPInternal      = item.IPInternal
        lastIPExternal      = item.IPExternal
        lastCPUUtilization  = item.CPUUtilization
        lastDiskUtilization = item.DiskUtilization

        if(len(outputList) > 30):
            deleteComputerStatusFromMysql(outputList)
            outputList = []

    deleteComputerStatusFromMysql(outputList)
    return outputList

def countComputerStatusFromMysql(PrintStr):
    cnx = mysql.connector.connect(user='compstatus', database='computerStatus')
    cursor = cnx.cursor()

    query = "SELECT Count(Id) FROM ComputerStatus;"
    
    cursor.execute(query)

    for row in cursor:
        print PrintStr,row[0]
   
    
ComputerNames = []
IdRemoveList  = []
ComputerNames = loadComputerNamesFromMysql()    

countComputerStatusFromMysql("Records before compression: ")
for ComputerName in ComputerNames:
    print "Checking list for: ",ComputerName
    ComputerStatusList = loadComputerStatusFromMysql(ComputerName)
    IdRemoveList       = findIdToRemove(ComputerStatusList)

countComputerStatusFromMysql("Records after compression: ")