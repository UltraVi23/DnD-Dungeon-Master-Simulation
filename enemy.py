import numpy as np

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
        Inputs:
        self: Enemy object
        grid: a 2D numpy array representing the game grid, where each cell can be None or an Enemy object
        Outputs:
        A string message indicating the action taken by the enemy
        Enemy object updated on the grid after the action
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
            return "No players to attack."

        # Try to attack first (assuming nearest player for now)
        adj = self.adjacent_players(grid)
        if adj:
            self.attack(adj[0], grid)
            return "Attacked a player, then moved towards the nearest player." # this can be more specific later...
        
        # If not adjacent, move toward nearest enemy
        nearest_player = self.find_nearest_player(players)
        if not nearest_player:
            return "No players found to move towards."
        
        if self.loc != nearest_player.loc:
            self.move_towards(nearest_player.loc, grid)
            # After moving, try to attack if now adjacent
            adj = self.adjacent_players(grid)
            if adj:
                self.attack(adj[0], grid)
                return "Moved towards the nearest player, then attacked if adjacent."
            return "Moved towards the nearest player, but no attack possible."
        else:
            return "Already adjacent to the nearest player, no movement needed."

    def attack(self, player, grid):
        """
        This function simulates attacking an player, dealing damage based on the enemy's damage dice.
        Inputs:
        self: Enemy object
        player: Player object to be attacked
        grid: a 2D numpy array representing the game grid, where each cell can be None or an Enemy object
        Outputs:
        None, but updates the enemy's health and removes it from the grid if defeated
        """
        # Roll to hit
        roll_to_hit = self.roll(20, self.strength + self.proficiency_bonus)
        damage = 0
        if(roll_to_hit >= player.armor_class):
            damage = self.roll(self.damage_die, self.strength)
            # Check for a crit, if so double the damage
            if(roll_to_hit - self.strength == 20):
                damage *= 2
            player.health -= damage
            # If player's health is zero, they die. Death Saves are not implemented
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
        Moves the player towards a target location on the grid, avoiding obstacles.
        Inputs:
        self: Player object
        target_loc: tuple (x, y) representing the target location to move towards
        grid: a 2D numpy array representing the game grid, where each cell can be None or an Enemy object
        Outputs:
        None, but updates the player's location on the grid
        """
        my_y, my_x = self.loc
        target_y, target_x = target_loc
        steps = 0

        # Clear starting position
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

        # Update final position
        self.loc = (my_y, my_x)
        grid[my_y, my_x] = self

    def adjacent_players(self, grid):
        """
        This function finds all enemies adjacent to the player.
        Inputs:
        self: Player object
        grid: a 2D numpy array representing the game grid, where each cell can be None or an Enemy object
        Outputs:
        adj: list of Enemy objects that are adjacent to the player
        """
        from player import Player
        my_y, my_x = self.loc
        adj = []
        
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = my_y + dy, my_x + dx
            if 0 <= ny < grid.shape[0] and 0 <= nx < grid.shape[1]:
                cell = grid[ny, nx]
                if isinstance(cell, Player):
                    adj.append(cell)        
        return adj