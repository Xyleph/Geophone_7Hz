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
				sr_dict = data.get("sr")
				sr_dict = sr_dict.items()
				for x in sr_dict:
					sr = x[1]
				time_limit = arg[4:].split(".")
				plt.xlim(int(sr)*int(time_limit[0]), int(sr)*int(time_limit[1]))

		plt.legend()
		plt.grid(b = True, which = 'both')
		plt.show()

if __name__ == "__main__":
	main()
