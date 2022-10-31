from os import path, listdir, system
from glob import glob

class DS18B20_Units:
    DEGREES_CELSIUS = 0x1
    DEGREES_FARENHEIT = 0x2
    KELVIN = 0x3
    FACTORS = {
        DEGREES_CELSIUS: lambda x: x * 0.001,
        DEGREES_FARENHEIT: lambda x: x * 0.001 * 1.8 + 32.0,
        KELVIN: lambda x: x * 0.001 + 273.15
    }

class DS18B20:
    BASE_DIRECTORY = "/sys/bus/w1/devices"
    SLAVE_PREFIX = "28-"
    SLAVE_FILE = "w1_slave"

    def __init__(self, sensor_id=None, load_kernel_mods=True):
        self._type = "DS18B20"
        self._id = sensor_id
        if load_kernel_mods:
            self._load_kernel_mods()
        self._sensor = self._get_sensor()

    @property
    def get_id(self) -> object:
        return self._id

    @property
    def get_type(self) -> str:
        return self._type

    def does_exist(self):
        path = self._get_sensor()
        return path is not None and path != ""

    def get_current_temp(self, unit=DS18B20_Units.DEGREES_CELSIUS) -> float:
        ff = self._get_unit_factor(unit)
        vv = self._get_sensor_value()
        return ff(vv)

    def get_current_temps(self, units) -> object:
        vv = self._get_sensor_value()
        temps = []
        for unit in units:
            factor = self._get_unit_factor(unit)
            temps.append(factor(vv))
        return temps

    @classmethod
    def get_installed_sensors(cls) -> object:
        ret = []
        for sensor in listdir(cls.BASE_DIRECTORY):
            if sensor.startswith(cls.SLAVE_PREFIX):
                ret.append(sensor[3:])
        return ret

    @classmethod
    def get_all_sensors(cls) -> object:
        return [DS18B20(id) for id in cls.get_installed_sensors()]

    @staticmethod
    def _get_unit_fac(self, unit):
        return DS18B20_Units.FACTORS[unit]

    def _get_sensor(self) -> str:
        sensors = self.get_installed_sensors()
        assert self._id in sensors
        if not self._id and sensors:
            self._id = sensors[0]
        return path.join(self.BASE_DIRECTORY, self.SLAVE_PREFIX + str(self._id), self.SLAVE_FILE)

    def _get_sensor_value(self) -> float:
        with open(self._sensor, "r") as f:
            data = f.readlines()
        assert data[0].strip()[-3:] == "YES"
        return float(data[1].split("=")[1])

    @staticmethod
    def _load_kernel_modules(self):
        system("modprobe w1-gpio")
        system("modprobe w1-therm")
