import matplotlib.pyplot as plt
import numpy as np

FILENAME = "a.csv"

dump = np.loadtxt(FILENAME, delimiter=',')
data = dump[0] + dump[1]*1j

data = data[1000:1100]
plt.scatter(data.real, data.imag, s=0.4)
plt.plot(data.real, data.imag, lw=0.2)
plt.savefig("1.png")
