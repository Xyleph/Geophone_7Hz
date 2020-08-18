'''
Ce script vise a enregistrer en format wav des signaux contenus dans un fichier json. En particulier, il a ete developpe pour les test sur le geophone.
Lors de l'enregistrement, le script js ou arduino/python enregistre les valeurs lues dans un json et separe les 3 voies en 3 paires key:object.
Pour le moment, le script converti seulement la voie a en wav. Il serait interessant d'ajouter la fonctionnalite de convertir les autres. Avec une technique comme dans json2graph.py?
Par exemple : si on veut convertir le fichier ~/Desktop/test/enregistrement.json, il faut ecrire la commande "python3 json2wav.py file=~/Desktop/test/enregistrement.json"
Les path relatif (a l'emplacement de json2graph.py) sont egalement supporte.
Pour le moment, le sample rate du wav est hardcoded dans la commande wav.read
'''

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
