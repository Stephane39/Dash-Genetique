from typing import List, Tuple
from abc import abstractmethod
from random import randint

class Neurone:

    @abstractmethod    
    def evaluer(self)->bool:
        """
        Cette méthode permet de vérifier si le neurone est activé.
        """
        pass




class DetecteurObstacle(Neurone):
    """
    detecte un bloc et un attribut
    """

    def __init__(self, coordonees:List[int], bloc_type:str) -> None:
        self.coordonees = coordonees
        self.bloc_type = bloc_type
    
    def evaluer(self, obstacles: List[Obstacle])->bool:
        for obstacle in obstacles:
            if (obstacle.type == self.bloc_type):
                if (obstacle.p2[0] > self.coordonees[0] > obstacle.p1[0]) and (obstacle.p1[1] > self.coordonees[1] > obstacle.p2[1]):
                    return True
        return False

class PorteLogique(Neurone):

    def __init__(self, operateur: bool, negatif: bool, enfants: Tuple[Neurone, Neurone]) -> None:
        self.operateur = operateur
        self.enfants = enfants
        self.negatif = negatif
    
    def evaluer(self)->bool:
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


def muter(neurone: Neurone):
    """
    DetecteurObstacle:
        peut changer les coordonnées
        peut changer le type de bloc
        peut se muter en porte logique
    PorteLogique:
        peut changer le type booleen
        peut changer le negatif
        peut muter ses enfants
    """
    if isinstance(neurone, DetecteurObstacle):
        pass
    if isinstance(neurone, PorteLogique):
        pass

class IA:
    def __init__(self):
        self.reseau: Neurone = DetecteurObstacle()

