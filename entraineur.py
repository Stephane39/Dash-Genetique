from level import Level
from neuronal_network import IA


class EntraineurIA:

    def __init__(self, level: Level, n=100):
        self.IAs = [IA() for _ in range(n)]
        self.level = level

    def commencer(self):
        self.level.start(self.IAs)
