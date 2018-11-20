#Bibliotheque du projet ruche

#IMPORT
import grovepi
import time
import sys, math
import os
import smbus
import GPIO
import I2C
import requests

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
	#Le graphe est affiche sur un moniteur. Il recupere les valeurs stocke dans la base de donnees

#Partie Accelerometre 

address = 0x6a #On renseigne l'adresse de l'accelerometre que l'on recupere avec la commande i2cdetect -y -1

class LSM6DS3:
    i2c = None
    tempvar = 0
    global accel_center_x
    accel_center_x = 0
    global accel_center_y
    accel_center_y = 0
    global accel_center_z
    accel_center_z = 0

    
    def __init__(self, address=0x6a, debug=0, pause=0.8):
        self.i2c = I2C.get_i2c_device(address)
        self.address = address
        dataToWrite = 0 #Start Fresh!
        dataToWrite |= 0x03 # set at 50hz, bandwidth
        dataToWrite |= 0x00  # 2g accel range
        dataToWrite |= 0x10 # 13hz ODR
        self.i2c.write8(0X10, dataToWrite) #writeRegister(LSM6DS3_ACC_GYRO_CTRL2_G, dataToWrite);
        
        accel_center_x = self.i2c.readS16(0X28)
        accel_center_y = self.i2c.readS16(0x2A)
        accel_center_z = self.i2c.readS16(0x2C)
    
    def readRawAccelX(self):
    	output = self.i2c.readS16(0X28)
    	return output;
    
    def readRawAccelY(self):
    	output = self.i2c.readS16(0x2A)
    	return output;
    
    def readRawAccelZ(self):
    	output = self.i2c.readS16(0x2C)
    	return output;
    	
    def calcAnglesXY(self):
		#Using x y and z from accelerometer, calculate x and y angles
		x_val = 0
		y_val = 0
		z_val = 0
		result = 0
		
		x2 = 0
		y2 = 0
		z2 = 0
		x_val = self.readRawAccelX() - accel_center_x
		y_val = self.readRawAccelY() - accel_center_y
		z_val = self.readRawAccelZ() - accel_center_z
		
		x2 = x_val*x_val
		y2 = y_val*y_val
		z2 = z_val*z_val
		
		result = math.sqrt(y2+z2)
		if (result != 0):
			result = x_val/result
		accel_angle_x = math.atan(result)
		return accel_angle_x;



    def readRawGyroX(self):
        output = self.i2c.readS16(0X22)
        return output;

    def readFloatGyroX(self):
        output = self.calcGyro(self.readRawGyroX())
        return output;

    def calcGyroXAngle(self):
        temp = 0
        temp += self.readFloatGyroX()
        if (temp > 3 or temp < 0):
            self.tempvar += temp
        return self.tempvar;

    def calcGyro(self, rawInput):
        gyroRangeDivisor = 245 / 125; #500 is the gyro range (DPS)
        output = rawInput * 4.375 * (gyroRangeDivisor) / 1000;
        return output;

#def ruche_enMouvement():
	#Retourne un boolean, True si en mouvement false sinon.
	#Cette fonction ne fait pas partie de la classe lsm6ds3


#Partie capteur de poids

# 	def init_poids():
	#Initialise le capteur de poids


#	def pese_ruche():
	#Mesure le poid de la ruche


#	def affichage_graphe_poids():


#Partie push bullet:

	def send_alert(): 
	os.system("""curl -u <user_token>: https://api.pushbullet.com/v2/pushes -d type=note -d title="Alerte! Ruche en mouvement" """)

	
#Partie envoie de données sur google sheet:
        #cette fonction envoie la valeur val_db dans le google sheet
	def send_son(val_db):
            requests.post("https://docs.google.com/forms/d/**id_form***/formResponse",{"entry.1417047577":val_db,verify=False)


#	def send_poids():
	#Sauvegarde les donnees recuperee dans le google sheet
