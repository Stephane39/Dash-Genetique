import pygame
from ressources import *
from level import *
from entraineur import EntraineurIA
from functools import partial
# Configuration de pygame
pygame.init()  # type: ignore
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))


# Création d'une liste d'obstacle

def play():
    """
    La fonction play permet de créer le niveau et le joueur puis appelle la fonction main()
    pour lancer le jeu.
    """
    # Création du niveau (LVL1)
    E = EntraineurIA(Level.level_2, 10)
    E.commencer()
    pass


play()
