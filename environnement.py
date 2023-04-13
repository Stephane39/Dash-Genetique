from pygame import Surface
from typing import List, Tuple
from ressources import *
from random import choice


class Obstacle:
    """
    pour les types:
        p = pique
        bs = bloc surface
    """

    def __init__(self, IMAGE, p1: List[float], p2: List[float], type: str):
        self.IMAGE = IMAGE
        self.p1 = p1
        self.p2 = p2
        self.type = type
        pass
    
    def clone(self):
        return Obstacle(self.IMAGE, self.p1.copy(), self.p2.copy(), self.type)

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

    def __str__(self):
        return f"{self.type} {self.p1}, {self.p2}"

    def __repr__(self):
        return str(self)


class Joueur:

    def __init__(self, BOB_X: float, BOB_Y: float, surface: float):
        self.BOB_X = BOB_X
        self.BOB_Y = BOB_Y
        self.surface = surface
        self.surface_actu = surface
        self.image = choice(BOB_PICS)
        self.LARGEUR, self.HAUTEUR = self.image.get_size()
        self.G = 0.05
        self.V = 0
        self.HAUTEUR_SAUT = 35
        self.VITESSE = 2.5
        self.est_en_train_de_sauter = False
        self.frame = 0
        self.alive = True

    @classmethod
    def nouveau(cls):
        return Joueur(LARGEUR//2-25, HAUTEUR_SOL - BOB_HAUTEUR,
                      HAUTEUR_SOL-BOB_HAUTEUR)

    def saut(self, frame: int) -> Tuple[bool, int]:
        """
        saut() permet de faire sauter BOB en l'affichant un peu plus haut à chaque appel.
        La fonction renvoie False quand l'animation est fini.
        """
        if frame < self.HAUTEUR_SAUT:
            frame += 1
            self.BOB_Y -= self.VITESSE
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

    def actualiser_surface(self, liste_obstacle: List[Obstacle]):
        """
        actualiser_surface() permet de gerer la hauteur de la surface afin de pouvoir sauter sur des
        éléments par exemple.
        """
        changed = False
        for obstacle in liste_obstacle:
            if (obstacle.type == "bs") and (self.BOB_Y + self.HAUTEUR <= obstacle.p1[1]):
                if (obstacle.p1[0] <= self.BOB_X <= obstacle.p2[0]) or (obstacle.p1[0] <= self.BOB_X + self.LARGEUR <= obstacle.p2[0]):
                    self.surface_actu = min(
                        self.surface_actu, obstacle.p1[1]-self.HAUTEUR)
                    changed = True
        if not changed:
            self.surface_actu = self.surface
        pass

    def __bool__(self):
        return self.alive
