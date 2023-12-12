M = 1000*1000
K = 1000
DEFAULT_TX_LO = 923*M
DEFAULT_RX_LO = 923*M
DEFAULT_TX_BW = int(1*M)
DEFAULT_RX_BW = int(1*M)
DEFAULT_SAMPLE_RATE = int(2*M)

def hprint(val: int|float):
    if val < 1*K:
        return f"{val}"
    elif val < 1*M:
        return f"{val/K}K"
    else:
        return f"{val/M}M"
