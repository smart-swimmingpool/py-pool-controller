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
from datetime import timedelta
from time import gmtime


class NTPtime:
    NTP_DELTA = 3155673600 if gmtime(0)[0] == 2000 else 2208988800
    SYNC_INTERVAL = 5.0
    DEFAULT_HOST = "pool.ntp.org"  # The NTP host can be configured at runtime by doing: ntptime.host = 'myhost.org'

    # Constructor
    # hrs_offset: Local time offset in hrs relative to UTC
    def __init__(self, ntp_host=DEFAULT_HOST, hrs_offset=0):
        self.host = ntp_host
        self.threshold_time = 0.0
        self.time = timedelta()
        self.hrs_offset = hrs_offset
        self.sync_time()

    def sync_time(self) -> int: # Local time offset in hrs relative to UTC
        ntp_query = bytearray(48)
        ntp_query[0] = 0x1B
        try:
            addr = socket.getaddrinfo(self.host, 123)[0][-1]
        except OSError:
            return 0
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        poller = select.poll()
        poller.register(sock, select.POLLIN)
        try:
            sock.sendto(ntp_query, addr)
            if poller.poll(1000):  # time in milliseconds
                msg = sock.recv(48)
                val = struct.unpack("!I", msg[40:44])[0]  # Can return 0
                return int(max(val - self.NTP_DELTA + (self.hrs_offset * -1) * 3600, 0))
        except OSError:
            return 0
        finally:
            sock.close()
        return 0  # Timeout or LAN error occurred

    def tick(self):  # loop to sync time
        t = time.time()
        if self.threshold_time < t:
            print("Syncing time from server...")
            self.threshold_time = t + self.SYNC_INTERVAL
            self.time = timedelta(seconds=self.sync_time())
            print("New time: " + str(self.time))


ntptime = NTPtime("pool.ntp.org", -2)
while True:
    ntptime.tick()
