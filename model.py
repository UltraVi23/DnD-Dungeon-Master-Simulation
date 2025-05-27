import numpy as np
from .enemy import Enemy
from .player import Player
import .visualize

class Model(object):
    def __init__(self):
        self.GRID_X = 100
        self.GRID_Y = 100
        self.NUM_PLAYERS = 5

        self.grid = np.zeros((self.GRID_Y,self.GRID_X), dtype = object)
        self.initiative_order = self.roll_initiative()
    
    def roll_initiative(self)
        # generate enemies and players and have them roll initiative, then place them in the list based on their number
        # add them to self.grid as you do so
        initiative = []
        return initiative

    def do_stuff(self) # please rename this to make more sense later
        # go through initiative and do actions
        for agent in self.initiative_order:
            agent.do_action(self.grid)

    def show(self) # also chage this name
        # call the visualize function for showing
        # pause
    