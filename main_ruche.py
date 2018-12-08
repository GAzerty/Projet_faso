#Main du projet faso, protection et statistiques de ruches
#On importe ruche.py, notre bibliotheque specifique a notre systeme

import ruche, time

#Initialisation des variables globales
hivesystems_secure = True
hivesystems_alarm = False
lsm = ruche.LSM6DS3()

#Initialisation de l'ecran
ruche.initialisation_ecran()
ruche.setRGB(0,255,0)
ruche.prompt_values(53,30)

#Debut du programme principal
print("------------ HIVE SYSTEMS ------------")

while True:

    while hivesystems_secure:
        print("Securisation de la ruche activee")
        #On recupere les donnees de son
        #De poids

        #On fait la moyenne des donnees de son au bout de 20 valeurs
        #   On envoie ses valeurs


        if lsm.ruche_enMouvement(): #Verifie si la ruche est en mouvement
            print("La ruche bouge !")
            print("Envoi d'un message")
            ruche.send_alert() # Envoi d'une notification via PushBullet

            hivesystems_secure = False
            hivesystems_alarm = True
            print("Fin de secure, activation de l'alarme ...")


    while hivesystems_alarm:

        #Activation du buzzer

        #Si la ruche redevient stable:
        #   hivesystems_secure = True
        #   hivesystems_alarm = False
        #   Arret du buzzer
        print("Alarme activee")
        ruche.allume_alarme()
        time.sleep(20) #On active l'alarme pendant 20 secondes !
        if not lsm.ruche_enMouvement():
            hivesystems_secure = True
            hivesystems_alarm = False
            ruche.arret_alarme()
            print("Fin de l'alarme, basculement vers le secure...")
            time.sleep(10)