'''
La fonction getlatest permet de trouver le fichier le plus recent ayant une extension particuliere en ajoutant l'argument file=path/to/search
Elle supporte de specifier un path absolu ou relatif. Si un dossier est specifie, la fonction trouve le fichier le plus recent du bon type.
On peut egalement specifier un fichier en particulier.
Si aucun argument "file=..." est donne, la fonction utilise le path en parametre (path du main).
'''

import os

def _getlatestfrompath(path, ext):
	ext_len = len(ext)
	os.chdir(path)
	files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
	files.reverse()

	for one_file in files:
		if one_file[-ext_len:] == ext:
			return one_file

def getlatest(path, ext, args):
	# path : base des path relatifs et path a verifier si aucun argument est donne.
	# ext  : string avec le type de fichier a chercher (eg:".wav")
	# args : arguments de la commande qui provient du main. Utiliser sys.argv
	default = True
	for arg in args:
		if arg[:5] == "file=":
			if arg[5] == "/" or arg[5] == "~":
				if arg[-len(ext):] == ext:
					toopen = arg[5:]
					default = False
				else:
					path = arg[5:]
					toopen = _getlatestfrompath(path, ext)
					default = False
			elif arg[-len(ext):] == ext:
				toopen = path + "/" + arg[5:]
				default = False
			else:
				path += "/" + arg[5:]
				toopen = _getlatestfrompath(path, ext)
				default = False
		elif default:
			toopen = _getlatestfrompath(path, ext)
	if toopen is None:
		print(f"No file of type {ext} found in specified directory\nIf not directory was not specified, add file=target/directory/here to the command")
	return toopen


