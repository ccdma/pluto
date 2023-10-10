from madi.locate import get_devices, find_device
from madi.static import *
import adi, csv
import numpy as np
from time import sleep

def destroy(sdr: adi.Pluto):
    sdr.tx_destroy_buffer()
    sdr.rx_destroy_buffer()

def save_csv(filename: str, arr: np.ndarray):
    with open(filename, "w+") as f:
        c = csv.writer(f)
        c.writerow(arr.real)
        c.writerow(arr.imag)

DEVICES = get_devices()
BUFFER_SIZE = int(1*MHz)

sdr = adi.Pluto(find_device("d87", DEVICES).uri_usb)

sdr.rx_lo = DEFAULT_RX_LO
sdr.rx_rf_bandwidth = DEFAULT_RX_BW
sdr.sample_rate = DEFAULT_SAMPLE_RATE
sdr.rx_buffer_size = BUFFER_SIZE
destroy(sdr)

sleep(1.0)
samplings = np.array(sdr.rx())
save_csv("a.csv", samplings)
