import machine, onewire, ds18x20, time
import settings
import uasyncio as asyncio
from homie.device import HomieDevice, await_ready_state
from homie.node import HomieNode
from homie.property import HomieProperty
from homie.constants import FLOAT
from machine import Pin

class DallasSensorNode(HomieNode):
    def __init__(self, name="Temp & Humid", pin=4, interval=60, pull=-1):
        super().__init__(id="ds18x20", name=name, type="ds18x20")
        print("* Init DallasSensorNode")
        self.pin = machine.Pin(pin)
        self.sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
        self.interval = interval

        self.roms = ds_sensor.scan()
        print('Found DS devices: ', roms)
        self.p_temp = HomieProperty(
            id="temperature",
            name="Temperature",
            datatype=FLOAT,
            format="-40:80",
            unit="°C",
        )
        self.add_property(self.p_temp)
        asyncio.create_task(self.update_data())

    @await_ready_state
    async def update_data(self):
        sensor = self.sensor
        roms = self.roms
        delay = self.interval * 1000
        while True:
            sensor.convert_temp()
            time.sleep_ms(750)
            for rom in roms:
                print(rom)
                print(sensor.read_temp(rom))
            await asyncio.sleep_ms(delay)