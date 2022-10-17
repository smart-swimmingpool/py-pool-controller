from wifi_setup.wifi_setup import WiFiSetup

from machine import Pin
import time

led = Pin(2, Pin.OUT)


def main():
    print("*-------------------------------*")
    print("* Pool Controller Py            *")
    print("*-------------------------------*")

    ws = WiFiSetup("pool-controller")
    sta = ws.connect_or_setup()
    del ws

    print("WiFi is setup")

    while True:
        led.off()
        time.sleep(0.5)
        led.on()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
