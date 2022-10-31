import machine
import network
import json
import utils

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

    initialize_wifi(ssid, wifi_password)
    install_dependencies()
    
    # Create controller context
    from PoolController import PoolControllerContext
    controller = PoolControllerContext(ssid, wifi_password)
    controller.run()


# Private method - initialize WI-FI
def initialize_wifi(ssid: str, wifi_password: str):
    assert ssid is not None and ssid != ""
    assert wifi_password is not None and wifi_password != ""
    wifi_module = network.WLAN(network.STA_IF)
    wifi_module.active(True)
    print("Connecting to specified WI-FI connection with SSID " + ssid)
    wifi_module.connect(ssid, wifi_password)
    while not wifi_module.isconnected():
        machine.idle()
    print("Connection established")

    assert wifi_module.isconnected(), "Failed to connect to WI-FI"
    print("WI-FI connected: " + str(wifi_module.ifconfig()))

# Private method - install required dependencies
def install_dependencies():
    from setup.installer import Installer
    installer = Installer()
    installer.install_deps()
    
if __name__ == "__main__":
    main()
