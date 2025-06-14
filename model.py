import numpy as np
from enemy import Enemy
from player import Player
import matplotlib.pyplot as plt
from visualize import visualize_grid

class Model(object):
    def __init__(self, num_players=5, num_enemies=10, enemy_strategy='attack_nearest', enemy_max_health=60):
        # Grid dimensions
        self.GRID_X = 100
        self.GRID_Y = 100

        # Number of players and enemies
        self.NUM_PLAYERS = num_players
        self.NUM_ENEMIES = num_enemies

        self.players_killed = 0
        self.enemies_killed = 0

        self.enemy_strategy = enemy_strategy  # Default enemy strategy
        self.enemy_max_health = enemy_max_health  # Max health for enemies
        self.grid = np.zeros((self.GRID_Y, self.GRID_X), dtype=object)

        # Initiative order
        self.initiative_order = self.roll_initiative()

        # Battle statistics
        self.battle_length = 0 # Tracks full rounds, not individual turns
        self.players_killed = 0
        self.enemies_killed = 0
        self.player_damage_dealt = 0
        self.player_damage_received = 0
        self.player_survival_count = 0
        self.enemy_survival_count = 0

        # Title message for visualization
        self.message = "D&D DM Simulation"

        # Living agents and attacks per turn
        self.turn_living_agents = []
        self.turn_attacks = []
    
    def roll_initiative(self):
        """
        This function rolls initiative for the combat, or the order in which players and enemies will attack.
        """

        initiative = []
        # Initialize grid with zeros
        self.grid = np.zeros((self.GRID_Y, self.GRID_X), dtype=object)
        
        # Place exactly NUM_PLAYERS players
        placed_players = 0
        while placed_players < self.NUM_PLAYERS:
            y = np.random.randint(0, self.GRID_Y)
            x = np.random.randint(0, self.GRID_X)
            if self.grid[y, x] == 0:  # Only place player if position is empty
                player = Player(y, x, 'melee')
                self.grid[y, x] = player  # Store the player object directly
                initiative.append(player)
                placed_players += 1
        
        # Place exactly NUM_ENEMIES enemies
        placed_enemies = 0
        while placed_enemies < self.NUM_ENEMIES:
            y = np.random.randint(0, self.GRID_Y)
            x = np.random.randint(0, self.GRID_X)
            if self.grid[y, x] == 0:  # Only place enemy if position is empty
                enemy = Enemy(y, x, self.enemy_strategy, max_health=self.enemy_max_health)
                self.grid[y, x] = enemy  # Store the enemy object directly
                initiative.append(enemy)
                placed_enemies += 1
        
        np.random.shuffle(initiative)
        return initiative

    def execute_turns(self):
        """Execute a single turn"""
        # Create a copy since we'll be modifying the list while iterating
        current_initiative = self.initiative_order.copy()
        attacks_this_turn = 0
        
        for agent in current_initiative:
            # Skip if agent is already dead
            if agent.health <= 0:
                continue
                
            dmg_dealt, dmg_recieved = agent.do_action(self.grid)
            self.player_damage_dealt += dmg_dealt
            self.player_damage_received += dmg_recieved
            if dmg_dealt > 0 or dmg_recieved > 0:
                attacks_this_turn += 1
            
            # Update stats
            if isinstance(agent, Player):
                if agent.health <= 0:
                    self.players_killed += 1
            elif isinstance(agent, Enemy):
                if agent.health <= 0:
                    self.enemies_killed += 1
    
        # Increment battle length once per full turn
        self.battle_length += 1
        
        self.turn_living_agents.append(len(self.get_all_players()) + len(self.get_all_enemies()))
        self.turn_attacks.append(attacks_this_turn)

        # Remove dead entities from initiative order
        self.initiative_order = [
            entity for entity in self.initiative_order 
            if entity.health > 0
        ]

    def compute_metrics(self):
        avg_attacks_per_turn = np.mean(self.turn_attacks) if self.turn_attacks else 0
        avg_entities_alive = np.mean(self.turn_living_agents) if self.turn_living_agents else 0
        return {
            "Total Damage Dealt by Players": self.player_damage_dealt,
            "Total Damage Dealt by Enemies": self.player_damage_received,
            "Rounds Taken": self.battle_length,
            "Avg Attacks per Turn": avg_attacks_per_turn,
            "Avg Entities Alive per Turn": avg_entities_alive,
            "Players Survived": len(self.get_all_players()),
            "Enemies Survived": len(self.get_all_enemies())
        }

    def update_grid_state(self):
        """
        Cleans up the grid by removing dead entities and updating entity counts
        """
        for y in range(self.GRID_Y):
            for x in range(self.GRID_X):
                entity = self.grid[y, x]
                if isinstance(entity, (Player, Enemy)) and entity.health <= 0:
                    self.grid[y, x] = 0  # Use 0 instead of None for numpy array

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
            visualize_grid(model.grid, message=model.message, ax=ax, pause=0.1, enemy_health=model.enemy_max_health)
        
        # Check if battle should end
        if len(model.get_all_players()) == 0:
            # print("All players defeated. Enemies win.")
            break
        if len(model.get_all_enemies()) == 0:
            # print("All enemies defeated. Players win!")
            break
    if visualize:  
        plt.close(fig)
    
