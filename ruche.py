#Bibliotheque du projet ruche

#IMPORT
import grovepi
import time
import os
import smbus

#---------------- COMPOSANTS DE SORTIE - OUTPUT -----
#Partie Buzzer

buzzer = 8 #Le buzzer est connecte au digital port D8 du shield
grovepi.pinMode(buzzer,"OUTPUT") #Le port D8 est definit comme port de Sortie

def alarme_vol1():
    while True:
        try:
            grovepi.digitalWrite(buzzer,1) # Buzzer actif 
            #print ('start')
            time.sleep(0.1) # Buzzer actif pendant 0.1 seconde

            grovepi.digitalWrite(buzzer,0) # Buzzer a l'arret
            #print ('stop')
            time.sleep(0.2) # Buzzer a l'arret pendant 0.2 seconde

        except KeyboardInterrupt: #Arret de l'alarme via interruption clavier
            grovepi.digitalWrite(buzzer,0) #Arret du buzzer
            break
        except IOError:
            print ("Arret de l'alarme")

def alarme_vol2():
    while True:
        try:
            grovepi.digitalWrite(buzzer,1) # Buzzer actif 
            #print ('start')
            time.sleep(0.5) # Buzzer actif pendant 0.5 seconde

            grovepi.digitalWrite(buzzer,0) # Buzzer a l'arret
            #print ('stop')
            time.sleep(1) # Buzzer a l'arret pendant 1 seconde

        except KeyboardInterrupt: #Arret de l'alarme via interruption clavier
            grovepi.digitalWrite(buzzer,0) #Arret du buzzer
            break
        except IOError:
            print ("Arret de l'alarme")

def arret_alarme():
    grovepi.digitalWrite(buzzer,0)

#Partie LCD

bus = smbus.SMBus(1)
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e

#Initialise le lcd, pour les couleurs et pour le texte
def initialisation_ecran():
    os.system("i2cset -y 1 0x62 0x00 0x00")
    os.system("i2cset -y 1 0x62 0x01 0x00")
    os.system("i2cset -y 1 0x3e 0x80 0x01 # clear display")
    os.system("i2cset -y 1 0x3e 0x80 0x0F # display on, block cursor")
    os.system("i2cset -y 1 0x3e 0x80 0x38 # 2 lines")

#Definit une couleur de fond pour le lcd
def setRGB(rouge,vert,bleu):
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x00,0x00)
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x01,0x00)
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x02,bleu)
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x03,vert)
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x04,rouge)
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xAA)
	
def textCmd(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)

#Affiche les valeur issues du capteur de poids et du loudness sensor	
def prompt_values(poids,son):
	textCmd(0x01)
	textCmd(0x0F)
	textCmd(0x38)

        affichage_poids = "Poids: "+str(poids)+" kg\n"
        affichage_son = "Son: "+str(son)+" db"
        affichage = affichage_poids+affichage_son
        
        for carac in range(-1,len(affichage)):
            if ord(affichage[carac]) == 10 : #Si le caractere est \n
                textCmd(0xc0) #On passe a la ligne
            else:
                bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(affichage[carac]))


#---------------- CAPTEURS ENTREES -----

#Partie Loudness sensor

loudness_sensor = 0 #Le loudness sensor est connecte au port A0


#	def capte_son():
	#Capte le son de la ruche 

#	def affichage_graphe_son():
	#Le graphe est affiché sur un moniteur. Il recupère les valeurs stocké dans la base de données

#Partie Accelerometre 

#	def ruche_enMouvement():
	#Retourne un boolean, True si en mouvement false sinon.
	#Cette fonction appelle les fonctions du fichier lsm6ds3.py


#Partie capteur de poids

# 	def init_poids():
	#Initialise le capteur de poids


#	def pese_ruche():
	#Mesure le poid de la ruche


#	def affichage_graphe_poids():


#Partie base de données

#	def init_bdd:
	#Fonction pour initialiser la connection à la base de données

#	def save_son():
	#Sauvegarde les données récupérée dans la base de données

#	def save_poids():
	#Sauvegarde les données récupérée dans la base de données