from pygame import Surface
from typing import List
from ressources import*

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
        if (self.p2[0] >= xy1[0] >= self.p1[0]) or (self.p2[0] >= xy2[0] >= self.p1[0]):
            if (self.p2[1] > xy1[1] > self.p1[1]) or (self.p2[1] >= xy2[1] > self.p1[1]):
                return True
        return False

    def defilement(self, speed: float):
        self.p1[0] -= speed
        self.p2[0] -= speed
        pass

class Level:

    def __init__(self, screen:Surface, *obstacles: Obstacle):
        self.screen = screen
        self.obstacles = list(sorted(obstacles, key=lambda ob: ob.p1))
        self.current = 0
        # Configuration des variables pour le défilement du sol 
        self.sol1_pos = 0
        self.sol2_pos = LARGEUR
        self.SPEED = 2.5
        self.DISTANCE = 0

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
                self.screen.blit(FILL, (x, y))
                obstacle.defilement(self.SPEED)
                x, y = obstacle.p1
                self.screen.blit(obstacle.IMAGE, (x, y))
        pass

    def defilement_sol(self):
        """
        La fonction décale le sol à chaque appel, cela permet de donner l'impression que le sol recule, donc
        que le joueur avance
        """
        self.DISTANCE += 1
        if self.sol1_pos <= -LARGEUR:
            self.sol1_pos = LARGEUR
        if self.sol2_pos <= -LARGEUR:
            self.sol2_pos = LARGEUR
        self.sol1_pos -= self.SPEED
        self.sol2_pos -= self.SPEED
        self.screen.blit(SOL, (self.sol1_pos, HAUTEUR_SOL))
        self.screen.blit(SOL, (self.sol2_pos, HAUTEUR_SOL))
        pass