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

sdrs = [
    adi.Pluto(find_device("f24", DEVICES).uri_usb),
    # adi.Pluto(find_device("9ce", DEVICES).uri_usb),
]

for sdr in sdrs:
    sdr.tx_lo = DEFAULT_TX_LO
    sdr.tx_rf_bandwidth = DEFAULT_TX_BW
    sdr.sample_rate = DEFAULT_SAMPLE_RATE
    sdr.tx_cyclic_buffer = True
    destroy(sdr)

print("start sending")

sdrs[0].tx(primitive_root_code(1019, 2, 1)*1024*2)
# sdrs[1].tx(primitive_root_code(53, 2, 2)*10)

sleep(8.0)
for sdr in sdrs:
    destroy(sdr)
