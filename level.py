from ressources import *
from environnement import *
from neuronal_network import *


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

        # IA
        p1 = IA().reseau
        if isinstance(p1, DetecteurObstacle):
            print(p1.coordonees, p1.bloc_type)

        # loop
        while running:
            self.screen.blit(FOND, (0, 0))
            Bob_position = (self.bob.BOB_X, self.bob.BOB_Y)

            # IA
            print(p1, self.obstacles[0].p1[0])
            if p1.evaluer(list(self.get_obstacles())):
                self.bob.est_en_train_de_sauter, frame, self.bob.V = True, 0, 0

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
    def level_1(cls, screen: Surface):
        """
        Fonction de création des obstacles du niveau.
        """
        liste_obstacle: List[Obstacle] = []
        liste_obstacle.append(Obstacle(PIQUE, [1000, 250], [1050, 300], "p"))
        liste_obstacle.append(
            Obstacle(PIQUE_REVERSE, [1000, 100], [1050, 150], "p"))
        liste_obstacle.append(Obstacle(BLOC, [1000, 50], [1050, 100], "bs"))
        liste_obstacle.append(Obstacle(BLOC, [1000, 0], [1050, 50], "bs"))
        liste_obstacle.append(Obstacle(BLOC, [1050, 250], [1100, 300], "bs"))
        liste_obstacle.append(Obstacle(PIQUE, [1100, 250], [1150, 300], "p"))
        liste_obstacle.append(Obstacle(BLOC, [1320, 200], [1370, 250], "bs"))
        liste_obstacle.append(Obstacle(BLOC, [1500, 200], [1550, 250], "bs"))
        liste_obstacle.append(Obstacle(BLOC, [1550, 200], [1600, 250], "bs"))
        liste_obstacle.append(
            Obstacle(PIQUE_REVERSE, [1600, 100], [1650, 150], "p"))
        liste_obstacle.append(Obstacle(BLOC, [1600, 50], [1650, 100], "bs"))
        liste_obstacle.append(Obstacle(BLOC, [1600, 0], [1650, 50], "bs"))
        liste_obstacle.append(Obstacle(PIQUE, [1580, 250], [1630, 300], "p"))
        liste_obstacle.append(Obstacle(PIQUE, [1820, 250], [1870, 300], "p"))
        liste_obstacle.append(Obstacle(PIQUE, [2050, 250], [2100, 300], "p"))
        liste_obstacle.append(Obstacle(BLOC, [2100, 250], [2150, 300], "bs"))
        liste_obstacle.append(Obstacle(PIQUE, [2150, 250], [2200, 300], "p"))
        liste_obstacle.append(Obstacle(PIQUE, [2200, 250], [2250, 300], "p"))
        liste_obstacle.append(Obstacle(PIQUE, [2250, 250], [2300, 300], "p"))
        liste_obstacle.append(Obstacle(BLOC, [2300, 250], [2350, 300], "bs"))
        liste_obstacle.append(
            Obstacle(GIGACHAD, [2600, 50], [2650, 100], "bs"))
        niveau = Level(screen, Joueur.nouveau(), *liste_obstacle)
        return niveau

    @classmethod
    def level_2(cls, screen: Surface):
        """
        Fonction de création des obstacles du niveau.
        """
        liste_obstacle: List[Obstacle] = []
        liste_obstacle.append(Obstacle(BLOC, [1000, 250], [1050, 300], "bs"))
        niveau = Level(screen, Joueur.nouveau(), *liste_obstacle)
        return niveau
