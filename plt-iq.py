import matplotlib.pyplot as plt
import numpy as np
from madi import code
from madi.static import *

def args_mul(arr: np.ndarray, n: int):
    arg1 = np.angle(arr[:-1])*n
    arg2 = np.angle(arr[1:])
    divarg = np.mod(arg2 - arg1 + np.pi, 2*np.pi) - np.pi
    return np.mean(np.abs(divarg))

IN_FILE = f"t512-sin.csv"
# IN_FILE = f"a.csv"
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
# fig.savefig(OUT_FILE)

# plot iq
fig, axes = plt.subplots(nrows=2, ncols=4, squeeze=False)
axes = np.ravel(axes)
size = 512
for i, ax in enumerate(axes):
    start = (i+1)*400
    pdata = data[start:start+size]
    ax.scatter(pdata.real, pdata.imag, s=0.4)
    ax.plot(pdata.real, pdata.imag, lw=0.2, color='darkblue')
    # ax.plot([pdata[0].real, 0, pdata[-1].real], [pdata[0].imag, 0, pdata[-1].imag], lw=2.0, color='red')
    # ax.text(-0.3, 0.4, f"{np.round(np.abs(np.angle(pdata[0])-np.angle(pdata[-1])), 4)}\n[rad]")
    ax.set_title(f"{start}-{start+size}")
    ax.set_aspect('equal')
fig.suptitle(f"""
IQ plot of sine wave
(t=512, sample_rate={hprint(DEFAULT_SAMPLE_RATE)}, lo={hprint(DEFAULT_RX_LO)}, bw={hprint(DEFAULT_RX_BW)})
""".strip())
fig.tight_layout()
fig.savefig(OUT_FILE)
