from madi.locate import get_devices, find_device
from madi.operate import destroy
from madi.code import *
from madi.static import *
import adi
import numpy as np
from time import sleep



np.random.seed(1)

DEVICES = get_devices()
BUFFER_SIZE = int(1*MHz)

sdr = adi.Pluto(find_device("f24", DEVICES).uri_usb)

sdr.tx_lo = DEFAULT_TX_LO
sdr.tx_rf_bandwidth = DEFAULT_TX_BW
sdr.sample_rate = DEFAULT_SAMPLE_RATE
sdr.tx_cyclic_buffer = True
destroy(sdr)
print("start sending")
sdr.tx(primitive_root_code(1019, 2, 1)*10)
sleep(8.0)
destroy(sdr)
