#Main du projet faso, protection et statistiques de ruches
#On importe ruche.py, notre bibliotheque specifique a notre systeme

import ruche, time, grovepi, math

#Initialisation des variables globales
hivesystems_secure = True
hivesystems_alarm = False
lsm = ruche.LSM6DS3()
loudness_sensor = 0
soundValues = []

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
        #   On trie par ordre croissant et on enleve les plus grosses valeurs
        # La capture sonore n'est pas effice lorsqu'il y a des variantion importantes en peu de temps
        #   Cependant, elle resitue des donnees coherentes lorsque que le son est relativement constant avec des variantions lentes comme c'est le cas dans une ruche
        sensor_value = grovepi.analogRead(loudness_sensor)
        if sensor_value <= 0:
            sensor_value = 0.004875
            #ref_SPL + 20 * log10(db_current / sensitivity));
        db = (94 + (20 * math.log10(sensor_value/3.16)))
        db = db / 2
        soundValues.append(db)

        if len(soundValues) == 10:
            soundValues = sorted(soundValues)
            soundValues = soundValues[:-5] #On enleve les 7 plus grosses valeurs
            sum = 0
            for i in soundValues:
                sum = sum + i
            db_avg = sum / len(soundValues)
            ruche.prompt_values(53, round(db_avg,0))
            soundValues = [] #Reinitialisation de la liste

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
        ruche.alarme_vol2()
        #time.sleep(20) #On active l'alarme pendant 20 secondes !
        if not lsm.ruche_enMouvement():
            hivesystems_secure = True
            hivesystems_alarm = False
            ruche.arret_alarme()
            print("Fin de l'alarme, basculement vers le secure...")
            #time.sleep(10)