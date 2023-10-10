import matplotlib.pyplot as plt
import numpy as np

FILENAME = "a.csv"

dump = np.loadtxt(FILENAME, delimiter=',')
data = dump[0] + dump[1]*1j

data = data[1000:1050]

# 円周上に正規化
data = data / np.abs(data)

fig, ax = plt.subplots()
ax.scatter(data.real, data.imag, s=0.4)
ax.plot(data.real, data.imag, lw=0.2)
ax.set_aspect('equal')
fig.tight_layout()
fig.savefig("1.png")
