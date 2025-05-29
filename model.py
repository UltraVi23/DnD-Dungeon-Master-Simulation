import numpy as np
from .enemy import Enemy
from .player import Player
import .visualize

class Model(object):
    def __init__(self):
        self.GRID_X = 100
        self.GRID_Y = 100
        self.NUM_PLAYERS = 5
        self.NUM_ENEMIES = 10

        self.grid = np.zeros((self.GRID_Y, self.GRID_X), dtype=object)
        self.initiative_order = self.roll_initiative()
        self.battle_length = 0
        self.total_damage_dealt = 0
        self.total_damage_received = 0
        self.player_survival_count = 0
    
    def roll_initiative(self):
        initiative = []
        for _ in range(self.NUM_PLAYERS):
            player = Player(np.random.randint(self.GRID_X), np.random.randint(self.GRID_Y), 'melee')
            initiative.append(player)
            self.grid[player.loc[1], player.loc[0]] = player
        
        for _ in range(self.NUM_ENEMIES):
            enemy = Enemy(np.random.randint(self.GRID_X), np.random.randint(self.GRID_Y), 'attack_nearest')
            initiative.append(enemy)
            self.grid[enemy.loc[1], enemy.loc[0]] = enemy
        
        np.random.shuffle(initiative)
        return initiative

    def execute_turns(self):
        for agent in self.initiative_order:
            agent.do_action(self.grid)
            self.battle_length += 1

    def show(self):
        # call the visualize function for showing
        # pause
    