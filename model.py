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
        self.enemy_survival_count = 0
        self.message = "Initiating Battle Sequence..."

        self.turn_living_agents = []
        self.turn_attacks = []
    
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
        attacks_this_turn = 0
        for agent in current_initiative:
            # Skip if agent is already dead
            if agent.health <= 0:
                continue
                
            dmg_dealt, dmg_recieved = agent.do_action(self.grid)
            self.total_damage_dealt += dmg_dealt
            self.total_damage_received += dmg_recieved
            if dmg_dealt > 0 or dmg_recieved > 0:
                attacks_this_turn += 1
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

            self.turn_living_agents.append(len(self.get_all_players()) + len(self.get_all_enemies()))
            self.turn_attacks.append(attacks_this_turn)

    def compute_metrics(self):
        tension = np.mean(self.turn_living_agents) if self.turn_living_agents else 0
        fairness = (self.player_survival_count / (self.player_survival_count + self.enemy_survival_count)
                    if (self.player_survival_count + self.enemy_survival_count) > 0 else 0)
        engagement = np.mean(self.turn_attacks) if self.turn_attacks else 0
        return {
            "Tension": tension,
            "Fairness": fairness,
            "Engagement": engagement
        }

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

def show(model, visualize = True):
    """
    This function initializes the model and starts the battle simulation, 
    visualizing the grid and updating it in real-time.
    """
    if visualize:
        plt.ion()  # Enable interactive mode
        fig, ax = plt.subplots(figsize=(8, 8))
        plt.show()

    # Simulation loop
    while True:
        model.execute_turns()
        model.update_grid_state()
        model.battle_length += 1
        model.player_survival_count = len(model.get_all_players())
        model.enemy_survival_count = len(model.get_all_enemies())
        if visualize:
            visualize_grid(model.grid, message=model.message, ax=ax, pause=0.1)
        
        # Check if battle should end
        if len(model.get_all_players()) == 0:
            print("All players defeated. Enemies win.")
            break
        if len(model.get_all_enemies()) == 0:
            print("All enemies defeated. Players win!")
            break
    if visualize:  
        plt.close(fig)
    
def batch_simulation(num_runs=10, num_players=5, num_enemies=10):
    results = []
    for i in range(num_runs):
        model = Model()
        model.NUM_PLAYERS = num_players
        model.NUM_ENEMIES = num_enemies
        model.grid = np.zeros((model.GRID_Y, model.GRID_X), dtype=object)
        model.initiative_order = model.roll_initiative()
        show(model, visualize=False)  # Run without visualization for batch simulation
        metrics = model.compute_metrics()
        results.append(metrics)
    print("\nBatch Simulation Results:")
    for i, m in enumerate(results):
        print(f"Run {i+1}:")
        print(f"  Tension   : {float(m['Tension']):.2f} (avg. living agents per turn)")
        print(f"  Fairness  : {float(m['Fairness']):.2f} (1=all players survive, 0=all enemies survive)")
        print(f"  Engagement: {float(m['Engagement']):.2f} (avg. attacks per turn)")
    # Compute averages
    avg_metrics = {k: float(np.mean([m[k] for m in results])) for k in results[0]}
    print("\nAverage Metrics (across all runs):")
    print(f"  Tension   : {avg_metrics['Tension']:.2f} (avg. living agents per turn)")
    print(f"  Fairness  : {avg_metrics['Fairness']:.2f} (1=all players survive, 0=all enemies survive)")
    print(f"  Engagement: {avg_metrics['Engagement']:.2f} (avg. attacks per turn)")


if __name__ == "__main__":
    model = Model()
    show(model)
    print(f"Battle Length: {model.battle_length}")
    print(f"Total Damage Dealt: {model.total_damage_dealt}")
    print(f"Total Damage Received: {model.total_damage_received}")
    print(f"Player Survival Count: {model.player_survival_count}")
    print(f"Enemy Survival Count: {model.enemy_survival_count}")
    metrics = model.compute_metrics()
    print("  Tension   : {:.2f} (avg. living agents per turn)".format(float(metrics['Tension'])))
    print("  Fairness  : {:.2f} (1=all players survive, 0=all enemies survive)".format(float(metrics['Fairness'])))
    print("  Engagement: {:.2f} (avg. attacks per turn)".format(float(metrics['Engagement'])))

    batch_simulation(num_runs=5, num_players=5, num_enemies=10)