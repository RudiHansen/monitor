#!/usr/bin/python
# coding=utf-8
import csv
from datetime import datetime
from datetime import timedelta
from random import randint


with open('compstats.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)

    spamwriter.writerow(['ComputerName','ComputerDescription','ComputerOS','Location','IPInternal','IPExternal','LastOnlineDateTime','UpdateIntervalSec','CPUUtilization','DiskUtilization'])

    dateTimeNow = datetime.now()
    dateTimeNow -= timedelta(seconds=120)
    spamwriter.writerow(['RSH-PC','Rudi Home','Windown 10','Skodsborg','192.168.0.190','',dateTimeNow.strftime('%d-%m-%Y %H:%M:%S'),60,randint(1,100),randint(1,100)])

    dateTimeNow += timedelta(seconds=60)
    spamwriter.writerow(['RSH-ARB','Rudi Work','Windown 10','Skodsborg','192.168.0.191','',dateTimeNow.strftime('%d-%m-%Y %H:%M:%S'),60,randint(1,100),randint(1,100)])

    dateTimeNow += timedelta(seconds=60)
    spamwriter.writerow(['firemane4','Rudi Server','Ubuntu 16.04','Skodsborg','192.168.0.192','',dateTimeNow.strftime('%d-%m-%Y %H:%M:%S'),60,randint(1,100),randint(1,100)])

    dateTimeNow += timedelta(seconds=60)
    spamwriter.writerow(['OBT-AX50-02','AX2009 Server 02','Windows Server 2008R2','Køge','192.168.1.200','',dateTimeNow.strftime('%d-%m-%Y %H:%M:%S'),60,randint(1,100),randint(1,100)])

    dateTimeNow += timedelta(seconds=60)
    spamwriter.writerow(['OBT-AX60-01','AX2012 Server 01','Windows Server 2008R2','Køge','192.168.1.201','',dateTimeNow.strftime('%d-%m-%Y %H:%M:%S'),60,randint(1,100),randint(1,100)])