def batch_simulation(num_runs=10, num_players=5, num_enemies=10, enemy_strategy='attack_nearest', enemy_max_health=60):
    results = []
    player_wins = 0
    for i in range(num_runs):
        model = Model(num_players=num_players, num_enemies=num_enemies, enemy_strategy=enemy_strategy, enemy_max_health=enemy_max_health)
        model.grid = np.zeros((model.GRID_Y, model.GRID_X), dtype=object)
        model.initiative_order = model.roll_initiative()
        show(model, visualize=False)
        metrics = model.compute_metrics()
        results.append(metrics)
        # Count as a win if at least one player survived
        if metrics["Players Survived"] > 0:
            player_wins += 1
    avg_metrics = {k: float(np.mean([m[k] for m in results])) for k in results[0]}
    win_percentage = 100 * player_wins / num_runs
    avg_metrics["Player Win %"] = win_percentage
    return avg_metrics

def experiment_varying_enemies_and_health(
    num_runs=100, 
    num_players=5, 
    enemy_numbers=[1, 3, 5, 7, 9, 11, 13], 
    enemy_strategies=['attack_nearest', 'attack_strongest', 'attack_weakest', 'attack_uniform'], 
    enemy_healths=[30, 60, 120]
):
    results = []
    for strategy in enemy_strategies:
        for health in enemy_healths:
            for num_enemies in enemy_numbers:
                print(f"Running simulation with {num_enemies} enemies, strategy: {strategy}, health: {health}")
                avg_metrics = batch_simulation(
                    num_runs=num_runs,
                    num_players=num_players,
                    num_enemies=num_enemies,
                    enemy_strategy=strategy,
                    enemy_max_health=health
                )
                results.append({
                    'strategy': strategy,
                    'health': health,
                    'num_enemies': num_enemies,
                    **avg_metrics
                })
    # Plotting
    for metric in [
    "Total Damage Dealt by Players",
    "Total Damage Dealt by Enemies",
    "Rounds Taken",
    "Avg Attacks per Turn",
    "Avg Entities Alive per Turn",
    "Players Survived",
    "Enemies Survived",
    "Player Win %"
    ]:
        plt.figure(figsize=(10, 6))
        for strategy in enemy_strategies:
            for health in enemy_healths:
                x = [r['num_enemies'] for r in results if r['strategy'] == strategy and r['health'] == health]
                y = [r[metric] for r in results if r['strategy'] == strategy and r['health'] == health]
                plt.plot(x, y, marker='o', label=f"{strategy}, HP={health}")
        plt.title(f"{metric} vs Number of Enemies")
        plt.xlabel("Number of Enemies")
        plt.ylabel(metric)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{metric.replace(' ', '_')}_vs_num_enemies.png")
        # plt.show()
        plt.close()

if __name__ == "__main__":
    # Uncomment to run the live demo
    # model = Model(num_enemies=10, enemy_max_health=60)
    # show(model)
    # metrics = model.compute_metrics()
    # for key, value in metrics.items():
    #     if isinstance(value, float):
    #         print(f"{key}: {value:.2f}")
    #     else:
    #         print(f"{key}: {value}")

    # model = Model(num_enemies=5, enemy_max_health=120)
    # show(model)
    # metrics = model.compute_metrics()
    # for key, value in metrics.items():
    #     if isinstance(value, float):
    #         print(f"{key}: {value:.2f}")
    #     else:
    #         print(f"{key}: {value}")

    # Uncomment to run a batch simulation
    # batch_simulation(num_runs=5, num_players=5, num_enemies=10)

    # Uncomment to run the experiment with varying enemies and health
    experiment_varying_enemies_and_health()