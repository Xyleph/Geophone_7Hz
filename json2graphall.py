import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import os
import sys
import json

def graph(channel, name, data):
	value = data.get(name)
	value = value.items()
	
	for x in value:
		channel.append(x[1])
    
	channel = channel[1:]
    
	plt.plot(channel, label = name)


def main():
	arg = sys.argv
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

	f = open(newest, "r")
	data = json.load(f)
	f.close()

	try:
		arg.index("a")
	except:
		print("A channel not graphed")
	else:
		a = []
		graph(a, "a", data)
		
	try:
		arg.index("b")
	except:
		print("B channel not graphed")
	else:
		b = []
		graph(b, "b", data)
		
	try:
		arg.index("c")
	except:
		print("C channel not graphed")
	else:
		c = []
		graph(c, "c", data)

	plt.legend()
	plt.grid(b = True, which = 'both')
	plt.show()

if __name__ == "__main__":
	main()
