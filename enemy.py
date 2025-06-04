import numpy as np
import time  # Add this import at the top

class Enemy(object):
    def __init__ (self, loc_x, loc_y, strategy):
        self.loc = (loc_x, loc_y)
        self.strat = strategy # Attack nearest, strongest, weakest, uniform, etc.
        self.health = np.random.randint(30,60)
        self.armor_class = 10

        self.strength = 4
        self.damage_die = 8
        self.speed = 6 # number of grids not feet: 1 grid = 5 feet
        self.proficiency_bonus = 0

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
        
        # If not adjacent, move toward nearest enemy
        nearest_player = self.find_nearest_player(players)
        if not nearest_player:
            return (0,0)  # No players to attack
        
        if self.loc != nearest_player.loc:
            self.move_towards(nearest_player.loc, grid)
            
        # After moving, try to attack if now adjacent
        adj = self.adjacent_players(grid)
        if adj:
            damage = self.attack(adj[0], grid)
            return (0,damage)  # Return damage dealt
        return (0,0)

    def attack(self, player, grid):
        """
        This function simulates attacking a player.
        """
        roll_to_hit = self.roll(20, self.strength + self.proficiency_bonus)
        damage = 0

        if(roll_to_hit >= player.armor_class):
            damage = self.roll(self.damage_die, self.strength)
            if(roll_to_hit - self.strength == 20):
                damage *= 2
            player.health -= damage
            
            if player.health <= 0:
                ex, ey = player.loc
                grid[ey, ex] = None
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
                """
                Calculates the Manhattan distance between two locations.
                Inputs:
                loc1: tuple (y1, x1) representing the first location
                loc2: tuple (y2, x2) representing the second location
                Outputs:
                distance: integer Manhattan distance between loc1 and loc2
                """
                return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])
            min_dist = float('inf')
            nearest = None
            for player in players:
                dist = manhattan(self.loc, player.loc)
                if dist < min_dist:
                    min_dist = dist
                    nearest = player
            return nearest

    def move_towards(self, target_loc, grid):
        """
        Moves the enemy towards a target location.
        """
        my_y, my_x = self.loc
        target_y, target_x = target_loc
        steps = 0

        grid[my_y, my_x] = None

        while steps < self.speed:
            options = []
            for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                ny, nx = my_y + dy, my_x + dx
                if (0 <= ny < grid.shape[0]) and \
                (0 <= nx < grid.shape[1]) and \
                (grid[ny, nx] is None or grid[ny, nx] == 0):
                    new_dist = abs(ny - target_y) + abs(nx - target_x)
                    options.append((new_dist, ny, nx))

            if not options:
                break

            options.sort()
            _, ny, nx = options[0]
            my_y, my_x = ny, nx
            steps += 1

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