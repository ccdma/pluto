import numpy as np


"""
RFの回転を補正する
- const_lag_rad分毎回回転する想定で修正をかける
"""
def fix_rf_rotate(iq: np.ndarray, const_lag_rad: float):
    fiq = np.empty(len(iq), dtype=np.complex128)
    lag_acc = np.exp(1j*0)
    for i in range(len(iq)-1):
        fiq[i] = iq[i] * lag_acc
        lag_acc *= np.exp(1j*const_lag_rad)
    return fiq

# [-π, π]に射影
def cmod(args: np.ndarray):
    return np.mod(args + np.pi, 2*np.pi) - np.pi
