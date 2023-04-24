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
        D = int(L*(70/100)/M)
        G = int(L*(20/100))
        # sauvegarde de 10% des meilleurs IAs pour la génération suivant
        meilleur = self.IAs[0]
        self.IAs = []
        meilleur.reset()
        # Ajout de 70% d'IAs qui sont des versions muté des 10% de meilleur
        for _ in range(L):
            enfant = meilleur.copy()
            self.IAs.append(enfant)
        """
        for ia in list(self.IAs):
            # reset des attributs des IAs
            ia.reset()
            for _ in range(D):
                enfant = ia.copy()
                self.IAs.append(enfant)
        """
        for ia in self.IAs:
            ia.reseau = IA.muter(ia.reseau)
        # ajout de 20% de nouvelles IAs générer aléatoirement

    def save(self, path: str):
        with open(path, "w") as file:
            file.write(str(self.IAs[0].reseau))

    def commencer(self):
        screen: pygame.surface.Surface = pygame.display.set_mode((LARGEUR, HAUTEUR))
        nbGeneration = 0
        score = 0
        for _ in range(500):
            #lancement de la simulation de la génération nbGeneration
            l = self.get_level(screen)
            l.start(self.IAs, 160, nbGeneration, score)

            #Ajustement du score d'une IA en fonction de la taille de son réseau
            """
            for ia in self.IAs:
                ia.calculer_taille()
                ia.score = ia.score - ia.taille_reseau
            """

            #Tri des IA en fonction de  leur score lors cette génération
            self.IAs.sort(key=lambda ia: (
                ia.joueur.alive, ia.score), reverse=True)
            
            #sauvegarde de la meuilleur ia de la géneration
            self.save("./saved.txt")

            #ajustement des variables d'affichages et mutation des IAs pour la génération future
            score = (sum(map(lambda ia: ia.score, self.IAs))//len(self.IAs))
            nbGeneration+=1
            self.muter_IAs()


        screen: pygame.surface.Surface = pygame.display.set_mode(
            (LARGEUR, HAUTEUR))
        l = self.get_level(screen)
        l.start(self.IAs, 160, nbGeneration, score)
        self.save("./saved.txt")
