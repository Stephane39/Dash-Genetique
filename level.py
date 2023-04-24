from ressources import *
from environnement import *
from neuronal_network import *
from random_map import *
from pygame import surface


class Level:

    def __init__(self, screen: surface.Surface, obstacles: Obstacle):
        self.screen = screen
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

    def is_bob_dead(self, bob: Joueur) -> bool:
        """
        isDead() regarde si les coordonnées actuelle de BOB rentrent en collisions avec
        un obstacle éventuel.
        """
        BOB_p1 = [bob.BOB_X, bob.BOB_Y]
        BOB_p2 = [bob.BOB_X + bob.LARGEUR,
                  bob.BOB_Y + bob.HAUTEUR]
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

    def start(self, joueurs: List[IA], fps: int = 160, nbGeneration:int = 0, score:int = 0):
        """
        Fonction principale qui tourne tant que le jeu n'est pas fini
        """
        clock = pygame.time.Clock()
        i = 0

        font = pygame.font.Font('freesansbold.ttf', 16)
        Text_Generation = font.render('Generation: ' + str(nbGeneration) , True, (255, 255, 255))

        Text_Score = font.render('Score: ' + str(score) , True, (255, 255, 255))
        # loop
        while any(joueurs) and self.obstacles[-1].p2[0] > 0:
            self.screen.blit(FOND, (0, 0))

            #Affichage du nombre de généartion
            self.screen.blit(Text_Generation, (0, 0))
            #Affichage du score de la génération précedente
            self.screen.blit(Text_Score, (0, Text_Generation.get_size()[1]))
            for ia in joueurs:
                bob = ia.joueur
                if not bob:
                    continue
                # AFFICHAGE
                self.screen.blit(bob.image, (bob.BOB_X, bob.BOB_Y))
                # GRAVITE
                if not bob.est_en_train_de_sauter:
                    bob.gravite()
                # VERIFICATION HITBOX
                if self.is_bob_dead(bob):
                    ia.score = i
                    bob.alive = False
                # SAUT
                if bob.est_en_train_de_sauter:
                    bob.est_en_train_de_sauter, bob.frame = bob.saut(
                        bob.frame)
                bob.actualiser_surface(list(self.get_obstacles()))
                # Lecture des events
                # type: ignore
                if (ia.reseau.evaluer(list(self.get_obstacles()), [ia.joueur.BOB_X, ia.joueur.BOB_Y])) and (not bob.est_en_train_de_sauter) and (bob.BOB_Y == bob.surface_actu):
                    bob.est_en_train_de_sauter, bob.frame, bob.V = True, 0, 0

            # Ferme le jeu si une touche est pressé.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # DEFILEMENT
            self.defilement_obstacle()
            self.defilement_sol()
            pygame.display.update()
            clock.tick(fps)
            i += 1

    @classmethod
    def level_1(cls, screen: surface.Surface):
        """
        Fonction de création des obstacles du niveau.
        """
        liste_obstacle: List[Obstacle] = []

        liste_obstacle.append(Obstacle(PIQUE, [1000, 250], [1050, 300], "p"))
        liste_obstacle.append(Obstacle(PIQUE_REVERSE, [1000, 100], [1050, 150], "p"))
        liste_obstacle.append(Obstacle(BLOC, [1000, 50], [1050, 100], "bs"))
        liste_obstacle.append(Obstacle(BLOC, [1000, 0], [1050, 50], "bs"))
        liste_obstacle.append(Obstacle(BLOC, [1050, 250], [1100, 300], "bs"))
        liste_obstacle.append(Obstacle(PIQUE, [1100, 250], [1150, 300], "p"))
        liste_obstacle.append(Obstacle(BLOC, [1320, 200], [1370, 250], "bs"))
        liste_obstacle.append(Obstacle(BLOC, [1500, 200], [1550, 250], "bs"))
        liste_obstacle.append(Obstacle(BLOC, [1550, 200], [1600, 250], "bs"))
        liste_obstacle.append(Obstacle(PIQUE_REVERSE, [1600, 100], [1650, 150], "p"))
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
        liste_obstacle.append(Obstacle(BLOC, [2300, 250], [2350, 300], "bs"))
        liste_obstacle.append(Obstacle(BLOC, [2350, 250], [2400, 300], "bs"))
        liste_obstacle.append(Obstacle(BLOC, [2400, 250], [2450, 300], "bs"))
        liste_obstacle.append(Obstacle(PIQUE, [2450, 250], [2500, 300], "p"))
        liste_obstacle.append(Obstacle(BLOC, [2500, 250], [2550, 300], "bs"))
        liste_obstacle.append(Obstacle(BLOC, [2550, 250], [2600, 300], "bs"))
        liste_obstacle.append(Obstacle(BLOC, [2550, 50], [2600, 100], "bs"))
        liste_obstacle.append(Obstacle(BLOC, [2550, 0], [2600, 50], "bs"))
        liste_obstacle.append(Obstacle(BLOC, [2600, 250], [2650, 300], "bs"))
        liste_obstacle.append(Obstacle(PIQUE, [2650, 250], [2700, 300], "p"))
        liste_obstacle.append(Obstacle(PIQUE, [2700, 250], [2750, 300], "p"))
        liste_obstacle.append(Obstacle(PIQUE, [2750, 250], [2800, 300], "p"))
        liste_obstacle.append(Obstacle(BLOC, [2750, 200], [2800, 250], "bs"))
        liste_obstacle.append(Obstacle(PIQUE, [2800, 250], [2850, 300], "p"))
        liste_obstacle.append(Obstacle(PIQUE, [2850, 250], [2900, 300], "p"))
        liste_obstacle.append(Obstacle(PIQUE, [2900, 250], [2950, 300], "p"))
        liste_obstacle.append(Obstacle(BLOC, [2900, 150], [2950, 200], "bs"))
        liste_obstacle.append(Obstacle(PIQUE_REVERSE, [2950, 0], [3000, 50], "p"))
        liste_obstacle.append(Obstacle(PIQUE, [3200, 250], [3250, 300], "p"))
        liste_obstacle.append(Obstacle(BLOC, [3250, 250], [3300, 300], "bs"))
        liste_obstacle.append(Obstacle(PIQUE_REVERSE, [3250, 100], [3300, 150], "p"))
        liste_obstacle.append(Obstacle(BLOC, [3250, 50], [3300, 100], "bs"))
        liste_obstacle.append(Obstacle(BLOC, [3250, 0], [3300, 50], "bs"))

        niveau = Level(screen, liste_obstacle)
        return niveau

    @classmethod
    def level_2(cls, screen: surface.Surface):
        """
        Fonction de création des obstacles du niveau.
        """
        liste_obstacle: List[Obstacle] = []
        liste_obstacle.append(Obstacle(BLOC, [1000, 250], [1050, 300], "bs"))
        niveau = Level(screen, liste_obstacle)
        return niveau
    
    @classmethod
    def level_random(cls, screen: surface.Surface):
        """
        Fonction de création des obstacles du niveau.
        """
        return Level(screen, randomLevel.nouveau().map)
