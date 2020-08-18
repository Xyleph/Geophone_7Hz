import os
import sys
from json import load as load
import scipy.io.wavfile as wav
import numpy as np
from utils import getlatest

args = sys.argv
path = os.path.dirname(os.path.realpath(__file__))
toopen = getlatest(path, ".json", args)
print(f"Opening : {toopen}")

a = []

f = open(toopen, "r")
data = load(f)
a_value = data.get("a")
a_value = a_value.items()

for x in a_value:
    a.append(x[1])

a = a[1:]
f.close()
a = np.array(a)

rms = np.sqrt(np.mean(a**2))
a = a - rms

a_norm = a/max(abs(a))

print(f"Max : {max(a_norm)} Min : {min(a_norm)}")

out_name = toopen.split("/")
out_name = out_name[-1]
wav.write(f"{out_name[:-5]}_geo.wav", 1810, a_norm)
