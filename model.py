import numpy as np
from enemy import Enemy
from player import Player
import matplotlib.pyplot as plt
from visualize import visualize_grid

class Model(object):
    def __init__(self):
        self.GRID_X = 100
        self.GRID_Y = 100

        self.NUM_PLAYERS = 5
        self.NUM_ENEMIES = 10

        self.player_damage_dealt = 0
        self.enemy_damage_dealt = 0

        self.players_killed = 0
        self.enemies_killed = 0

        self.grid = np.zeros((self.GRID_Y, self.GRID_X), dtype=object)
        self.initiative_order = self.roll_initiative()
        self.battle_length = 0
        self.total_damage_dealt = 0
        self.total_damage_received = 0
        self.player_survival_count = 0
        self.message = "Initiating Battle Sequence..."
    
    def roll_initiative(self):
        """
        This function rolls initiative for the combat, or the order in which players and enemies will attack.

        Inputs: 
        Self
        Outputs: 
        initiative (list of Player and Enemy objects in random order)
        """
        initiative = []
        # Currently fully random, will overwrite preexisting players and enemies
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

    def execute_turns(self): # I'm considering making this just do one player's action at a time so that we can see the messages individually
        for agent in self.initiative_order:
            self.message = agent.do_action(self.grid)
            self.battle_length += 1

def show(model):
    """
    This function initializes the model and starts the battle simulation, visualizing the grid and updating it in real-time.

    Inputs: 
    model (Model object)
    Outputs: 
    None, but visualizes the grid and updates it in real-time.
    """
    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.show()

    # Simulation loop
    while 1: # currently infinite - will need to be adjusted later
        model.execute_turns()
        model.battle_length += 1
        visualize_grid(model.grid, message=model.message, ax=ax)
    plt.close(fig)
    pass
    
if __name__ == "__main__":
    model = Model()
    show(model)
    print(f"Battle Length: {model.battle_length}")
    print(f"Total Damage Dealt: {model.total_damage_dealt}")
    print(f"Total Damage Received: {model.total_damage_received}")
    print(f"Player Survival Count: {model.player_survival_count}")