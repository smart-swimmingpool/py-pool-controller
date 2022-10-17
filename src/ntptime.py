# Adapted from official ntptime by Peter Hinch July 2022
# The main aim is portability:
# Detects host device's epoch and returns time relative to that.
# Basic approach to local time: add offset in hours relative to UTC.
# Timeouts return a time of 0. These happen: caller should check for this.
# Replace socket timeout with select.poll as per docs:
# http://docs.micropython.org/en/latest/library/socket.html#socket.socket.settimeout
#
# Source: https://github.com/peterhinch/micropython-samples/blob/master/ntptime/ntptime.py

import time
import utime    # lib to convert unixtime in array wiht hour, min, sec,day,month,year
import ntptime  # NTP Support
from time import gmtime
from machine import RTC # Realtime Clock


class NTPtime:
    last_request_timestamp = 0
    SYNC_INTERVAL = 3600.0
    rtc = RTC()
    
    # Constructor
    # ntp_host: host can be configured at runtime by doing: ntptime.host = 'myhost.org'
    # hrs_offset: local time offset in hrs relative to UTC
    def __init__(self, ntp_host="pool.ntp.org", hrs_offset=0):
        ntptime.host = ntp_host
        self.threshold_time = 0.0
        self.hrs_offset = hrs_offset
        self.sync_time()

    def sync_time(self): # Local time offset in hrs relative to UTC
        print("sync time ...")
        try: 
            ntptime.settime(self.hrs_offset)
            self.last_request_timestamp = time.time()
            self.rtc.datetime(time.gmtime(self.last_request_timestamp)) # set a specific date and time
        except:
            print("Connecting NTP-Server failed")
            self.last_request_timestamp = time.time()
        return time.time()

    def tick(self):  # loop to sync time
        t = time.time()
        if self.threshold_time < t:
            print('Update time via NTP from host:', ntptime.host)
            self.threshold_time = t + self.SYNC_INTERVAL
            self.time = self.sync_time()
            print("New time: " + str(time.time()))

    def tzoffset(now):
        # Auszüge von https://community.hiveeyes.org/t/berechnung-von-sommerzeit-winterzeit-in-micropython/3183
        year = now[0]       #get current year
        HHMarch   = time.mktime((year,3 ,(31-(int(5*year/4+4))%7),1,0,0,0,0,0)) #Time of March change to CEST
        HHOctober = time.mktime((year,10,(31-(int(5*year/4+1))%7),1,0,0,0,0,0)) #Time of October change to CET
        now=time.time()
        if now < HHMarch :               # we are before last sunday of march
            tzoffset=1                   # CET:  UTC+1H
        elif now < HHOctober :           # we are before last sunday of october
            tzoffset=2                   # CEST: UTC+2H
        else:                            # we are after last sunday of october
            tzoffset=1                   # CET:  UTC+1H
        return(tzoffset)