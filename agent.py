# import numpy as np

# class Agent:
#     def __init__(self, x, y, strategy, agent_type="player"):
#         """
#         Initialize an agent (player or enemy)
        
#         Args:
#             x (int): X coordinate
#             y (int): Y coordinate
#             behavior (str): Behavior type (e.g., "attack_nearest", "defend")
#             strategy (str): Movement/combat strategy
#             agent_type (str): Either "player" or "enemy"
#         """
#         self.loc = (x, y)
#         self.strat = strategy
#         self.type = agent_type
        
#         # Base stats shared by both types
#         self.strength = 4
#         self.damage_die = 8 if strategy == "melee" else 4
#         self.speed = 6
#         self.armor_class = 14 if agent_type == "player" else 10
#         self.proficiency_bonus = 2 if agent_type == "player" else 0
#         self.attack_range = 1 if strategy == "melee" else 12
#         self.health = np.random.randint(30, 61)  # Random health between 30-60
        
#     def roll(self, die, plus):
#         """
#         Roll a die and add a modifier
        
#         Args:
#             die (int): Size of die to roll
#             plus (int): Modifier to add
            
#         Returns:
#             int: Result of roll + modifier
#         """
#         return np.random.randint(1, die + 1) + plus
    
#     def attack(self, target, grid):
#         """
#         Attack another agent if it's a valid target
        
#         Args:
#             target (Agent): The agent being attacked
#             grid (np.array): The game grid
            
#         Returns:
#             str: Message describing the attack
#         """
#         # Check if target is valid (different type)
#         if target.type == self.type:
#             return f"{self.type.capitalize()} cannot attack same type"
            
#         damage = self.roll(self.damage_die, self.strength)
#         target.health -= damage
#         return f"{self.type.capitalize()} deals {damage} damage!"

#     def find_nearest_target(self, grid):
#         """
#         Find the nearest opposing agent
        
#         Args:
#             grid (np.array): The game grid
            
#         Returns:
#             Agent or None: Nearest opposing agent if found
#         """
#         target_type = "enemy" if self.type == "player" else "player"
#         nearest = None
#         min_dist = float('inf')
        
#         for y in range(grid.shape[0]):
#             for x in range(grid.shape[1]):
#                 if isinstance(grid[y, x], Agent) and grid[y, x].type == target_type:
#                     dist = abs(self.loc[0] - x) + abs(self.loc[1] - y)
#                     if dist < min_dist:
#                         min_dist = dist
#                         nearest = grid[y, x]
        
#         return nearest
    
#     def move_towards(self, target_loc, grid):
#         """
#         Move towards a target location
        
#         Args:
#             target_loc (tuple): (x, y) coordinates of target
#             grid (np.array): The game grid
            
#         Returns:
#             str: Message describing the movement
#         """
#         current_x, current_y = self.loc
#         target_x, target_y = target_loc
#         steps = 0

#         while steps < self.speed:
#             dx = int(np.sign(target_x - current_x))
#             dy = int(np.sign(target_y - current_y))
            
#             moved = False
#             # Try horizontal movement first
#             if dx != 0 and 0 <= current_x + dx < grid.shape[1]:
#                 if grid[current_y, current_x + dx] is None:
#                     # Clear current position
#                     grid[current_y, current_x] = None
#                     # Update coordinates
#                     current_x += dx
#                     # Place agent in new position
#                     grid[current_y, current_x] = self
#                     # Update agent's stored location
#                     self.loc = (current_x, current_y)
#                     steps += 1
#                     moved = True
        
#             # Try vertical movement if horizontal wasn't possible
#             if not moved and dy != 0 and 0 <= current_y + dy < grid.shape[0]:
#                 if grid[current_y + dy, current_x] is None:
#                     # Clear current position
#                     grid[current_y, current_x] = None
#                     # Update coordinates
#                     current_y += dy
#                     # Place agent in new position
#                     grid[current_y, current_x] = self
#                     # Update agent's stored location
#                     self.loc = (current_x, current_y)
#                     steps += 1
#                     moved = True
        
#             # If no movement was possible, break
#             if not moved:
#                 break

#         return f"{self.type.capitalize()} moved {steps} steps"
    
#     def do_action(self, grid):
#         """
#         Execute the agent's turn
        
#         Args:
#             grid (np.array): The game grid
            
#         Returns:
#             str: Message describing the action taken
#         """
#         target = self.find_nearest_target(grid)
#         if not target:
#             return f"No targets found for {self.type}"
            
#         # If adjacent to target, attack
#         if abs(self.loc[0] - target.loc[0]) + abs(self.loc[1] - target.loc[1]) <= 1:
#             return self.attack(target, grid)
#         # Otherwise move towards target
#         else:
#             return self.move_towards(target.loc, grid)

# def test_agent_movement_clears_original_position():
#     grid = np.zeros((10, 10), dtype=object)
#     agent = Agent(0, 0, "melee")
#     grid[0, 0] = agent
#     agent.move_towards((1, 0), grid)
