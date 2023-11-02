import matplotlib.pyplot as plt
import numpy as np
from madi import code
from madi.static import *

def args_mul(arr: np.ndarray, n: int):
    arg1 = np.angle(arr[:-1])*n
    arg2 = np.angle(arr[1:])
    divarg = np.mod(arg2 - arg1 + np.pi, 2*np.pi) - np.pi
    return np.mean(np.abs(divarg))

IN_FILE = f"a.csv"
OUT_FILE = f"{IN_FILE}.png"

dump = np.loadtxt(IN_FILE, delimiter=',')
data = dump[0] + dump[1]*1j

## reference code print
# data = code.primitive_root_code(1019, 2, 1)  # reference
# data = np.sin(np.linspace(0, 2*np.pi, 1024)) + 1j*np.cos(np.linspace(0, 2*np.pi, 1024))
# data = np.tile(data, 20); print("warning: use reference code")

data = data[1000:10000]
# 円周上に正規化
# data = data / np.abs(data)


# argument
fig, ax = plt.subplots()
argplt = []
for arr in np.split(data, 100):
    argplt.append(args_mul(arr, n=2))
ax.plot(argplt, marker='o', markersize=5)
ax.set_title("argument difference for x_1 - x_0*2 [rad]")
ax.set_xlabel("chunck")
ax.set_ylabel("argument [rad]")

fig.tight_layout()
fig.savefig(OUT_FILE)

# plot iq
fig, axes = plt.subplots(nrows=2, ncols=2, squeeze=False)
axes = np.ravel(axes)
size = 1024
for i, ax in enumerate(axes):
    start = (i+1)*1000
    pdata = data[start:start+size]
    ax.scatter(pdata.real, pdata.imag, s=0.4)
    ax.plot(pdata.real, pdata.imag, lw=0.2)
    ax.set_title(f"{start}-{start+size}")
    ax.set_aspect('equal')
fig.suptitle(f"IQ plot of sine wave \n(T=1024, SAMPLE_RATE=5M, LO=923MHz,BANDWIDTH=10Mz)")
fig.tight_layout()
fig.savefig(OUT_FILE)
