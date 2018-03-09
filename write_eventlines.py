#!/usr/bin/python
# coding=utf-8
import csv
from datetime import datetime
from datetime import timedelta
from random import randint


with open('eventlines.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)

    spamwriter.writerow(['2017-09-01 08:00:36','','Obtain IP 188.182.160.189'])
    spamwriter.writerow(['2017-09-05 16:57:45','OBT-AX60-02','Start Incremental CIL compiling application'])
    spamwriter.writerow(['2017-09-05 16:58:21','OBT-AX60-02','Stop Incremental CIL compiling application'])
    spamwriter.writerow(['2017-10-02 15:25:08','OBT-AX60-02','Start Incremental CIL compiling application'])
    spamwriter.writerow(['2017-10-02 15:27:30','OBT-AX60-02','Start Incremental CIL compiling application'])
    spamwriter.writerow(['2017-10-02 15:27:45','OBT-AX60-02','Stop Incremental CIL compiling application'])
    spamwriter.writerow(['2017-10-03 10:11:58','OBT-AX60-02','Start Incremental CIL compiling application'])
    spamwriter.writerow(['2017-10-03 10:12:15','OBT-AX60-02','Stop Incremental CIL compiling application'])
    spamwriter.writerow(['2017-10-03 10:20:55','OBT-AX60-02','Start Incremental CIL compiling application'])
    spamwriter.writerow(['2017-10-03 10:21:04','OBT-AX60-02','Stop Incremental CIL compiling application'])
    spamwriter.writerow(['2017-10-03 10:32:09','OBT-AX60-02','Start Incremental CIL compiling application'])
    spamwriter.writerow(['2017-10-03 10:32:17','OBT-AX60-02','Stop Incremental CIL compiling application'])
    spamwriter.writerow(['2017-10-03 10:35:17','OBT-AX60-02','Start Incremental CIL compiling application'])
    spamwriter.writerow(['2017-10-03 10:35:25','OBT-AX60-02','Stop Incremental CIL compiling application'])
    spamwriter.writerow(['2017-11-14 10:55:13','OBT-AX60-02','Start Incremental CIL compiling application'])
    spamwriter.writerow(['2017-11-14 11:05:08','OBT-AX60-02','Start FULL CIL compiling application'])
    spamwriter.writerow(['2017-11-14 11:21:27','OBT-AX60-02','Start Incremental CIL compiling application'])
    spamwriter.writerow(['2017-11-14 11:22:09','OBT-AX60-02','Stop Incremental CIL compiling application'])
    spamwriter.writerow(['2017-11-30 13:01:03','OBT-AX60-02','\<Classes\\Application\\new clientKind WorkerThread sessionId 5'])
    spamwriter.writerow(['2017-11-30 13:01:05','OBT-AX60-02','\<Classes\\Application\\new clientKind WorkerThread sessionId 6'])

