#!/usr/bin/python
# coding=utf-8
import urllib
import string
import datetime
from random import randint
import time
import socket
import os

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def disk_free(path):
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    free = float(free / (1024 * 1024))
    total = float(total / (1024 * 1024))
    return 100 - int((free/total) * 100)

def cpu_utilization():
    CPU_Pct=float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline())
    return int(CPU_Pct*100)
    
def writeComputerStatusURL(computerName, computerDescription, computerOS, location, ipInternal, ipExternal, updateIntervalSec, cpuUtilization, diskUtilization):
    url     = "http://birkelan.no-ip.org/test/writecomputerstatus.php?computername=%s&computerdescription=%s&computeros=%s&location=%s&ipinternal=%s&ipexternal=%s&updateintervalsec=%s&cpuutilization=%s&diskutilization=%s" % (computerName, computerDescription, computerOS, location, ipInternal, ipExternal, updateIntervalSec, cpuUtilization, diskUtilization)
    url     = string.replace(url," ","%20")    
    response = urllib.urlopen(url)
    
hostname = socket.gethostname()
description = 'This computer'
osname = os.name
location = 'Skodsborg'
ipadress = get_ip_address()
CPU_Pct = cpu_utilization()
DISK_Pct = disk_free('/')

writeComputerStatusURL(hostname,description,osname,location,ipadress,'',60*5,CPU_Pct,DISK_Pct)
