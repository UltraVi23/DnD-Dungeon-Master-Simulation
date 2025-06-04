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
            self.grid[player.loc[0], player.loc[1]] = player
        
        for _ in range(self.NUM_ENEMIES):
            enemy = Enemy(np.random.randint(self.GRID_X), np.random.randint(self.GRID_Y), 'attack_strongest')
            initiative.append(enemy)
            self.grid[enemy.loc[0], enemy.loc[1]] = enemy
        
        np.random.shuffle(initiative)
        return initiative

    def execute_turns(self):
        # Create a copy since we'll be modifying the list while iterating
        current_initiative = self.initiative_order.copy()
        
        for agent in current_initiative:
            # Skip if agent is already dead
            if agent.health <= 0:
                continue
                
            dmg_dealt,dmg_recieved = agent.do_action(self.grid)
            self.total_damage_dealt += dmg_dealt
            self.total_damage_received += dmg_recieved
            
            # Remove dead entities from initiative order
            self.initiative_order = [
                entity for entity in self.initiative_order 
                if entity.health > 0
            ]
            
            # Update stats
            if isinstance(agent, Player):
                if agent.health <= 0:
                    self.players_killed += 1
            elif isinstance(agent, Enemy):
                if agent.health <= 0:
                    self.enemies_killed += 1
                    
            self.battle_length += 1

    def update_grid_state(self):
        """
        Cleans up the grid by removing dead entities and updating entity counts
        """
        for y in range(self.GRID_Y):
            for x in range(self.GRID_X):
                entity = self.grid[y, x]
                if isinstance(entity, (Player, Enemy)) and entity.health <= 0:
                    self.grid[y, x] = None

    def get_all_players(self):
        """Returns a list of all living players in the grid"""
        return [cell for cell in self.grid.flat if isinstance(cell, Player)]

    def get_all_enemies(self):
        """Returns a list of all living enemies in the grid"""
        return [cell for cell in self.grid.flat if isinstance(cell, Enemy)]

def show(model):
    """
    This function initializes the model and starts the battle simulation, 
    visualizing the grid and updating it in real-time.
    """
    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.show()

    # Simulation loop
    while True:
        model.execute_turns()
        model.update_grid_state()
        model.battle_length += 1
        visualize_grid(model.grid, message=model.message, ax=ax, pause=0.1)
        
        # Check if battle should end
        if len(model.get_all_players()) == 0 or len(model.get_all_enemies()) == 0:
            break
            
    plt.close(fig)
    
if __name__ == "__main__":
    model = Model()
    show(model)
    print(f"Battle Length: {model.battle_length}")
    print(f"Total Damage Dealt: {model.total_damage_dealt}")
    print(f"Total Damage Received: {model.total_damage_received}")
    print(f"Player Survival Count: {model.player_survival_count}")