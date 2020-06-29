import matplotlib.pyplot as plt
import numpy as np
import os

path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)
files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
files.reverse()

for one_file in files:
    if one_file[-4:] == ".txt":
        newest = one_file
        break

print("Opening:", newest)

f = open(newest, "r")

data = f.read()
start = False
a_value = []
b_value = []
count = 0

for x in range(len(data)):

    if start:
        if data[x] == 'a' and data[x+1] == ':':
            if data[x+2] != 'N':
                a_value.append(float(data[x+2] + data[x+3] + data[x+4] + data[x+5] + data[x+6]))

        if data[x] == 'b' and data[x+1] == ':':
            if data[x+2] != 'N':
                b_value.append(float(data[x+2] + data[x+3] + data[x+4] + data[x+5] + data[x+6]))

    if data[x] == 'r' and data[x+1] == 'x' and data[x+3] == '0' and data[x+4] == '0' and data[x+5] == '0' and data[x+6] == '1' and data[x+11] != 'N':
        print(count)
        count += 1
        start = True        

f.close()

plt.plot(a_value)
plt.yticks(np.arange(1.75,2,0.001))
plt.grid(b = True, which = 'both')
#plt.plot(b_value)

plt.show()
