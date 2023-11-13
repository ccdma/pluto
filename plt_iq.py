import matplotlib.pyplot as plt
import numpy as np
from madi import code, algo
from madi.static import *

T = 64

IN_FILE = f"t{T}-sin.csv"
# IN_FILE = f"t{T}-pri.csv"
# IN_FILE = f"a.csv"

OUT_FILE = f"{IN_FILE}.png"

RF_PARAM_DESC = f"sample_rate={hprint(DEFAULT_SAMPLE_RATE)}, lo={hprint(DEFAULT_RX_LO)}, bw={hprint(DEFAULT_RX_BW)}"

def figconf(fig: plt.Figure):
    fig.tight_layout()
    fig.text(0.01, 0.01, IN_FILE, fontsize=7)

dump = np.loadtxt(IN_FILE, delimiter=',')
data = dump[0] + dump[1]*1j

## reference code print
# data = code.primitive_root_code(1019, 2, 1)  # reference
# data = np.sin(np.linspace(0, 2*np.pi, 1024)) + 1j*np.cos(np.linspace(0, 2*np.pi, 1024))
# data = np.tile(data, 20); print("warning: use reference code")

data = data[1000:10000]
# 円周上に正規化
# data = data / np.abs(data)

# 回転補正
LAG = 2*np.pi - 0.005510028883016813
data = algo.fix_rf_rotate(data, LAG)

def args_mul(arr: np.ndarray, n: int):
    arg1 = np.angle(arr[:-1])*n
    arg2 = np.angle(arr[1:])
    divarg = algo.cmod(arg2 - arg1)
    return np.mean(np.abs(divarg))

# fig, ax = plt.subplots()
# argplt = []
# for arr in np.split(data, 100):
#     argplt.append(args_mul(arr, n=2))
# ax.plot(argplt, marker='o', markersize=5)
# ax.set_title("argument difference for x_1 - x_0*2 [rad]")
# ax.set_xlabel("chunck")
# ax.set_ylabel("argument [rad]")
# figconf(fig)
# fig.savefig(OUT_FILE)


fig, ax = plt.subplots()
pdata = algo.cmod(np.angle(data)[1:] - np.angle(data)[:-1])[:8000]
ax.plot(pdata)
ax.grid(True, axis='y')
ax.set_xlabel("time [1/sample_rate]")
ax.set_ylabel("argument [rad]")
fig.suptitle(f"""
Argument difference of sine wave
(t={T}, {RF_PARAM_DESC})
""".strip())
figconf(fig)
fig.savefig(OUT_FILE)
average = np.mean(pdata)
expected = np.pi*2/T
print(f"average={average}[rad]")
print(f"expected={expected}[rad]")
print(- average - expected)


fig, axes = plt.subplots(nrows=2, ncols=2, squeeze=False)
axes = np.ravel(axes)
size = T
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
(t={T}, {RF_PARAM_DESC})
""".strip())
figconf(fig)
fig.savefig(OUT_FILE)
