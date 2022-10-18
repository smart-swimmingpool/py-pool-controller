import machine
import time
import network
import json
import utils
from timesync import TimeSync

# Core controller class
class PoolControllerContext:

    # Constructor
    def __init__(self, ssid: str, wifi_password: str):
        print("Initializing PoolControllerContext...")
        self.led = machine.Pin(2, machine.Pin.OUT)
        self.__initialize_wifi(ssid, wifi_password)
        self.is_running = True
        self.time_sync = TimeSync("pool.ntp.org")

    # Start the dispatch loop
    def run(self):
        print("Running dispatch loop...")
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

    # Private method - initialize WI-FI
    def __initialize_wifi(self, ssid: str, wifi_password: str):
        assert ssid is not None and ssid != ""
        assert wifi_password is not None and wifi_password != ""
        self.wifi_module = network.WLAN(network.STA_IF)
        self.wifi_module.active(True)
        print("Connecting to specified WI-FI connection with SSID " + ssid)
        self.wifi_module.connect(ssid, wifi_password)
        while not self.wifi_module.isconnected():
            machine.idle()
            print('.', end='')
        print("Connection established")

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
