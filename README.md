# pyPool Controller (planned)

Python based implementation of [Pool Controller](https://github.com/smart-swimmingpool/pool-controller).

Porting the C-implementation based on ESP8266 on Micro-/Circuit-Python for Raspberry Pico (RP2040) and/or ESP32.

## Hacktoberfest

<img width="800" alt="Hacktoberfest 2022" src="https://user-images.githubusercontent.com/184547/191762878-c28f4e68-fd69-4306-9293-d7037b0c364a.png">


I am a beginner in programming with Python. But I have had enough of C! I want to learn Python on micro circuits (ESP32, Raspberry Pico RP2040) and port Pool Controller which is now working for years!
Who could help me to start an initial base for professional setup of the project?

Let us code a new cool version for next summer season!

How to contribute:

1) ⭐ the repository
2) Pick an existing issue or create a new one (new feature or bug fixing)
3) Fork the repository and start working on your branch
4) Create a Pull Request to the original repo and wait for a code review (expect <12h)
5) Have fun and learn new things

Happy coding 🚀

## Community

Join the community on [Discord](https://discord.gg/ywHCYKdamu)

## Development

### Installing MicroPython/CircuitPython

```commandline
> esptool --chip esp8266 --port COM12 erase_flash
> esptool --port COM12 --baud 460800 write_flash --flash_size=detect 0 .\adafruit-circuitpython-ai_thinker_esp_12k_nodemcu-de_DE-8.0.0-beta.4.bin

esptool.py --chip esp32 --port COM10 --baud 460800 write_flash -z 0x1000 ./firmware/esp32-20190125-v1.10.bin

```