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
        self.IAs = self.IAs[:M]
        print(len(self.IAs))
        print(1)
        for ia in self.IAs:
            ia.reset()
        for to_copy in list(self.IAs):
            for _ in range(D):
                # print(2)
                copied = copy(to_copy)
                IA.muter(copied.reseau)
                self.IAs.append(copied)
        print(3)
        for _ in range(G):
            self.IAs.append(IA())
        print(4)

    def commencer(self):
        for i in range(5):
            l = self.get_level()
            l.start(self.IAs)
            self.IAs.sort(key=lambda ia: ia.score, reverse=True)
            self.muter_IAs()
            print(i)
