#Main du projet faso, protection et statistiques de ruches
#On importe ruche.py, notre bibliotheque specifique a notre systeme

import ruche, time, grovepi, math
from datetime import datetime, timedelta

#Initialisation des variables globales
print("Intialisation du systeme ...")
time.sleep(5)
hivesystems_secure = True
hivesystems_alarm = False
lsm = ruche.LSM6DS3()
loudness_sensor = 0
soundValues = list()
#Initialisation de l'ecran
ruche.initialisation_ecran()
ruche.setRGB(0,255,0)

#poids = ruche.pese_ruche()
poids = 45
son = ruche.capte_son()
date_reference_Poids = datetime.now() + timedelta(days=1)
minute_reference_son = datetime.now() + timedelta(minutes=1)

ruche.prompt_values(poids,son)

#Debut du programme principal
print("------------ HIVE SYSTEMS ------------")

while True:

    while hivesystems_secure:
        
        print("Securisation de la ruche activee")
        
        date_actuelle = datetime.now() #On recupere la date actuelle, heure, minutes et secondes

        #On recupere les donnees de son
        #De poids

        minute_actuelle = date_actuelle.minute
        #print("minute_actuelle : "+str(minute_actuelle))
        #print("minute_reference_son : "+str(minute_reference_son.minute))
        if minute_reference_son.minute == minute_actuelle: # Toutes les 10 minutes on verifie si on peut mesurer l'intensite sonore de la ruche
            son = ruche.capte_son()
            soundValues.append(son)
            minute_reference_son = minute_reference_son + timedelta(minutes=1)

        if len(soundValues)==6: #Au bout de 6 valeurs recoltees on peut faire une moyenne et envoyer cela à la dashboard( au google sheet dans un premier temps)
            val_db_heure = ruche.calcule_dB_heure(soundValues)
            soundValues = list() #On remet a zero la liste de valeurs
            ruche.send_son(val_db_heure)

        print(soundValues)

        """jour_actuel = date_actuelle.day
        if jour_actuel == date_reference_Poids.day #Nous verifions si le jour de notre date de reference et le jour de notre date actuelle correspondent.
            poids = ruche.pese_ruche()                  #Si les jours correspondent alors on pese la ruche
            date_reference_Poids = date_reference_Poids + timedelta(days=1) #On change notre date de reference en ajoutant 1 jour, afin que la ruche soit pese demain en debut de journee (minuit)
        """  

        if lsm.ruche_enMouvement(): #Verifie si la ruche est en mouvement
            print("La ruche bouge !")
            print("Envoi d'un message")
            ruche.send_alert() # Envoi d'une notification via PushBullet

            hivesystems_secure = False
            hivesystems_alarm = True
            print("Fin de secure, activation de l'alarme ...")

        #Affichage des valeurs sur l'ecran LCD
        ruche.prompt_values(poids,son)

    while hivesystems_alarm:

        #Activation du buzzer

        #Si la ruche redevient stable:
        #   hivesystems_secure = True
        #   hivesystems_alarm = False
        #   Arret du buzzer
        print("Alarme activee")
        ruche.alarme_vol2()
        #time.sleep(20) #On active l'alarme pendant 20 secondes !
        if not lsm.ruche_enMouvement():
            hivesystems_secure = True
            hivesystems_alarm = False
            ruche.arret_alarme()
            print("Fin de l'alarme, basculement vers le secure...")
            #time.sleep(10)
            #Faut-il retablir date_reference_poids et minute_reference_son ? Au cas ou l'interruption dure plus d'une minute ou plus d'un jour, on perdrait notre repere et le system ne recupererai plus de donnees
