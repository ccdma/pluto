import matplotlib.pyplot as plt
import numpy as np
from madi import code, algo
from madi.static import *

def split_map_mean(arr: np.ndarray, chunks: int):
    arr_spl = []
    for d in np.split(arr, chunks):
        arr_spl.append(np.mean(d))
    return np.array(arr_spl)

def load(filename: str):
    dump = np.loadtxt(filename, delimiter=',')
    return dump[0] + dump[1]*1j

def preprocess(data: np.ndarray):
    data = data[1000:1400]

    # 重心移動
    data = data - np.mean(data)

    # 振幅平均が1になるように正規化
    # data = data / np.mean(np.abs(data))

    # 円周上に正規化
    # data = data / np.abs(data)

    # 回転補正
    LAG = -0.006043094190666974
    # data = algo.fix_rf_rotate(data, LAG)
    return data

def figconf(fig: plt.Figure, ultxt: str):
    fig.tight_layout()
    fig.text(0.01, 0.01, ultxt, fontsize=7)

T = 587

IN_FILE = f"t{T}-pri-1212.csv"
# IN_FILE = f"t{T}-ov-pri-1212.csv"

# IN_FILE = f"t{T}-pri.csv"
# IN_FILE = f"a.csv"

OUT_FILE = f"{IN_FILE}.png"

RF_PARAM_DESC = f"sample_rate={hprint(DEFAULT_SAMPLE_RATE)}, lo={hprint(DEFAULT_RX_LO)}, bw={hprint(DEFAULT_RX_BW)}"

data = load(IN_FILE)

## reference code print
# data = code.primitive_root_code(1019, 2, 1)  # reference
# data = np.exp(1j*np.linspace(0, 2*np.pi, T))
# data = np.tile(data, 20); print("warning: use reference code")

data = preprocess(data)

# 原始根符号
# t=n-1から算出したt=nと、実際のt=nにおける受信符号の差
# fig, ax = plt.subplots()
# Q = 2
# # pdata = 0となることが期待される
# pdata = algo.cmod(np.angle(data)[1:] - np.angle(data)[:-1]*Q)[:8000]
# print(f"primitive: var={np.var(pdata)}")
# chunks = 50
# pdata_spl = split_map_mean(pdata, chunks)
# ax.plot(pdata_spl, marker='o', markersize=3)
# ax.grid(True, axis='y')
# ax.set_xlabel("time [1sec/sample_rate]")
# ax.set_ylabel(f"code[t+1] - {Q}*code[t] [rad]")
# fig.suptitle(f"""
# Argument difference of primitive root code
# (t={T}, {RF_PARAM_DESC})
# """.strip())
# figconf(fig, IN_FILE)
# fig.savefig(OUT_FILE)

# sine wave
# t=n-1から算出したt=nと、実際のt=nにおける受信符号の差
# fig, ax = plt.subplots()
# # pdata = 0となることが期待される
# pdata = algo.cmod(np.angle(data)[1:] - np.angle(data)[:-1] - 2*np.pi/T)[:8000]
# print(f"sin: avg={np.mean(pdata)}[rad]")
# chunks = 50
# pdata_spl = split_map_mean(pdata, chunks)
# ax.plot(pdata_spl, marker='o', markersize=3, label="raw")
# ax.set_ylim(-0.0042, 0.012)
# ax.hlines([np.mean(pdata_spl)], 0, chunks, "red", linestyles='dashed', lw=2)
# ax.grid(True, axis='y')
# ax.set_xlabel("chunks [1sec/sample_rate]")
# ax.set_ylabel(f"code[t+1] - code[t] - 2pi/{T} [rad]")
# fig.suptitle(f"""
# Argument difference of sine wave
# (t={T}, {RF_PARAM_DESC})
# """.strip())
# figconf(fig, IN_FILE)
# fig.legend()
# fig.savefig(OUT_FILE)


fig, axes = plt.subplots(nrows=1, ncols=2, squeeze=False)
axes = np.ravel(axes)
size = 100

for i, ax in enumerate(axes):
    start = (i+1)*(100)
    pdata = data[start:start+size]
    ax.scatter(pdata.real, pdata.imag, s=0.4)
    ax.plot(pdata.real, pdata.imag, lw=0.2, color='blue')

data = preprocess(load(f"t{T}-ov-pri-1212.csv"))
for i, ax in enumerate(axes):
    start = (i+1)*(100)
    pdata = data[start:start+size]
    ax.scatter(pdata.real, pdata.imag, s=0.4)
    ax.plot(pdata.real, pdata.imag, lw=0.2, color='orange')

    ## 始点と終点の偏角差
    # ax.plot([pdata[0].real, 0, pdata[-1].real], [pdata[0].imag, 0, pdata[-1].imag], lw=2.0, color='red')
    # ax.text(-0.3, 0.4, f"{np.round(np.abs(np.angle(pdata[0])-np.angle(pdata[-1])), 4)}\n[rad]")

    ## 重心
    # center = np.mean(pdata)
    # ax.scatter(center.real, center.imag, s=15, color='red', marker='x')
    # ax.text(-0.3, 0.4, f"{np.round(center, 2)}", size=8)
    
    ax.set_title(f"{start}-{start+size} (n={size})")
    ax.set_aspect('equal')
    ax.grid(True, axis='both')



fig.suptitle(f"""
IQ plot {RF_PARAM_DESC}
(t={T}, orange=oversampling, blue=normal)
""".strip())
figconf(fig, IN_FILE)
fig.savefig(OUT_FILE)
