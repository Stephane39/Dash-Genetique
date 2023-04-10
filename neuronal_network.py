from typing import List
from abc import abstractmethod
from random import randint, choice
from ressources import LARGEUR, HAUTEUR
from copy import copy
from environnement import *


class Neurone:

    @abstractmethod
    def evaluer(self, obstacles: List[Obstacle], coos_bob: List[float]) -> bool:
        """
        Cette méthode permet de vérifier si le neurone est activé.
        """
        pass

    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass


class PorteLogique(Neurone):

    def __init__(self, operateur: bool, negatif: bool, enfants: List[Neurone]) -> None:
        self.operateur = operateur
        self.enfants = enfants
        self.negatif = negatif

    def evaluer(self, obstacles, coos_bob) -> bool:
        ou = False
        et = True
        for e in self.enfants:
            b = e.evaluer(obstacles, coos_bob)
            et = et and b
            ou = ou or b
        if self.negatif:
            et = not et
            ou = not ou
        if self.operateur:
            return et
        else:
            return ou

    def copy(self):
        enfants = list(map(lambda n: n.copy(), self.enfants))
        P = PorteLogique(self.operateur, self.negatif, enfants)
        return P

    @classmethod
    def nouveau(cls):
        return PorteLogique(bool(randint(0, 1)), bool(randint(0, 1)), [])

    def __str__(self):
        return f"PL({'et' * self.operateur + 'ou' * (1-self.operateur)}, {''.join(map(str, self.enfants))})"

    def __repr__(self):
        return f"PL({'et' if self.operateur else 'ou'},{'non' if self.negatif else 'oui'},{str(self.enfants)})"


class DetecteurObstacle(Neurone):
    """
    detecte un bloc et un attribut
    """
    types_obstacles = ["bs", "p"]

    def __init__(self, coordonees: List[float], bloc_type: str) -> None:
        self.coordonees = coordonees
        self.bloc_type = bloc_type

    def evaluer(self, obstacles, coos_bob) -> bool:
        x = coos_bob[0] + self.coordonees[0]
        y = coos_bob[1] + self.coordonees[1]
        for obstacle in obstacles:
            if (obstacle.type == self.bloc_type):
                if (obstacle.p2[0] > x > obstacle.p1[0]) and (obstacle.p2[1] > y > obstacle.p1[1]):
                    return True
        return False

    def random_type(self):
        return choice(self.types_obstacles)

    @classmethod
    def nouveau(cls):
        """
        Créer un nouveau neurone detecteur d'obstacle random
        """
        coos: List[float] = [
            randint(0, LARGEUR//2), randint(-HAUTEUR_SOL, HAUTEUR_SOL)]
        bloc_type = choice(cls.types_obstacles)
        return DetecteurObstacle(coos, bloc_type)

    def passer_en_porte_logique(self):
        """
        Créer une porte logique de manière aléatoire
        """
        e = self.copy()
        operateur = bool(randint(0, 1))
        negatif = bool(randint(0, 1))
        return PorteLogique(operateur, negatif, [e])

    def copy(self):
        D = DetecteurObstacle(
            [self.coordonees[0], self.coordonees[1]], copy(self.bloc_type))
        return D

    def __str__(self):
        return f"DO({self.bloc_type}, {self.coordonees})"

    def __repr__(self):
        return self.__str__()


class IA:

    def __init__(self):
        self.reseau: Neurone = DetecteurObstacle.nouveau()
        self.joueur = Joueur.nouveau()
        self.score = 0

    @classmethod
    def muter(cls, neurone: Neurone):
        """
        DetecteurObstacle:
            peut changer les coordonnées (1 chance sur 2)
            peut changer le type de bloc (1 chance sur 10)
            peut se muter en porte logique (1 chance sur 4)
        PorteLogique:
            peut changer le type booleen
            peut changer le negatif
            peut créer un nouveau neurone
            peut muter ses enfants
        """
        if isinstance(neurone, DetecteurObstacle):
            if randint(0, 1):
                # Changement des coordonnées
                decalage_X = randint(-10, 10)
                decalage_Y = randint(-10, 10)
                neurone.coordonees[0] = min(
                    neurone.coordonees[0] + decalage_X, LARGEUR)
                neurone.coordonees[1] = min(
                    neurone.coordonees[1] + decalage_Y, HAUTEUR)

            if randint(1, 10) == 10:
                # Changement du type de bloc
                neurone.bloc_type = "p" if neurone.bloc_type == "bs" else "bs"

            if randint(1, 2) == 2:
                # Mutation en porte logique
                neurone = neurone.passer_en_porte_logique()

        elif isinstance(neurone, PorteLogique):
            if randint(1, 5) == 5:
                # Changement du type booléen
                neurone.operateur = not neurone.operateur

            if randint(1, 10) == 10:
                # Changement du négatif
                neurone.negatif = not neurone.negatif

            if randint(1, 4) == 4:
                # Creation d'une neurone
                if not randint(0, 2):
                    neurone.enfants.append(PorteLogique.nouveau())
                else:
                    neurone.enfants.append(DetecteurObstacle.nouveau())

            if randint(0, 1):
                # Mutation des enfants
                for enfant in neurone.enfants:
                    if randint(0, 1):
                        cls.muter(enfant)
        return neurone

    def reset(self):
        self.joueur = Joueur.nouveau()
        self.score = 0

    def copy(self):
        I = IA()
        I.reseau = self.reseau.copy()
        return I

    def __bool__(self):
        return bool(self.joueur)
