from level import Level
from neuronal_network import IA
from typing import Callable
from copy import copy


class EntraineurIA:

    def __init__(self, get_level: Callable[[], Level], n: int = 100):
        self.IAs = [IA() for _ in range(n)]
        self.get_level = get_level

    def muter_IAs(self):
        L = len(self.IAs)
        M = int(L*(10/100))
        D = int(L*(50/100))
        G = int(L*(40/100))

        #sauvegarde de 10% des meilleurs IAs pour la génération suivant
        self.IAs = self.IAs[:M]

        #reset des attributs des IAs
        for ia in self.IAs:
            ia.reset()
        
        #Ajout de 50% d'IAs qui sont des versions muté des 10% de meilleur
        for to_copy in list(self.IAs):
            for _ in range(D):
                # print(2)
                copied = copy(to_copy)
                IA.muter(copied.reseau)
                self.IAs.append(copied)

        #ajout de 40% de nouvelles IAs générer aléatoirement
        for _ in range(G):
            self.IAs.append(IA())

    def commencer(self):
        for i in range(5):
            l = self.get_level()
            l.start(self.IAs)
            self.IAs.sort(key=lambda ia: ia.score, reverse=True)
            self.muter_IAs()
            print(i)
