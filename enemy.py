import numpy as np
import time  # Add this import at the top

class Enemy(object):
    def __init__ (self, loc_y, loc_x, strategy, max_health=60):
        self.loc = (loc_y, loc_x)

        # Strategy for enemy: Either "attack_nearest", "attack_strongest", "attack_weakest", or "attack_uniform"
        self.strat = strategy

        # Enemy stats
        self.health = np.random.randint(max(1, max_health - 30), max_health) # Random health between 30 and 60
        self.armor_class = 10 # Number that must be rolled on attack to hit
        self.strength = 4 # Damage bonus for attacks
        self.damage_die = 8 # Damage die for attacks (d8)
        self.speed = 6 # Number of grids not feet: 1 grid = 5 feet
        self.proficiency_bonus = 0 # Proficiency bonus for attacks - Enemies have no proficiency by default

    def roll(self, die, plus):
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
        """
        This function processes and executes the enemy's action based on their strategy.
        """
        from player import Player
        # Find all players
        players = []
        for y in range(grid.shape[0]):
            for x in range(grid.shape[1]):
                cell = grid[y, x]
                if isinstance(cell, Player):
                    players.append(cell)
        if not players:
            return (0,0)  # No players to attack

        # Try to attack first
        adj = self.adjacent_players(grid)
        if adj:
            damage = self.attack(adj[0], grid)
            return (0,damage)  # Return damage dealt

        # If not adjacent, move toward target enemy
        if self.strat == 'attack_nearest':
            target_player = self.find_nearest_player(players)
        elif self.strat == 'attack_strongest':
            target_player = max(players, key=lambda p: p.health, default=None)
        elif self.strat == 'attack_weakest':
            target_player = min(players, key=lambda p: p.health, default=None)
        elif self.strat == 'attack_uniform':
            target_player = np.random.choice(players) if players else None

        if not target_player:
            return (0,0)  # No players to attack
        
        if self.loc != target_player.loc:
            self.move_towards(target_player.loc, grid)
            
        # After moving, try to attack if now adjacent
        adj = self.adjacent_players(grid)
        if adj:
            damage = self.attack(adj[0], grid)
            return (0,damage)  # Return damage dealt
        return (0,0)

    def attack(self, player, grid):
        """
        This function simulates attacking an enemy, dealing damage based on the player's damage dice.
        Returns the amount of damage dealt.
        """
        # Get the raw d20 roll before modifiers
        raw_roll = self.roll(20, 0)
        attack_roll = raw_roll + self.strength + self.proficiency_bonus
        damage = 0
        
        # Check if attack hits (either meets AC or is natural 20)
        is_critical = raw_roll == 20
        if is_critical or attack_roll >= player.armor_class:
            # Roll base damage
            damage_roll = self.roll(self.damage_die, 0)
            
            # On critical hit, double the damage roll (not the modifier)
            if is_critical:
                damage = (damage_roll * 2) + self.strength
            else:
                damage = damage_roll + self.strength
                
            # Apply damage to enemy
            player.health -= damage
            
        return damage

    def find_nearest_player(self, players):
        """
        Finds the nearest player based on Manhattan distance.
        Inputs:
        self: Enemy object
        players: list of Player objects
        Outputs:
        nearest: the nearest Player object based on Manhattan distance, or None if no players
        """
        def manhattan(loc1, loc2):
            return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])
            
        min_dist = float('inf')
        nearest = None
        for player in players:
            # Changed condition: Only skip if player is actually dead or has no location
            if player.health > 0 and player.loc is not None:
                dist = manhattan(self.loc, player.loc)
                if dist < min_dist:
                    min_dist = dist
                    nearest = player
        return nearest

    def move_towards(self, target_loc, grid):
        """
        Moves the enemy towards a target location using BFS pathfinding.
        If the preferred path is blocked, it will find alternative routes.
        """
        my_y, my_x = self.loc
        original_y, original_x = my_y, my_x  # Save original position
        target_y, target_x = target_loc

        # Remove self from current position
        grid[my_y, my_x] = None

        # Use BFS to find path
        def find_path():
            queue = [(my_y, my_x, [])]
            visited = set()
            
            while queue:
                curr_y, curr_x, path = queue.pop(0)
                
                if (curr_y, curr_x) == (target_y, target_x):
                    return path
                    
                if (curr_y, curr_x) not in visited:
                    visited.add((curr_y, curr_x))
                    
                    # Check all adjacent squares
                    for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                        ny, nx = curr_y + dy, curr_x + dx
                        
                        # Check if position is valid and unoccupied
                        if (0 <= ny < grid.shape[0]) and \
                           (0 <= nx < grid.shape[1]) and \
                           (grid[ny, nx] is None or grid[ny, nx] == 0 or (ny, nx) == target_loc):
                            new_path = path + [(ny, nx)]
                            queue.append((ny, nx, new_path))
            
            return []  # Return empty path if no valid path found

        # Find the best path
        path = find_path()
        if path:
            # Move along the path up to speed limit
            for step in range(min(self.speed, len(path))):
                my_y, my_x = path[step]
        else:
            # If no path found, return to original position
            my_y, my_x = original_y, original_x

        # Update enemy position
        self.loc = (my_y, my_x)
        grid[my_y, my_x] = self

    def adjacent_players(self, grid):
        """
        Returns a list of adjacent Player objects.
        Inputs:
        self: Enemy object
        grid: numpy array representing the game grid
        Outputs:
        adjacent: list of Player objects that are adjacent to this enemy
        """
        from player import Player
        adjacent = []
        my_y, my_x = self.loc
        
        # Check all adjacent squares
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = my_y + dy, my_x + dx
            
            # Check if position is within grid bounds
            if (0 <= ny < grid.shape[0]) and (0 <= nx < grid.shape[1]):
                cell = grid[ny, nx]
                if isinstance(cell, Player):
                    adjacent.append(cell)
        
        return adjacent