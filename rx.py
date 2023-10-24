from madi.locate import get_devices, find_device
from madi.operate import destroy
from madi.static import *
from madi.code import *
import adi, csv
import numpy as np
from time import sleep

OUT_FILE = f"a.csv"

def save_csv(filename: str, arr: np.ndarray):
    with open(filename, "w+") as f:
        c = csv.writer(f)
        c.writerow(arr.real)
        c.writerow(arr.imag)

DEVICES = get_devices()
BUFFER_SIZE = int(1*MHz)

sdr = adi.Pluto(find_device("f24", DEVICES).uri_usb)

sdr.rx_lo = DEFAULT_RX_LO
sdr.rx_rf_bandwidth = DEFAULT_RX_BW
sdr.sample_rate = DEFAULT_SAMPLE_RATE
sdr.rx_buffer_size = BUFFER_SIZE

sdr.tx_lo = DEFAULT_TX_LO
sdr.tx_rf_bandwidth = DEFAULT_TX_BW
sdr.tx_cyclic_buffer = True
destroy(sdr)
sdr.tx(primitive_root_code(1019, 2, 1)*1024*2)

sleep(3.0)
samplings = np.array(sdr.rx())
save_csv(OUT_FILE, samplings)
destroy(sdr)
