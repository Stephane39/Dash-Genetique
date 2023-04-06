import pygame
from typing import Tuple, List
from ressources import *

# Configuration de pygame
pygame.init()  # type: ignore
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))

# Configuration des variables pour le défilement du sol
SOL1_pos = 0
SOL2_pos = LARGEUR
SPEED = 2.5
DISTANCE = 0


class Joueur:
    def __init__(self, BOB_X, BOB_Y, surface):
        self.BOB_X = BOB_X
        self.BOB_Y = BOB_Y
        self.surface = surface
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
        if self.BOB_Y < self.surface:
            self.V += self.G
            self.BOB_Y += min(self.V, self.surface-self.BOB_Y)
        pass

    def isDead(self, liste_obstacle: list) -> bool:
        """
        isDead() regarde si les coordonnées actuelle de BOB rentrent en collisions avec
        un obstacle éventuel
        """
        BOB_p1 = (self.BOB_X, self.BOB_Y)
        BOB_p2 = (self.BOB_X + self.LARGEUR, self.BOB_Y + self.HAUTEUR)
        for obstacle in liste_obstacle:
            if obstacle.is_hit(BOB_p1, BOB_p2):
                return True
        return False


class Obstacle:
    """
    pour les types:
        p = pique
        b = bloc
        bs = bloc surface
    """

    def __init__(self, IMAGE, p1: List[float], p2: List[float], type: str):
        self.IMAGE = IMAGE
        self.p1 = p1
        self.p2 = p2
        self.type = type
        pass

    def is_hit(self, xy1: List[float], xy2: List[float]) -> bool:
        """
        Detecte si la valeur passé en paramètre rentre en collision avec l'objet
        """
        if ((self.p2[0] >= xy1[0] >= self.p1[0]) or (self.p2[0] >= xy2[0] >= self.p1[0])):
            if (self.p2[1] > xy1[1] >= self.p1[1]) or (self.p2[1] >= xy2[1] >= self.p1[1]):
                return True
        return False

    def defilement(self, speed: float):
        self.p1[0] -= speed
        self.p2[0] -= speed
        pass


class Level:

    def __init__(self, speed: float, *obstacles: Obstacle):
        self.speed = speed
        print(self.speed)
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
                obstacle.defilement(self.speed)
                x, y = obstacle.p1
                screen.blit(obstacle.IMAGE, (x, y))

    def defilement_sol(self):
        """
        La fonction décale le sol à chaque appel, cela permet de donner l'impression que le sol recule, donc
        que le joueur avance
        """
        global SOL1_pos, SOL2_pos, SPEED, DISTANCE
        DISTANCE += 1
        if SOL1_pos <= -LARGEUR:
            SOL1_pos = LARGEUR
        if SOL2_pos <= -LARGEUR:
            SOL2_pos = LARGEUR
        SOL1_pos -= SPEED
        SOL2_pos -= SPEED
        screen.blit(SOL, (SOL1_pos, HAUTEUR_SOL))
        screen.blit(SOL, (SOL2_pos, HAUTEUR_SOL))

# Création d'une liste d'obstacle


liste_obstacle = []
liste_obstacle.append(Obstacle(PIQUE, [1000, 250], [1050, 300], "p"))
liste_obstacle.append(Obstacle(PIQUE_REVERSE, [1000, 100], [1050, 150], "p"))
liste_obstacle.append(Obstacle(BLOC, [1000, 50], [1050, 100], "b"))
liste_obstacle.append(Obstacle(BLOC, [1450, 250], [1500, 300], "b"))
liste_obstacle.append(Obstacle(BLOC, [1500, 250], [1550, 300], "b"))
liste_obstacle.append(Obstacle(BLOC, [1550, 250], [1600, 300], "b"))
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
LVL1 = Level(SPEED, *liste_obstacle)


def main():
    """
    Fonction principale qui tourne tant que le jeu n'est pas fini
    """
    Bob = Joueur(LARGEUR//2-25, HAUTEUR_SOL - BOB_HAUTEUR,
                 HAUTEUR_SOL-BOB_HAUTEUR)  # Création du joueur (Bob)
    Bob_position = (Bob.BOB_X, BOB_Y)
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

        # Lecture des events
        if Bob.BOB_Y != Bob.surface:
            pygame.event.clear()
        else:
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
