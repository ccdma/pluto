import matplotlib.pyplot as plt
import numpy as np
from madi import code
from madi.static import *

# [-π, π]に射影
def cmod(args: np.ndarray):
    return np.mod(args + np.pi, 2*np.pi) - np.pi

def args_mul(arr: np.ndarray, n: int):
    arg1 = np.angle(arr[:-1])*n
    arg2 = np.angle(arr[1:])
    divarg = cmod(arg2 - arg1)
    return np.mean(np.abs(divarg))

T = 1024

IN_FILE = f"t{T}-sin.csv"
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

def figconf(fig: plt.Figure):
    fig.tight_layout()
    fig.text(0.01, 0.01, IN_FILE, fontsize=7)

# argument
fig, ax = plt.subplots()
argplt = []
for arr in np.split(data, 100):
    argplt.append(args_mul(arr, n=2))
ax.plot(argplt, marker='o', markersize=5)
ax.set_title("argument difference for x_1 - x_0*2 [rad]")
ax.set_xlabel("chunck")
ax.set_ylabel("argument [rad]")
figconf(fig)
# fig.savefig(OUT_FILE)

fig, ax = plt.subplots()
pdata = cmod(np.angle(data)[1:] - np.angle(data)[:-1])[:1000]
ax.plot(pdata)
ax.grid(True, axis='y')
ax.set_xlabel("time [1/sample_rate]")
ax.set_ylabel("argument [rad]")
ax.text(0.03, 0.14, f"average={np.round(np.mean(pdata), 4)}[rad]", size=10)
ax.text(0.03, 0.17, f"expected=-{np.round(np.pi*2/T, 4)}[rad]", size=10)
fig.suptitle(f"""
Argument difference of sine wave
(t={T}, sample_rate={hprint(DEFAULT_SAMPLE_RATE)}, lo={hprint(DEFAULT_RX_LO)}, bw={hprint(DEFAULT_RX_BW)})
""".strip())
figconf(fig)
fig.savefig(OUT_FILE)

# plot iq
fig, axes = plt.subplots(nrows=2, ncols=2, squeeze=False)
axes = np.ravel(axes)
size = int(T/2)
for i, ax in enumerate(axes):
    start = (i+1)*400
    pdata = data[start:start+size]
    ax.scatter(pdata.real, pdata.imag, s=0.4)
    ax.plot(pdata.real, pdata.imag, lw=0.2, color='darkblue')

    ## 始点と終点の偏角差
    # ax.plot([pdata[0].real, 0, pdata[-1].real], [pdata[0].imag, 0, pdata[-1].imag], lw=2.0, color='red')
    # ax.text(-0.3, 0.4, f"{np.round(np.abs(np.angle(pdata[0])-np.angle(pdata[-1])), 4)}\n[rad]")

    ## 重心
    # center = np.mean(pdata)
    # ax.scatter(center.real, center.imag, s=15, color='red', marker='x')
    # ax.text(-0.3, 0.4, f"{np.round(center, 2)}", size=8)
    
    ax.set_title(f"{start}-{start+size}")
    ax.set_aspect('equal')
    ax.grid(True, axis='both')

fig.suptitle(f"""
IQ plot of sine wave
(t={T}, sample_rate={hprint(DEFAULT_SAMPLE_RATE)}, lo={hprint(DEFAULT_RX_LO)}, bw={hprint(DEFAULT_RX_BW)})
""".strip())
figconf(fig)
# fig.savefig(OUT_FILE)
