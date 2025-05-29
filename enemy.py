import numpy as np

class Enemy(object):
    def __init__ (self, loc_x, loc_y, strategy):
        self.loc = (loc_x, loc_y)
        self.strat = strategy # Attack nearest strongest, weakest, uniform, etc.
        self.health = np.random.randint(30,60)
        self.strength = 4
        self.damage_die = 8
        self.speed = 6 # number of grids not feet

    def roll(die, plus):
        return np.random.randint(1, die) + plus

    def do_action(self, grid):
        # choose an action to do (move, attack)
        # update grid

        # for movement go somewhere based on chosen action, move up till max movement if possible
        pass