import matplotlib.pyplot as plt
import numpy as np
from madi import code, algo
from madi.static import *

T = 269

IN_FILE = f"t{T}-sin.csv"
IN_FILE = f"t{T}-pri.csv"
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

data = data[1000:11000]

# 振幅平均が1になるように正規化
data = data / np.mean(np.abs(data))

# 円周上に正規化
# data = data / np.abs(data)

# 回転補正
LAG = 2*np.pi - 0.005510028883016813
data = algo.fix_rf_rotate(data, LAG)

# 原始根符号
# t=n-1から算出したt=nと、実際のt=nにおける受信符号の差
fig, ax = plt.subplots()
Q = 2
# pdata = 0となることが期待される
pdata = algo.cmod(np.angle(data)[1:] - np.angle(data)[:-1]*Q)[:1000]
ax.plot(pdata, marker='o', markersize=3)
ax.grid(True, axis='y')
ax.set_xlabel("time [1sec/sample_rate]")
ax.set_ylabel("code[t+1] - code[t]*{Q} [rad]")
fig.suptitle(f"""
Argument difference of primitive root code
(t={T}, {RF_PARAM_DESC})
""".strip())
figconf(fig)
# fig.savefig(OUT_FILE)

# sine wave
# t=n-1から算出したt=nと、実際のt=nにおける受信符号の差
fig, ax = plt.subplots()
# pdata = 0となることが期待される
pdata = algo.cmod(np.angle(data)[1:] - np.angle(data)[:-1] + np.pi*2/T)[:1000]
print(f"average={np.mean(pdata)}[rad]")
ax.plot(pdata, marker='o', markersize=3)
ax.hlines([np.mean(pdata)], 0, 1000, "red", linestyles='dashed')
ax.text(100, 0.01, f"{np.round(np.mean(pdata), 7)}", size=10, color='white')
ax.grid(True, axis='y')
ax.set_xlabel("time [1sec/sample_rate]")
ax.set_ylabel("code[t+1] - code[t] + 2pi/T [rad]")
fig.suptitle(f"""
Argument difference of sine wave
(t={T}, {RF_PARAM_DESC})
""".strip())
figconf(fig)
# fig.savefig(OUT_FILE)


fig, axes = plt.subplots(nrows=1, ncols=3, squeeze=False)
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
IQ plot of primitive root code (p,q={T},2)
(t={T}, {RF_PARAM_DESC})
""".strip())
figconf(fig)
fig.savefig(OUT_FILE)
