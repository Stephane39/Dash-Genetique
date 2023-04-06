import pygame

pygame.font.init()
BOB = pygame.image.load('ressources/bob.png')
FOND = pygame.image.load('ressources/fond.png')
SOL = pygame.image.load('ressources/sol.png')
FILL = pygame.image.load('ressources/fill.png')
PIQUE = pygame.image.load('ressources/pique.png')
BLOC = pygame.image.load('ressources/bloc.png')
PIQUE_REVERSE = pygame.transform.rotate(PIQUE, 180)
LARGEUR, HAUTEUR = FOND.get_size()
HAUTEUR_SOL = HAUTEUR-(SOL.get_size()[1])
BOB_LARGEUR, BOB_HAUTEUR = BOB.get_size()
BOB_X, BOB_Y = LARGEUR//2-25, HAUTEUR_SOL - BOB_HAUTEUR
white = (255, 255, 255)
purple = (162, 72, 164)
font = pygame.font.Font('freesansbold.ttf', 32)
LABEL_X = 15
LABEL_Y = 15