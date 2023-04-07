from pygame import Surface
from typing import List, Tuple, Callable
from typing_extensions import Self
from ressources import *


class Obstacle:
    """
    pour les types:
        p = pique
        b = bloc
        bs = bloc surface
    """

    def __init__(self, IMAGE, p1: List[float], p2: List[float], type: str):
        self.IMAGE = IMAGE
        self.p1 = p1
        self.p2 = p2
        self.type = type
        pass

    def is_hit(self, xy1: List[float], xy2: List[float]) -> bool:
        """
        Detecte si la valeur passé en paramètre rentre en collision avec l'objet
        """
        if (self.p2[0] >= xy1[0] >= self.p1[0]) or (self.p2[0] >= xy2[0] >= self.p1[0]):
            if (self.p2[1] > xy1[1] > self.p1[1]) or (self.p2[1] >= xy2[1] > self.p1[1]):
                return True
        return False

    def defilement(self, speed: float):
        self.p1[0] -= speed
        self.p2[0] -= speed
        pass


class Joueur:

    def __init__(self, BOB_X: float, BOB_Y: float, surface):
        self.BOB_X = BOB_X
        self.BOB_Y = BOB_Y
        self.surface = surface
        self.surface_actu = surface
        self.image = BOB
        self.LARGEUR, self.HAUTEUR = self.image.get_size()
        self.G = 0.05
        self.V = 0
        self.HAUTEUR_SAUT = 35
        self.VITESSE = 2.5
        self.est_en_train_de_sauter = False
        pass

    @classmethod
    def nouveau(cls):
        return Joueur(LARGEUR//2-25, HAUTEUR_SOL - BOB_HAUTEUR,
                      HAUTEUR_SOL-BOB_HAUTEUR)

    def saut(self, frame: int, screen: Surface) -> Tuple[bool, int]:
        """
        saut() permet de faire sauter BOB en l'affichant un peu plus haut à chaque appel.
        La fonction renvoie False quand l'animation est fini.
        """
        if frame < self.HAUTEUR_SAUT:
            frame += 1
            screen.blit(FILL, (self.BOB_X, self.BOB_Y))
            self.BOB_Y -= self.VITESSE
            screen.blit(BOB, (self.BOB_X, self.BOB_Y))
            return True, frame
        else:
            return False, -1

    def gravite(self):
        """
        gravite() permet d'appliquer une effet de gravité au joueur si il se situe dans les airs
        """
        if self.BOB_Y < self.surface_actu:
            self.V += self.G
            self.BOB_Y += min(self.V, self.surface_actu-self.BOB_Y)
            pygame.event.clear()
        pass

    def actualiser_surface(self, liste_obstacle: list):
        """
        actualiser_surface() permet de gerer la hauteur de la surface afin de pouvoir sauter sur des
        éléments par exemple.
        """
        changed = False
        for obstacle in liste_obstacle:
            if (obstacle.type == "bs") and (self.BOB_Y + self.HAUTEUR <= obstacle.p1[1]):
                if (obstacle.p1[0] <= self.BOB_X <= obstacle.p2[0]) or (obstacle.p1[0] <= self.BOB_X + self.LARGEUR <= obstacle.p2[0]):
                    self.surface_actu = min(
                        self.surface_actu, obstacle.p1[1]-self.HAUTEUR)
                    changed = True
        if not changed:
            self.surface_actu = self.surface
        pass


