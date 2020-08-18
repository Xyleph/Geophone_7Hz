import os

def getlatestfrompath(path, ext):
	ext_len = len(ext)
	os.chdir(path)
	files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
	files.reverse()

	for one_file in files:
		if one_file[-ext_len:] == ext:
			return one_file


def getlatest(path, ext, args):
	default = True
	for arg in args:
		if arg[:5] == "file=":
			if arg[5] == "/" or arg[5] == "~":
				if arg[-len(ext):] == ext:
					toopen = arg[5:]
					default = False
				else:
					path = arg[5:]
					toopen = getlatestfrompath(path, ext)
					default = False
			elif arg[-len(ext):] == ext:
				toopen = path + "/" + arg[5:]
				default = False
			else:
				path += "/" + arg[5:]
				toopen = getlatestfrompath(path, ext)
				default = False
		elif default:
			toopen = getlatestfrompath(path, ext)
	return toopen


