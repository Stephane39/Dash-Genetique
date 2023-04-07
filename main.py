import pygame
from typing import Tuple, List
from ressources import *
from environnement import *

# Configuration de pygame
pygame.init()  # type: ignore
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))


class Joueur:
    def __init__(self, BOB_X, BOB_Y, surface):
        self.BOB_X = BOB_X
        self.BOB_Y = BOB_Y
        self.surface = surface
        self.surface_actu = surface
        self.image = BOB
        self.LARGEUR, self.HAUTEUR = self.image.get_size()
        self.G = 0.05
        self.V = 0
        self.HAUTEUR_SAUT = 35
        self.VITESSE = 2.5
        pass

    def saut(self, frame: int) -> Tuple[bool, int]:
        """
        saut() permet de faire sauter BOB en l'affichant un peu plus haut à chaque appel.
        La fonction renvoie False quand l'animation est fini.
        """
        if frame < self.HAUTEUR_SAUT:
            frame += 1
            screen.blit(FILL, (self.BOB_X, self.BOB_Y))
            self.BOB_Y -= self.VITESSE
            screen.blit(BOB, (self.BOB_X, self.BOB_Y))
            return True, frame
        else:
            return False, -1

    def gravite(self):
        """
        gravite() permet d'appliquer une effet de gravité au joueur si il se situe dans les airs
        """
        if self.BOB_Y < self.surface_actu:
            self.V += self.G
            self.BOB_Y += min(self.V, self.surface_actu-self.BOB_Y)
            pygame.event.clear()
        pass

    def isDead(self, liste_obstacle: list) -> bool:
        """
        isDead() regarde si les coordonnées actuelle de BOB rentrent en collisions avec
        un obstacle éventuel.
        """
        BOB_p1 = (self.BOB_X, self.BOB_Y)
        BOB_p2 = (self.BOB_X + self.LARGEUR, self.BOB_Y + self.HAUTEUR)
        for obstacle in liste_obstacle:
            if obstacle.is_hit(BOB_p1, BOB_p2):
                return True
        return False
    
    def actualiser_surface(self, liste_obstacles:list):
        """
        actualiser_surface() permet de gerer la hauteur de la surface afin de pouvoir sauter sur des
        éléments par exemple.
        """
        changed = False
        for obstacle in liste_obstacle:
            if (obstacle.type == "bs"):
                if (obstacle.p1[0] < self.BOB_X < obstacle.p2[0]) or (obstacle.p1[0] < self.BOB_X + self.LARGEUR < obstacle.p2[0]):
                    self.surface_actu = min(self.surface_actu, obstacle.p1[1]-self.HAUTEUR)
                    changed = True
        if not changed:
            self.surface_actu = self.surface
        pass

# Création d'une liste d'obstacle

liste_obstacle = []
liste_obstacle.append(Obstacle(PIQUE, [1000, 250], [1050, 300], "p"))
liste_obstacle.append(Obstacle(PIQUE_REVERSE, [1000, 100], [1050, 150], "p"))
liste_obstacle.append(Obstacle(BLOC, [1000, 50], [1050, 100], "b")) 
liste_obstacle.append(Obstacle(BLOC, [1450, 250], [1500, 300], "bs"))
liste_obstacle.append(Obstacle(BLOC, [1500, 250], [1550, 300], "bs"))
liste_obstacle.append(Obstacle(BLOC, [1550, 250], [1600, 300], "bs"))
liste_obstacle.append(Obstacle(BLOC, [1750, 200], [1800, 250], "bs"))
"""
liste_obstacle.append( Obstacle( BLOC , [1000, 0], [1050, 50], "b" ) )
liste_obstacle.append( Obstacle( PIQUE ,[1280, 250], [1330, 300], "p" ) )
liste_obstacle.append( Obstacle( BLOC , [1450, 50], [1500, 100], "b" ) )
liste_obstacle.append( Obstacle( BLOC , [1450, 100], [1500, 150], "b" ) )
liste_obstacle.append( Obstacle( BLOC , [1450, 150], [1500, 200], "b" ) )
liste_obstacle.append( Obstacle( BLOC , [1450, 200], [1500, 250], "b" ) )
liste_obstacle.append( Obstacle( PIQUE , [1620, 250], [1670, 300], "p" ) )
liste_obstacle.append( Obstacle( PIQUE , [1650, 250], [1700, 300], "p" ) )
liste_obstacle.append( Obstacle( BLOC , [1750, 250], [1800, 300], "b" ) )
liste_obstacle.append( Obstacle( BLOC , [2050, 250], [2100, 300], "b" ) )
"""
LVL1 = Level(screen, *liste_obstacle)


def main():
    """
    Fonction principale qui tourne tant que le jeu n'est pas fini
    """
    Bob = Joueur(LARGEUR//2-25, HAUTEUR_SOL - BOB_HAUTEUR,
                 HAUTEUR_SOL-BOB_HAUTEUR)  # Création du joueur (Bob)
    Bob_position = (Bob.BOB_X, Bob.BOB_Y)
    running = True
    SAUT = False
    screen.blit(FOND, (0, 0))
    screen.blit(BOB, (Bob.BOB_X, Bob.BOB_Y))
    frame = 0
    clock = pygame.time.Clock()
    pygame.display.flip()
    while running:

        screen.blit(FOND, (0, 0))
        Bob_position = (Bob.BOB_X, Bob.BOB_Y)

        # GRAVITE
        if not SAUT:
            Bob.gravite()
            Bob_position = (Bob.BOB_X, Bob.BOB_Y)
            screen.blit(BOB, Bob_position)

        # DEFILEMENT
        LVL1.defilement_obstacle()
        LVL1.defilement_sol()
        # VERIFICATION HITBOX
        running = not Bob.isDead(liste_obstacle)

        # SAUT
        if SAUT:
            SAUT, frame = Bob.saut(frame)
            pygame.event.clear()
        Bob.actualiser_surface(liste_obstacle)

        # Lecture des events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # type: ignore
                running = False
            elif event.type == pygame.KEYDOWN:  # type: ignore
                SAUT, frame, Bob.V = True, 0, 0

        # Affichage de la distance parcouru
        pygame.display.flip()
        clock.tick(160)
    pygame.quit()  # type: ignore


main()
