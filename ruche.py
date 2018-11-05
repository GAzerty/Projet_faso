#Bibliotheque du projet ruche

#IMPORT
import grovepi
import smbus, time, os


#---------------- CAPTEURS SORTIES -----
#Partie Buzzer

#	def init_buzzer():
	#Initialise le buzzer

#	def alarme_1():

#	def alarme_2():

#	def stop_buzzer():

#Partie LCD

#	def init_lcd():
	#Initialise le lcd

#	def textCmd():

#	def affichage_valeurs(poids,son):



#---------------- CAPTEURS ENTREES -----

#Partie Loudness sensor

#	def init_son():
	#Initialise le capteur de son


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