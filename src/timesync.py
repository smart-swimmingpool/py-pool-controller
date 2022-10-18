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
import machine
import logging

class TimeSync:
    log = logging.getLogger(__name__)
    last_request_timestamp = 0
    SYNC_INTERVAL = 360.0
    rtc = machine.RTC()
    
    # Constructor
    # ntp_host: host can be configured at runtime by doing: ntptime.host = 'myhost.org'
    # hrs_offset: local time offset in hrs relative to UTC
    def __init__(self, ntp_host="pool.ntp.org"):
        ntptime.host = ntp_host
        self.threshold_time = 0.0
        self.sync_time()

    def sync_time(self): # Local time offset in hrs relative to UTC
        self.log.debug("sync time ...")
        try: 
            ntptime.settime()             
            self.last_request_timestamp = time.time()
        except Exception as e:
            self.log.error("Connecting NTP-Server failed")
            # printing stack trace
            import sys
            sys.print_exception(e)      
            self.last_request_timestamp = time.time()
        return time.time()

    def tick(self):  # loop to sync time
        t = time.time()
        if self.threshold_time < t:
            self.log.debug('Update time via NTP from host:', ntptime.host)
            self.threshold_time = t + self.SYNC_INTERVAL
            self.time = self.rtc.datetime()
            now = self.rtc.datetime()
            self.log.info("Datum/UTCTime/TZ: %s.%s.%s  %s:%s:%s TZ %s", now[2], now[1], now[0], now[4], now[5], now[6], self.tzoffset(now))

    def tzoffset(self, now):
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