import logging
import machine
import time
from timesync import TimeSync

# Core controller class
class PoolControllerContext:
    
    log = logging.getLogger(__name__)
    
    # Constructor
    def __init__(self, ssid: str, wifi_password: str):
        self.log.debug("Initializing PoolControllerContext...")
        self.led = machine.Pin(2, machine.Pin.OUT)
        
        logging.basicConfig(level=logging.INFO)
        logging.getLogger().addHandler(LogHandler())
    
        self.is_running = True
        self.time_sync = TimeSync("fritz.box")

    # Start the dispatch loop
    def run(self):
        self.log.info("Running dispatch loop...")
        self.is_running = True
        while self.is_running:
            self.led.off()
            time.sleep(0.5)
            self.led.on()
            time.sleep(0.5)
            self.time_sync.tick()
            machine.idle()

    # Stop the dispatch loop
    def stop(self):
        self.is_running = False


class LogHandler(logging.Handler):
    def emit(self, record):
        print("level=%(levelname)s \tname=%(name)s: %(message)s" % record.__dict__)