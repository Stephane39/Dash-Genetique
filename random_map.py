from typing import List
from environnement import Obstacle
from random import choice
from ressources import *
from copy import copy

def liste_etape()->List[List[Obstacle]]:
    liste_etape = []

    etape1 = []
    etape1.append(Obstacle(BLOC, [0, 250], [50, 300], "bs"))
    etape1.append(Obstacle(PIQUE, [50, 250], [100, 300], "p"))
    etape1.append(Obstacle(PIQUE, [100, 250], [150, 300], "p"))
    etape1.append(Obstacle(PIQUE, [150, 250], [200, 300], "p"))
    etape1.append(Obstacle(BLOC, [200, 200], [250, 250], "bs"))
    etape1.append(Obstacle(BLOC, [250, 200], [300, 250], "bs"))
    etape1.append(Obstacle(PIQUE_REVERSE, [450, 150], [500, 200], "p"))
    etape1.append(Obstacle(BLOC, [450, 100], [500, 150], "bs"))
    etape1.append(Obstacle(BLOC, [450, 50], [500, 100], "bs"))
    etape1.append(Obstacle(BLOC, [450, 0], [500, 50], "bs"))
    liste_etape.append(etape1)

    etape2 = []
    etape2.append(Obstacle(BLOC, [0, 250], [50, 300], "bs"))
    etape2.append(Obstacle(PIQUE, [50, 250], [100, 300], "p"))
    etape2.append(Obstacle(PIQUE, [100, 250], [150, 300], "p"))
    etape2.append(Obstacle(PIQUE, [150, 250], [200, 300], "p"))
    etape2.append(Obstacle(BLOC, [250, 200], [300, 250], "bs"))
    etape2.append(Obstacle(BLOC, [500, 150], [550, 200], "bs"))
    etape2.append(Obstacle(BLOC, [750, 100], [800, 150], "bs"))
    etape2.append(Obstacle(BLOC, [850, 150], [900, 200], "bs"))
    etape2.append(Obstacle(PIQUE_REVERSE, [900, 30], [950, 80], "p"))
    etape2.append(Obstacle(BLOC, [900,-20], [950, 30], "bs"))
    etape2.append(Obstacle(BLOC, [950, 200], [1000, 250], "bs"))
    etape2.append(Obstacle(PIQUE_REVERSE, [1000, 0], [1050, 50], "p"))
    etape2.append(Obstacle(PIQUE, [1000, 250], [1050, 300], "p"))
    etape2.append(Obstacle(BLOC, [1050, 250], [1100, 300], "bs"))
    etape2.append(Obstacle(PIQUE, [1050, 200], [1100, 250], "p"))
    liste_etape.append(etape2)

    etape3 = []
    etape3.append(Obstacle(PIQUE, [0, 250], [50, 300], "p"))
    etape3.append(Obstacle(PIQUE_REVERSE, [0, 100], [50, 150], "p"))
    etape3.append(Obstacle(BLOC, [0, 50], [50, 100], "bs"))
    etape3.append(Obstacle(BLOC, [0, 0], [50, 50], "bs"))
    etape3.append(Obstacle(BLOC, [50, 250], [100, 300], "bs"))
    etape3.append(Obstacle(PIQUE, [100, 250], [150, 300], "p"))
    liste_etape.append(etape3)

    

    return liste_etape

class randomLevel:
    """
    class qui vise à génerer des maps de manière aléatoire
    """
    def __init__(self, etapes:List[List[Obstacle]], nbEtapes:int = 3) -> None:
        self.etapes = etapes
        self.nbEtapes = nbEtapes
        self.map:List[Obstacle] = []
        self.distance = 400
        self.debut = LARGEUR

    def createRandomLevel(self)->None:
        """
        créer un map self.map d'étapes aléatoire de longueur self.nbEtapes
        les unes à la suite des autresgrâce à self.etapes
        """
        XlastEtape = self.debut
        for i in range(self.nbEtapes):
            for e in [e.clone() for e in choice(self.etapes)]:
                e.p1[0]+=XlastEtape
                e.p2[0]+=XlastEtape
                self.map.append(e)
            XlastEtape = self.map[-1].p2[0] + self.distance

    def __str__(self)->str:
        return f"Map: {self.map}, Nombre d'étapes: {self.nbEtapes}, Distance: {self.distance}, Début: {self.debut}"
    
    def __repr__(self):
        return f"randomLevel(etapes={self.etapes}, nbEtapes={self.nbEtapes}, map={self.map}, distance={self.distance}, debut={self.debut})"

    @classmethod
    def nouveau(cls):
        new = randomLevel(liste_etape(), 5)
        new.createRandomLevel()
        return new

