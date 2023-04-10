from level import Level
from neuronal_network import IA
from typing import Callable
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
        # sauvegarde de 10% des meilleurs IAs pour la génération suivant
        self.IAs = self.IAs[:M]
        print(self.IAs[0].reseau)
        # Ajout de 50% d'IAs qui sont des versions muté des 10% de meilleur
        for ia in list(self.IAs):
            # reset des attributs des IAs
            ia.reset()
            for _ in range(D):
                enfant = ia.copy()
                self.IAs.append(enfant)
        for ia in self.IAs:
            ia.reseau = IA.muter(ia.reseau)
            print(ia.reseau)
        # ajout de 40% de nouvelles IAs générer aléatoirement
        for _ in range(G):
            self.IAs.append(IA())

    def save(self, path: str):
        with open(path, "w") as file:
            file.write(str(self.IAs[0].reseau))

    def commencer(self):
        screen: pygame.surface.Surface = pygame.display.set_mode((LARGEUR, HAUTEUR))
        nbGeneration = 0
        score = 0
        for _ in range(100):
            l = self.get_level(screen)
            l.start(self.IAs, 160, nbGeneration, score)
            self.IAs.sort(key=lambda ia: (
                ia.joueur.alive, ia.score), reverse=True)
            self.save("./saved.txt")
            score = sum(map(lambda ia: ia.score, self.IAs))//len(self.IAs)
            nbGeneration+=1
            self.muter_IAs()


        screen: pygame.surface.Surface = pygame.display.set_mode(
            (LARGEUR, HAUTEUR))
        l = self.get_level(screen)
        l.start(self.IAs, 160, nbGeneration, score)
        self.save("./saved.txt")
