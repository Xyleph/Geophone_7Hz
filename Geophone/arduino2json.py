'''
Ce script sert a lire les donnees provenant d'un arduino et a les organiser en json. En particulier, il a ete developpe pour les test sur le geophone.
Le arduino qui acquiert les donnes doit simplement envoyer, sur le port serial, un string du format "data1,data2,data3" ou dataN est la lecture analogique de la voie N.
Pour utiliser, il faut specifier la duree de l'enregistrement lors de la commande. Par exemple, pour demarer un enregistrement de 50 secondes, il faut ecrire "python3 arduino2json.py 50"
'''

# Avec baud rate de 220000 --> environ 1810 S/s

import serial
import time
import json
import sys

t_0 = 0
count = 0
sample = 0
sec = 0
a_data = {}
b_data = {}
c_data = {}

ser = serial.Serial('/dev/ttyACM0',220000)								#Ouvre le port serial du arduino
sec_tot = int(sys.argv[1])

while True:
	if(t_0 == 0):
		t_0 = time.time_ns()
	
	read_serial=str(ser.readline())
	
	if len(read_serial) > 10 and len(read_serial) < 21:					#Une lecture de taille differente signifie une erreur
		read_serial = read_serial[2:-5]
		split = read_serial.split(",")
		a_data[count] = float(split[0])*(5/1024)						#Converti la valeur de l'adc (0-1024) en volts
		b_data[count] = float(split[1])*(5/1024)
		c_data[count] = float(split[2])*(5/1024)
	
	if(time.time_ns()-t_0 > 1000000000):
		print(f"{sample} echantillions a la seconde {sec}")				#Donne le sample rate pour la seconde qui vient de se terminer
		sec +=1
		sample = 0
		t_0 = 0
	
	if(sec > sec_tot):
		tojson = {
			"a":a_data,
			"b":b_data,
			"c":c_data
		}
		
		with open('arduino_json.json', 'w') as json_file:
			json.dump(tojson, json_file)
		break

	count += 1
	sample += 1

print("Done.")
