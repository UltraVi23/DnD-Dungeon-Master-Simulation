import numpy as np

class Enemy(object):
    def __init__ (self, loc_x, loc_y, strategy):
        self.loc = (loc_x, loc_y)
        self.strat = strategy # Attack nearest, strongest, weakest, uniform, etc.
        self.health = np.random.randint(30,60)
        # Implement armor class?
        self.strength = 4
        self.damage_die = 8
        self.speed = 6 # number of grids not feet: 1 grid = 5 feet

    def roll(die, plus):
        """
        Rolls a die with a given number of sides and adds a modifier.
        Inputs:
        die: number of sides on the die (e.g., 20 for a d20)
        plus: modifier to add to the roll (e.g., attack bonus)
        Outputs:
        - result: integer result of the roll plus modifier
        """
        return np.random.randint(1, die) + plus

    def do_action(self, grid):
        # choose an action to do (move, attack)
        # update grid

        # for movement go somewhere based on chosen action, move up till max movement if possible
        pass