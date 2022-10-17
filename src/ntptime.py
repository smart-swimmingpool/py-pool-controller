# Adapted from official ntptime by Peter Hinch July 2022
# The main aim is portability:
# Detects host device's epoch and returns time relative to that.
# Basic approach to local time: add offset in hours relative to UTC.
# Timeouts return a time of 0. These happen: caller should check for this.
# Replace socket timeout with select.poll as per docs:
# http://docs.micropython.org/en/latest/library/socket.html#socket.socket.settimeout
#
# Source: https://github.com/peterhinch/micropython-samples/blob/master/ntptime/ntptime.py

import socket
import struct
import select
import time
from time import gmtime


class NTPtime:
    # (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
    # (date(1970, 1, 1) - date(1900, 1, 1)).days * 24*60*60
    NTP_DELTA = 3155673600 if gmtime(0)[0] == 2000 else 2208988800
    SYNC_INTERVAL = 5.0

    host = "pool.ntp.org"  # The NTP host can be configured at runtime by doing: ntptime.host = 'myhost.org'
    hrs_offset = 0  # Local time offset in hrs relative to UTC

    last_timestamp = 0.0

    # Constructor
    # hrs_offset: Local time offset in hrs relative to UTC
    def __init__(self, ntp_host="pool.ntp.org", hrs_offset=0):
        self.host = ntp_host
        self.threshold_time = 0.0
        self.time()

    def time(self):  # Local time offset in hrs relative to UTC
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1B
        try:
            addr = socket.getaddrinfo(self.host, 123)[0][-1]
        except OSError:
            return 0
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        poller = select.poll()
        poller.register(s, select.POLLIN)
        try:
            s.sendto(NTP_QUERY, addr)
            if poller.poll(1000):  # time in milliseconds
                msg = s.recv(48)
                val = struct.unpack("!I", msg[40:44])[0]  # Can return 0
                x = max(val - self.NTP_DELTA + self.hrs_offset * 3600, 0)
                self.last_timestamp = time.time()
                return self.last_timestamp
        except OSError:
            pass  # LAN error
        finally:
            s.close()
        return 0  # Timeout or LAN error occurred

    def loop(self):  # loop to sync time
        t = time.time()
        if self.threshold_time < t:
            print("Syncing time from server...")
            self.threshold_time = t + self.SYNC_INTERVAL
            self.time()


ntptime = NTPtime("pool.ntp.org", -2)
while True:
    ntptime.loop()
