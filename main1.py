import pygame
from typing import Tuple, List
from ressources import *
#Configuration de pygame
pygame.init() # type: ignore

screen = pygame.display.set_mode((LARGEUR, HAUTEUR))

#Configuration des variables pour le défilement du sol
SOL1_pos = 0
SOL2_pos = LARGEUR
SPEED = 2.5
DISTANCE = 0

#Configuration des variables liée à la gravité de BOB.
G = 0.05
V = 0
isGravite = False
HAUTEUR_SAUT = 35

class Obstacle:
    """
    pour les types:
        p = pique
        b = bloc
        bs = bloc surface
    """
    def __init__(self, IMAGE, p1:List[float], p2:List[float], type:str):
        self.IMAGE = IMAGE
        self.p1 = p1
        self.p2 = p2
        self.type = type

    def is_hit(self, xy1:List[float], xy2:List[float])->bool:
        """
        Detecte si la valeur passé en paramètre rentre en collision avec l'objet
        """
        if ((self.p2[0] >= xy1[0] >= self.p1[0]) or (self.p2[0] >= xy2[0] >= self.p1[0])):
            if (self.p2[1] > xy1[1] >= self.p1[1]) or (self.p2[1] >= xy2[1] >= self.p1[1]):
                return True
        return False
    
    def defilement(self):
        self.p1[0] -= SPEED
        self.p2[0] -= SPEED
        pass

class Level:

    def __init__(self, *obstacles: Obstacle):
        self.obstacles = list(sorted(obstacles, key=lambda ob: ob.p1))
        self.current = 0

    def defilement_obstacle(self):
        """
        Cette fonction permet de faire défiler les obstacles, si les obstacles sont déjà passé
        alors on les retire de la liste liste_obstacle pour éviter de faire des calculs inutiles
        """
        for i in range(self.current, len(self.obstacles)):
            obstacle = self.obstacles[i]
            x, y = obstacle.p1
            if obstacle.p2[0] < 0:
                self.current = i
            else:
                screen.blit(FILL, (x, y))
                obstacle.defilement()
                x, y = obstacle.p1
                screen.blit(obstacle.IMAGE, (x, y))

#Création d'une liste d'obstacle

liste_obstacle = []
liste_obstacle.append( Obstacle( PIQUE , [1000, 250], [1050, 300], "p" ) )
liste_obstacle.append( Obstacle( PIQUE_REVERSE , [1000, 100], [1050, 150], "p" ) )
liste_obstacle.append( Obstacle( BLOC , [1000, 50], [1050, 100], "b" ) )
liste_obstacle.append( Obstacle( BLOC , [1000, 0], [1050, 50], "b" ) )
liste_obstacle.append( Obstacle( PIQUE ,[1280, 250], [1330, 300], "p" ) )
liste_obstacle.append( Obstacle( BLOC , [1450, 0], [1500, 50], "b" ) )
liste_obstacle.append( Obstacle( BLOC , [1450, 50], [1500, 100], "b" ) )
liste_obstacle.append( Obstacle( BLOC , [1450, 100], [1500, 150], "b" ) )
liste_obstacle.append( Obstacle( BLOC , [1450, 150], [1500, 200], "b" ) )
liste_obstacle.append( Obstacle( BLOC , [1450, 200], [1500, 250], "b" ) )
liste_obstacle.append( Obstacle( PIQUE , [1620, 250], [1670, 300], "p" ) )
liste_obstacle.append( Obstacle( PIQUE , [1650, 250], [1700, 300], "p" ) )
liste_obstacle.append( Obstacle( BLOC , [1750, 250], [1800, 300], "b" ) )
liste_obstacle.append( Obstacle( BLOC , [2050, 250], [2100, 300], "b" ) )
LVL1 = Level(*liste_obstacle)

def defilement_sol():
    """
    La fonction décale le sol à chaque appel, cela permet de donner l'impression que le sol recule, donc
    que le joueur avance
    """
    global SOL1_pos, SOL2_pos, SPEED, DISTANCE
    DISTANCE+=1
    if SOL1_pos <= -LARGEUR:
        SOL1_pos = LARGEUR
    if SOL2_pos <= -LARGEUR:
        SOL2_pos = LARGEUR
    SOL1_pos-=SPEED
    SOL2_pos-=SPEED
    screen.blit(SOL, (SOL1_pos, HAUTEUR_SOL))
    screen.blit(SOL, (SOL2_pos, HAUTEUR_SOL))
    pass


def saut(frame:int)->Tuple[bool, int]:
    """
    saut() permet de faire sauter BOB en l'affichant un peu plus haut à chaque appel.
    La fonction renvoie False quand l'animation est fini.
    """
    global BOB_Y
    if frame < HAUTEUR_SAUT:
        frame+=1
        screen.blit(FILL, (BOB_X, BOB_Y))
        BOB_Y-=SPEED
        screen.blit(BOB, (BOB_X, BOB_Y))
        return True, frame
    else:
        return False, -1

def gravite(surface):
    global V, BOB_Y
    if BOB_Y < surface:
        V+=G
        BOB_Y+=min(V, surface-BOB_Y)
    pass

def isDead(BOB_p1:tuple, BOB_p2:tuple, liste_obstacle:list)->bool:
    """
    Fonction qui regarde si les coordonnées actuelle de BOB rentrent en collisions avec
    un obstacle éventuel
    """
    for obstacle in liste_obstacle:
        if obstacle.is_hit(BOB_p1, BOB_p2):
            return True
    return False

def show_distance():
    """
    Fonction qui permet d'afficher la distance du joueur en haut à gauche de la fenêtre
    """
    toshow = font.render(str(DISTANCE//2000), True, white, purple)
    screen.blit(toshow, (LABEL_X, LABEL_Y))
    pass

def main():
    """
    Fonction principale qui tourne tant que le jeu n'est pas fini
    """
    global BOB_Y, V, SPEED
    running = True
    SAUT = False
    surface = HAUTEUR_SOL-BOB_HAUTEUR
    screen.blit(FOND, (0, 0))
    screen.blit(BOB, (BOB_X, BOB_Y))
    frame = 0
    clock = pygame.time.Clock()
    pygame.display.flip()
    while running:

        BOB_POSITION = (BOB_X, BOB_Y)
        screen.blit(FILL, BOB_POSITION)

        #GRAVITE
        if not SAUT:
            gravite(surface)
            BOB_POSITION = (BOB_X, BOB_Y)
            screen.blit(BOB, BOB_POSITION)

        #DEFILEMENT
        LVL1.defilement_obstacle()
        defilement_sol()
        #VERIFICATION HITBOX

        BOB_p1 = BOB_POSITION
        BOB_p2 = ( BOB_POSITION[0]+BOB_LARGEUR, BOB_POSITION[1]+BOB_HAUTEUR )
        running = not isDead(BOB_p1, BOB_p2, liste_obstacle)

        #SAUT
        if SAUT:
            SAUT, frame = saut(frame)
            pygame.event.clear()

        #Lecture des events
        if BOB_Y != surface:
            pygame.event.clear()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # type: ignore
                    running = False
                elif event.type == pygame.KEYDOWN: # type: ignore
                    SAUT, frame, V, isGravite = True, 0, 0, True

        #Affichage de la distance parcouru
        show_distance()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit() # type: ignore
    
main()




