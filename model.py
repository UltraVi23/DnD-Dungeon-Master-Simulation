import numpy as np
from .enemy import Enemy
from .player import Player

class Model(object):
    def __init__(self):
        self.GRID_X = 100
        self.GRID_Y = 100
        self.NUM_PLAYERS = 5

        self.grid = np.zeros((self.GRID_Y,self.GRID_X), dtype = object)
        self.enemies = []
        self.players []