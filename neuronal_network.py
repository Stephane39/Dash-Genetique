from typing import List, Tuple
from abc import abstractmethod
from random import randint, choice
from ressources import LARGEUR, HAUTEUR
from copy import deepcopy


class Neurone:

    @abstractmethod
    def evaluer(self) -> bool:
        """
        Cette méthode permet de vérifier si le neurone est activé.
        """
        pass


class PorteLogique(Neurone):

    def __init__(self, operateur: bool, negatif: bool, enfants: List[Neurone]) -> None:
        self.operateur = operateur
        self.enfants = enfants
        self.negatif = negatif

    def evaluer(self) -> bool:
        ou = False
        et = True
        for e in self.enfants:
            b = e.evaluer()
            et = et and b
            ou = ou or b
        if self.negatif:
            et = not et
            ou = not ou
        if self.operateur:
            return et
        else:
            return ou


class DetecteurObstacle(Neurone):
    """
    detecte un bloc et un attribut
    """
    types_obstacles = ["bs", "p"]

    def __init__(self, coordonees: List[int], bloc_type: str) -> None:
        self.coordonees = coordonees
        self.bloc_type = bloc_type

    def evaluer(self, obstacles: List[Obstacle]) -> bool:
        for obstacle in obstacles:
            if (obstacle.type == self.bloc_type):
                if (obstacle.p2[0] > self.coordonees[0] > obstacle.p1[0]) and (obstacle.p1[1] > self.coordonees[1] > obstacle.p2[1]):
                    return True
        return False

    def random_type(self):
        return choice(self.types_obstacles)

    @classmethod
    def nouveau(cls):
        """
        creer un truc random
        """
        coos = [randint(0, LARGEUR-1), randint(0, HAUTEUR-1)]
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


class IA:

    def __init__(self):
        self.reseau: Neurone = DetecteurObstacle.nouveau()

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

            if randint(1, 10) == 10:
                # Creation d'une neurone
                for _ in range(randint(1, 2)):
                    neurone.enfants.append(DetecteurObstacle.nouveau())

            if randint(0, 1):
                # Mutation des enfants
                for enfant in neurone.enfants:
                    if randint(0, 1):
                        self.muter(enfant)
