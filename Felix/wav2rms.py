import numpy as np
import sys
import os
import scipy.io.wavfile as wav
from utils import getlatest

args = sys.argv
path = os.path.dirname(os.path.realpath(__file__))
toopen = getlatest(path, ".wav", args)
print(f"Opening : {toopen}")

sr, data = wav.read(toopen)
print(f"Lu a {sr} Hz")

if data.ndim == 2:
	data = data[:,1]
	print(f"Fichier stereo : seule la partie droite est traite")

for arg in args:
	if arg[:4] == "sec=":
		time_limit = arg[4:].split(".")
		print(f"Using time {int(time_limit[0])} to {int(time_limit[1])}")
		data = data[sr*int(time_limit[0]):sr*int(time_limit[1])]

data = data.astype(np.int64)

rms = np.sqrt(np.mean(data**2))

print(rms)
