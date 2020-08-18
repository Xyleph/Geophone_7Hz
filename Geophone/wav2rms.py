'''
Ce script calcul la valeur RMS d'un signal sous format wav.
Il est possible de specifier un interval de temps (en seconde) a prendre en compte.
Il est egalement possible de traiter un signal periodique comme test_pot_vibrant.wav (avec du signal pendant 60s, 5s de silence, signal 60s, 5s de silence, ect)
Pour specifier un interval, utiliser l'argument sec=debut.fin (eg: "python3 wav2rms.py sec=5.50" pour faire le RMS de la seconde 5 a 50)
Pour un signal periodique, il faut utiliser le tag --periodic et ajouter les arguments debut=, duree= et silence= (eg: "python3 wav2rms.py --periodic debut=4 duree=30 silence=5" calcul les valeurs RMS a partir de la seconde 4, en bloc de 30 secondes et fait une pause de 5 secondes entre chaque.
Pour faire le calcul sur tout le signal, utiliser le tag --all (eg: python3 wav2rms.py --all) 
'''
import numpy as np
import sys
import os
import scipy.io.wavfile as wav
from utils import getlatest

args = sys.argv
path = os.path.dirname(os.path.realpath(__file__))
toopen = getlatest(path, ".wav", args)


if toopen is not None:
	print(f"Opening : {toopen}")
	sr, data = wav.read(toopen)
	data = data.astype(np.int64)
	print(f"Lu a {sr} Hz")

	if data.ndim == 2:
		data = data[:,1]
		print(f"Fichier stereo : seule la partie droite est traite")
	
	doall = False
	periodic = False
	
	for arg in args:
		if arg[:4] == "sec=":
			time_limit = arg[4:].split(".")
			print(f"Using time {int(time_limit[0])} to {int(time_limit[1])}")
			data = data[sr*int(time_limit[0]):sr*int(time_limit[1])]

			print(f"RMS : {np.sqrt(np.mean(data**2))}")

		elif arg[:5] == "--all":
			doall = True
		
		elif arg[:10] == "--periodic"
			periodic = True
	if doall:
		print(f"RMS : {np.sqrt(np.mean(data**2))}")
	
	if periodic:
		for arg in args:
			if arg[:6] == "debut=":
				debut = int(arg[6:])
			if arg[:6] == "duree=":
				duree = int(arg[6:])
			if arg[:8] == "silence=":
				silence = int(arg[8:])

		data = data[sr*debut:]
		cycle = duree + silence
		nb_todo = len(data) / (cycle*sr)
		
		for x in range(int(nb_todo)):
			td = x*(duree+silence)+debut
			tf = x*(duree+silence)+debut+duree
			data_buff = data[sr*td:sr*tf]
			print(f"Time : {td}-{tf} RMS : {np.sqrt(np.mean(data_buff**2))}")
