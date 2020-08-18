'''
Ce script vise a grapher des signaux contenus dans un fichier json. En particulier, il a ete developpe pour les test sur le geophone.
Lors de l'enregistrement, le script js ou arduino/python enregistre les valeurs lues dans un json et separe les 3 voies en 3 paires key:object.
Pour voir le graphique, il faut specifier quelles voies afficher dans la commande. Il est egalement possible de specifier un fichier ou un dossier a traiter
Par exemple : si on veut voir la voie b et c du fichier ~/Desktop/test/enregistrement.json, il faut ecrire la commande "python3 json2graph.py b c file=~/Desktop/test/enregistrement.json"
Les path relatif (a l'emplacement de json2graph.py) sont egalement supporte. On peut egalement specifier un range en x avec l'argument "sec=debut.fin" ouu debut et fin sont des entiers
Pour le moment, la commande sec= assume un sample rate de 2000S/s.
'''

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import os
import sys
import json
from utils import getlatest

def graph(channel, name, data, color):
	value = data.get(name)
	value = value.items()
	
	for x in value:
		channel.append(x[1])
    
	channel = channel[1:]
    
	plt.plot(channel, label = name, color = color)

errmsg = f"Channel(s) to be plotted need to be added as arguments (eg:python3 {sys.argv[0]} a b c)"

def main():
	args = sys.argv
	try:
		args[1] == "something"
	except IndexError:
		print(errmsg)
	else:
		path = os.path.dirname(os.path.realpath(__file__))
		toopen = getlatest(path, ".json", args)
		print("Opening:", toopen)

		f = open(toopen, "r")
		data = json.load(f)
		f.close()
		
		for arg in args:
			if arg == "a":
				a = []
				graph(a, "a", data, "red")
			
			if arg == "b":
				b = []
				graph(b, "b", data, "blue")
			
			if arg == "c":
				c = []
				graph(c, "c", data, "green")
			
			if arg[:4] == "sec=":
#				sr_dict = data.get("sr")
#				sr_dict = sr_dict.items()
#				for x in sr_dict:
#					sr = x[1]
				sr = 2000
				time_limit = arg[4:].split(".")
				plt.xlim(int(sr)*int(time_limit[0]), int(sr)*int(time_limit[1]))

		plt.legend()
		plt.grid(b = True, which = 'both')
		plt.show()

if __name__ == "__main__":
	main()
