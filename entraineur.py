from level import Level
from neuronal_network import IA
from typing import Callable
from copy import copy
from ressources import LARGEUR, HAUTEUR
import pygame


class EntraineurIA:

    def __init__(self, get_level: Callable[[pygame.surface.Surface], Level], n: int = 100):
        self.IAs = [IA() for _ in range(n)]
        self.get_level = get_level

    def muter_IAs(self):
        L = len(self.IAs)
        M = int(L*(10/100))
        D = int(L*(50/100)/M)
        G = int(L*(40/100))
        print(M+D*M+G)
        self.IAs = self.IAs[:M]
        print(len(self.IAs))
        for ia in self.IAs:
            ia.reset()
        for to_copy in list(self.IAs):
            for _ in range(D):
                copied = copy(to_copy)
                IA.muter(copied.reseau)
                self.IAs.append(copied)
        for _ in range(G):
            self.IAs.append(IA())

    def commencer(self):
        for i in range(5):
            screen: pygame.surface.Surface = pygame.display.set_mode(
                (LARGEUR, HAUTEUR))
            l = self.get_level(screen)
            l.start(self.IAs)
            self.IAs.sort(key=lambda ia: ia.score, reverse=True)
            self.muter_IAs()
            print(i)
