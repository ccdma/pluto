import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

IN_FILE = f"a.csv"
OUT_FILE = f"{IN_FILE}.png"

dump = np.loadtxt(IN_FILE, delimiter=',')
data = dump[0] + dump[1]*1j

start = 10000
size = 100
data = data[start:start+size]

# 円周上に正規化
data = data / np.abs(data)

fig, ax = plt.subplots()
ax.scatter(data.real, data.imag, s=0.4)
ax.plot(data.real, data.imag, lw=0.2)
ax.set_aspect('equal')
fig.tight_layout()
fig.savefig(OUT_FILE)
