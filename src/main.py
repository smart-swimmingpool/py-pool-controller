import machine
import time
import network
import json
import utils
from ntptime import NTPtime

# Core controller class
class PoolControllerContext:
    TIMEZONE_OFFSET = -2 # Offset of timezone to UTC

    # Constructor
    def __init__(self, ssid: str, wifi_password: str):
        print("Initializing PoolControllerContext...")
        self.__initialize_wifi(ssid, wifi_password)
        self.led = machine.Pin(2, machine.Pin.OUT)
        self.is_running = True
        
        # Update Time via NTP Timzone UTC -2
        self.ntptime = NTPtime("pool.ntp.org", self.TIMEZONE_OFFSET)

    # Start the dispatch loop
    def run(self):
        print("Running dispatch loop...")
        self.is_running = True
        while self.is_running:
            self.led.off()
            time.sleep(0.5)
            self.led.on()
            time.sleep(0.5)
            print("current time: " + str(time.localtime()))
            self.ntptime.tick()

    # Stop the dispatch loop
    def stop(self):
        self.is_running = False

    # Private method - initialize WI-FI
    def __initialize_wifi(self, ssid: str, wifi_password: str):
        assert ssid is not None and ssid != ""
        assert wifi_password is not None and wifi_password != ""
        self.wifi_module = network.WLAN(network.STA_IF)
        self.wifi_module.active(True)
        for connection in self.wifi_module.scan():
            print("Found available WI-FI connection: " + str(connection))
            if connection[0] == ssid:
                print("Connecting to specified WI-FI connection with SSID " + ssid)
                self.wifi_module.connect(ssid, wifi_password)
                while not self.wifi_module.isconnected():
                    machine.idle()
                print("Connection established")
                break

        assert self.wifi_module.isconnected(), "Failed to connect to WI-FI"
        print("WI-FI connected: " + str(self.wifi_module.ifconfig()))


# Main function
def main():
    print("*-------------------------------*")
    print("* Pool Controller Py            *")
    print("*-------------------------------*")

    # Load WI-FI configuration

    ssid: str = ""
    wifi_password: str = ""
    config_file: str = "wifi_config.json"

    if not utils.does_file_exists(config_file):
        with open(config_file, "w") as f:
            content = '{"ssid": "Your SSID", "password": "Your WiFi Password"}'
            json.dump(content, f)

    with open(config_file, "r") as f:
        data = json.load(f)
        ssid = data["ssid"]
        wifi_password = data["password"]

    # Create controller context
    controller = PoolControllerContext(ssid, wifi_password)
    controller.run()


if __name__ == "__main__":
    main()
