from machine import Pin
import time
import network

# Core controller class
class PoolControllerContext:

    # Constructor
    def __init__(self, ssid, wifi_password):
        print("Initializing PoolControllerContext...")
        self.__initialize_wifi(ssid, wifi_password)
        self.led = Pin(2, Pin.OUT)
        self.is_running = True

    # Start the dispatch loop
    def run(self):
        self.is_running = True
        while self.is_running:
            self.led.off()
            time.sleep(0.5)
            self.led.on()
            time.sleep(0.5)

    # Stop the dispatch loop
    def stop(self):
        self.is_running = False

    # Private method - initialize WI-FI
    def __initialize_wifi(self, ssid, wifi_password):
        self.wifi_module = network.WLAN(network.STA_IF)
        self.wifi_module.active(True)
        for connection in self.wifi_module.scan():
            print(f"Found available WI-FI connection: {connection}")
        self.wifi_module.connect(ssid, wifi_password)
        assert self.wifi_module.isconnected(), "Failed to connect to WI-FI"
        print(f"WI-FI connected: {self.wifi_module.ifconfig()}")

# Main function
def main():
    print("*-------------------------------*")
    print("* Pool Controller Py            *")
    print("*-------------------------------*")

    ssid = "Your SSID"
    wifi_password = "Your WiFi Password"
    controller = PoolControllerContext(ssid, wifi_password)
    controller.run()


if __name__ == "__main__":
    main()