class Level:

    def __init__(self, screen: Surface, bob: Joueur, *obstacles: Obstacle):
        self.screen = screen
        self.bob = bob
        self.largeur_ecran = self.screen.get_width()
        self.obstacles = list(sorted(obstacles, key=lambda ob: ob.p1[0]))
        self.current = 0
        # Configuration des variables pour le défilement du sol
        self.sol1_pos = 0
        self.sol2_pos = LARGEUR
        self.SPEED = 2.5
        self.DISTANCE = 0

    def get_obstacles(self, stop_when_lose_vision: bool = True):
        """
        renvoi les obstacles dans le champs de vision
        """
        for i in range(self.current, len(self.obstacles)):
            obstacle = self.obstacles[i]
            if obstacle.p2[0] < 0:
                self.current += 1
            elif stop_when_lose_vision and obstacle.p1[0] > self.largeur_ecran:
                break
            else:
                yield obstacle

    def is_bob_dead(self) -> bool:
        """
        isDead() regarde si les coordonnées actuelle de BOB rentrent en collisions avec
        un obstacle éventuel.
        """
        BOB_p1 = [self.bob.BOB_X, self.bob.BOB_Y]
        BOB_p2 = [self.bob.BOB_X + self.bob.LARGEUR,
                  self.bob.BOB_Y + self.bob.HAUTEUR]
        for obstacle in self.get_obstacles(True):
            if obstacle.is_hit(BOB_p1, BOB_p2):
                return True
        return False

    def defilement_obstacle(self):
        """
        Cette fonction permet de faire défiler les obstacles, si les obstacles sont déjà passé
        alors on les retire de la liste liste_obstacle pour éviter de faire des calculs inutiles
        """
        for obstacle in self.get_obstacles(False):
            x, y = obstacle.p1
            self.screen.blit(FILL, (x, y))
            obstacle.defilement(self.SPEED)
            x, y = obstacle.p1
            self.screen.blit(obstacle.IMAGE, (x, y))

    def defilement_sol(self):
        """
        La fonction décale le sol à chaque appel, cela permet de donner l'impression que le sol recule, donc
        que le joueur avance
        """
        self.DISTANCE += 1
        if self.sol1_pos <= -LARGEUR:
            self.sol1_pos = LARGEUR
        if self.sol2_pos <= -LARGEUR:
            self.sol2_pos = LARGEUR
        self.sol1_pos -= self.SPEED
        self.sol2_pos -= self.SPEED
        self.screen.blit(SOL, (self.sol1_pos, HAUTEUR_SOL))
        self.screen.blit(SOL, (self.sol2_pos, HAUTEUR_SOL))
        pass

    def start(self, restart: Callable[[], None]):
        """
        Fonction principale qui tourne tant que le jeu n'est pas fini
        """
        # init
        running = True
        self.screen.blit(FOND, (0, 0))
        self.screen.blit(BOB, (self.bob.BOB_X, self.bob.BOB_Y))
        frame = 0
        clock = pygame.time.Clock()
        pygame.display.flip()

        # loop
        while running:
            self.screen.blit(FOND, (0, 0))
            Bob_position = (self.bob.BOB_X, self.bob.BOB_Y)

            # GRAVITE
            if not self.bob.est_en_train_de_sauter:
                self.bob.gravite()
                Bob_position = (self.bob.BOB_X, self.bob.BOB_Y)
                self.screen.blit(BOB, Bob_position)

            # DEFILEMENT
            self.defilement_obstacle()
            self.defilement_sol()

            # VERIFICATION HITBOX
            running = not self.is_bob_dead()
            if running is False:
                restart()
                break

            # SAUT
            if self.bob.est_en_train_de_sauter:
                self.bob.est_en_train_de_sauter, frame = self.bob.saut(
                    frame, self.screen)
                pygame.event.clear()
            self.bob.actualiser_surface(list(self.get_obstacles()))

            # Lecture des events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # type: ignore
                    running = False
                elif event.type == pygame.KEYDOWN:  # type: ignore
                    self.bob.est_en_train_de_sauter, frame, self.bob.V = True, 0, 0

            # Affichage de la distance parcouru
            pygame.display.update()
            clock.tick(160)
        pygame.quit()  # type: ignore

    @classmethod
    def level_1(cls, screen: Surface) -> Self:
        """
        Fonction de création des obstacles du niveau.
        """
        liste_obstacle: List[Obstacle] = []
        liste_obstacle.append(Obstacle(PIQUE, [1000, 250], [1050, 300], "p"))
        liste_obstacle.append(
            Obstacle(PIQUE_REVERSE, [1000, 100], [1050, 150], "p"))
        liste_obstacle.append(Obstacle(BLOC, [1000, 50], [1050, 100], "b"))
        liste_obstacle.append(Obstacle(BLOC, [1000, 0], [1050, 50], "b"))
        liste_obstacle.append(Obstacle(BLOC, [1050, 250], [1100, 300], "bs"))
        liste_obstacle.append(Obstacle(PIQUE, [1100, 250], [1150, 300], "p"))
        liste_obstacle.append(Obstacle(BLOC, [1320, 200], [1370, 250], "bs"))
        liste_obstacle.append(Obstacle(BLOC, [1500, 200], [1550, 250], "bs"))
        liste_obstacle.append(Obstacle(BLOC, [1550, 200], [1600, 250], "bs"))
        liste_obstacle.append(
            Obstacle(PIQUE_REVERSE, [1600, 100], [1650, 150], "p"))
        liste_obstacle.append(Obstacle(BLOC, [1600, 50], [1650, 100], "b"))
        liste_obstacle.append(Obstacle(BLOC, [1600, 0], [1650, 50], "b"))
        liste_obstacle.append(Obstacle(PIQUE, [1580, 250], [1630, 300], "p"))
        liste_obstacle.append(Obstacle(PIQUE, [1820, 250], [1870, 300], "p"))
        liste_obstacle.append(Obstacle(PIQUE, [2050, 250], [2100, 300], "p"))
        liste_obstacle.append(Obstacle(BLOC, [2100, 250], [2150, 300], "bs"))
        liste_obstacle.append(Obstacle(PIQUE, [2150, 250], [2200, 300], "p"))
        liste_obstacle.append(Obstacle(PIQUE, [2200, 250], [2250, 300], "p"))
        liste_obstacle.append(Obstacle(PIQUE, [2250, 250], [2300, 300], "p"))
        liste_obstacle.append(Obstacle(BLOC, [2300, 250], [2350, 300], "bs"))
        liste_obstacle.append(Obstacle(GIGACHAD, [2600, 50], [2650, 100], "b"))
        niveau = Level(screen, Joueur.nouveau(), *liste_obstacle)
        return niveau
