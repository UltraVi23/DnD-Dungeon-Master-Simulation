import numpy as np

class Player(object):
    def __init__(self, loc_x, loc_y, strategy):
        self.loc = (loc_x, loc_y)
        self.strat = strategy # melee or ranged
        self.health = np.random.randint(30,60)
        self.strength = 4
        self.damage_die = 8