# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
import gc
import micropython

# import webrepl
# webrepl.start()
gc.collect()
micropython.mem_info()

