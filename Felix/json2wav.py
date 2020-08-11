import os
from json import load as load
import scipy.io.wavfile as wav
from numpy import array

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
data = load(f)
a_value = data.get("a")
a_value = a_value.items()

for x in a_value:
    a.append(x[1])

a = a[1:]
f.close()

a_norm = [float(i)/max(a) for i in a]

a_norm = array(a_norm)

wav.write("TestWrite.wav", 44100, a_norm)