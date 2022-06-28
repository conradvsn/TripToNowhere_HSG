#-------------------------------------------------------------------------------
# Name : Trip to NOWHERE
#
# Author : Conrad and ARIS
#
# Created : 15/04/11
#
#Copyright : (c) Conrad and ARIS
#-------------------------------------------------------------------------------

TITRE = "TRIP TO NOWHERE"
WIDTH = 480
HEIGHT = 600
#Combien de fois par seconde l'ecran est update
FPS = 70
#Proptiétés du joueur
JOUEUR_ACC = 0.5
JOUEUR_FROTTEMENTS = -0.10
JOUEUR_GRAVITE = 0.8
JOUEUR_SAUT = 20
POLICE = 'times'
MS_FICHIER = "meilleurscore.txt"
SON_SAUT = 'jetpack.wav'
SON_BOOST = 'cartoon-boing-sound-effect.wav'
SPRITESHEET = "megaman2.png"
BACKGROUND = "back.jpg"
BOOST_POWER = 60
POW_SPAWN_PCT = 10
MOB_FREQ = 5000
JOUEUR_COUCHE = 2
PLATEFORME_COUCHE = 1
POWER_COUCHE = 2
MOB_COUCHE = 2
Plateforme_liste = [(0, HEIGHT -60),
                    (WIDTH / 2 -50, HEIGHT *3/4 - 50 ),
                    (125, HEIGHT -350),
                    (350, 200),
                    (175, 100)]
# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
VIOLET = (255, 0,255)
BGCOLOR = (51, 153, 255)
