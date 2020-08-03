import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import os
import json

path = os.path.dirname(os.path.realpath(__file__))
path += "/payload"
os.chdir(path)
files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
files.reverse()

for one_file in files:
    if one_file[-5:] == ".json":
        newest = one_file
        break
print("Opening:", newest)

a = []

f = open(newest, "r")
data = json.load(f)
a_value = data.get("c")
print(a_value)
a_value = a_value.items()

for x in a_value:
    a.append(x[1])

a = a[1:]
f.close()

fig, ax = plt.subplots()
ax.plot(a, marker = ".")
ax.yaxis.set_major_locator(MultipleLocator(0.1))
ax.yaxis.set_minor_locator(MultipleLocator(0.01))

plt.grid(b = True, which = 'both')

plt.show()

