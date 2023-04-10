from typing import List
from abc import abstractmethod
from random import randint, choice
from ressources import LARGEUR, HAUTEUR
from copy import deepcopy
from environnement import *


class Neurone:

    @abstractmethod
    def evaluer(self, obstacles: List[Obstacle]) -> bool:
        """
        Cette méthode permet de vérifier si le neurone est activé.
        """
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class PorteLogique(Neurone):

    def __init__(self, operateur: bool, negatif: bool, enfants: List[Neurone]) -> None:
        self.operateur = operateur
        self.enfants = enfants
        self.negatif = negatif

    def evaluer(self, obstacles: List[Obstacle]) -> bool:
        ou = False
        et = True
        for e in self.enfants:
            b = e.evaluer(obstacles)
            et = et and b
            ou = ou or b
        if self.negatif:
            et = not et
            ou = not ou
        if self.operateur:
            return et
        else:
            return ou

    def __str__(self):
        return f"PL({'et' if self.operateur else 'ou'},{'non' if self.negatif else 'oui'},{str(self.enfants)})"

    def __repr__(self):
        return str(self)


class DetecteurObstacle(Neurone):
    """
    detecte un bloc et un attribut
    """
    types_obstacles = ["bs", "p"]

    def __init__(self, coordonees: List[float], bloc_type: str) -> None:
        self.coordonees = coordonees
        self.bloc_type = bloc_type

    def evaluer(self, obstacles: List[Obstacle]) -> bool:
        for obstacle in obstacles:
            if (obstacle.type == self.bloc_type):
                if (obstacle.p2[0] > self.coordonees[0] > obstacle.p1[0]) and (obstacle.p2[1] > self.coordonees[1] > obstacle.p1[1]):
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
            randint(LARGEUR//2, LARGEUR), randint(250, HAUTEUR_SOL)]
        bloc_type = choice(cls.types_obstacles)
        return DetecteurObstacle(coos, bloc_type)

    def passer_en_porte_logique(self):
        """
        Créer une porte logique de manière aléatoire
        """
        e = deepcopy(self)
        operateur = bool(randint(0, 1))
        negatif = bool(randint(0, 1))
        self = PorteLogique(operateur, negatif, [e])

    def __str__(self):
        return f"DO({self.bloc_type}, {self.coordonees})"


class IA:

    def __init__(self):
        self.reseau: Neurone = DetecteurObstacle.nouveau()
        self.joueur = Joueur.nouveau()

    def muter(self, neurone: Neurone):
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

            if randint(1, 4) == 4:
                # Mutation en porte logique
                neurone.passer_en_porte_logique()

        if isinstance(neurone, PorteLogique):
            if randint(1, 5) == 5:
                # Changement du type booléen
                neurone.operateur = not neurone.operateur

            if randint(1, 10) == 10:
                # Changement du négatif
                neurone.negatif = not neurone.negatif

            if randint(1, 3) == 3:
                # Creation d'une neurone
                for _ in range(randint(0, 2 - len(neurone.enfants))):
                    neurone.enfants.append(DetecteurObstacle.nouveau())

            if randint(0, 1):
                # Mutation des enfants
                for enfant in neurone.enfants:
                    if randint(0, 1):
                        self.muter(enfant)

    def __bool__(self):
        return bool(self.joueur)
