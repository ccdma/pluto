import adi

def destroy(sdr: adi.Pluto):
    sdr.tx_destroy_buffer()
    sdr.rx_destroy_buffer()
