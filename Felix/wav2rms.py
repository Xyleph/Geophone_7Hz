import numpy as np
import sys
import scipy.io.wavfile as wav

args = sys.argv

sr, data = wav.read("/home/pi/Desktop/Felix/results_tests_2020-08/G08_394C06_1.wav")
data = data[:,1]

for arg in args:
	if arg[:4] == "sec=":
		time_limit = arg[4:].split(".")
		data = data[sr*int(time_limit[0]):sr*int(time_limit[1])]

rms = np.sqrt(np.mean(data**2))

print(rms)
