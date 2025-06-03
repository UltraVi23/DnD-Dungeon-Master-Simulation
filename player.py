import numpy as np

class Player(object):
    def __init__(self, loc_x, loc_y, strategy):
        self.loc = (loc_x, loc_y)

        self.strat = strategy # Melee or ranged
        self.health = np.random.randint(30,60)

        self.armor_class = 14
        self.proficiency_bonus = 2
        self.strength = 4
        if(self.strat == "melee"):
            self.damage_die = 8
            self.attack_range = 1 # distance that a melee attack can reach
        elif(self.strat == "ranged"):
            self.damage_die = 4
            self.attack_range = 12 # distance that a ranged attack can reach
        
        self.speed = 6 # number of grids not feet: 1 grid = 5 feet

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
        This function executes the player's action based on their strategy.
        Inputs:
        self: Player object
        grid: a 2D numpy array representing the game grid, where each cell can be None or an Enemy object
        Outputs:
        A string message indicating the action taken by the player
        Player object updated on the grid after the action
        """
        from enemy import Enemy
        # Find all enemies
        enemies = []
        for y in range(grid.shape[0]):
            for x in range(grid.shape[1]):
                cell = grid[y, x]
                if isinstance(cell, Enemy):
                    enemies.append(cell)
        if not enemies:
            return "No enemies to attack."

        # Try to attack first (assuming melee for now)
        adj = self.adjacent_enemies(grid)
        if adj:
            self.attack(adj[0], grid)
            # After attacking, try to move toward nearest enemy if possible (will have to update to see if this one died)
            # nearest_enemy = self.find_nearest_enemy(enemies)
            # if nearest_enemy:
            #     self.move_towards(nearest_enemy.loc, grid)
            return "Attacked an enemy, then moved towards the nearest enemy." # this can be more specific later...
        
        # If not adjacent, move toward nearest enemy
        nearest_enemy = self.find_nearest_enemy(enemies)
        if not nearest_enemy:
            return "No enemies found to move towards."
        
        if self.loc != nearest_enemy.loc:
            self.move_towards(nearest_enemy.loc, grid)
            # After moving, try to attack if now adjacent
            adj = self.adjacent_enemies(grid)
            if adj:
                self.attack(adj[0], grid)
                return "Moved towards the nearest enemy, then attacked if adjacent."
            return "Moved towards the nearest enemy, but no attack possible."
        else:
            return "Already adjacent to the nearest enemy, no movement needed."
    
    def find_nearest_enemy(self, enemies):
        """
        Finds the nearest enemy based on Manhattan distance.
        Inputs:
        self: Player object
        enemies: list of Enemy objects
        Outputs:
        nearest: the nearest Enemy object based on Manhattan distance, or None if no enemies
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
        for enemy in enemies:
            dist = manhattan(self.loc, enemy.loc)
            if dist < min_dist:
                min_dist = dist
                nearest = enemy
        return nearest

    def attack(self, enemy, grid):
        """
        This function simulates attacking an enemy, dealing damage based on the players's damage dice.
        Inputs:
        self: Player object
        enemy: an Enemy object to attack
        grid: a 2D numpy array representing the game grid, where each cell can be None or an Enemy object
        Outputs:
        damage: Damage dealt to the enemy.
        """
        # Roll to hit
        roll_to_hit = self.roll(20, self.strength + self.proficiency_bonus)
        damage = 0
        if(roll_to_hit >= enemy.armor_class):
            damage = self.roll(self.damage_die, self.strength)
            # Check for a crit, if so double the damage
            if(roll_to_hit - self.strength == 20):
                damage *= 2
            enemy.health -= damage
            # If player's health is zero, they die. Death Saves are not implemented
            if enemy.health <= 0:
                    ex, ey = enemy.loc
                    grid[ey, ex] = None
        return damage

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

        # Calculate ideal range (1 for melee, just within attack_range for ranged)
        ideal_range = 1 if self.strat == "melee" else self.attack_range - 1

        # Clear starting position
        grid[my_y, my_x] = None

        while steps < self.speed:
            current_dist = abs(my_y - target_y) + abs(my_x - target_x)
            
            # Stop if we're at ideal range
            if current_dist <= ideal_range:
                break

            options = []
            for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                ny, nx = my_y + dy, my_x + dx
                if (0 <= ny < grid.shape[0]) and \
                (0 <= nx < grid.shape[1]) and \
                (grid[ny, nx] is None or grid[ny, nx] == 0):
                    new_dist = abs(ny - target_y) + abs(nx - target_x)
                    # Only move if it gets us closer to ideal range
                    if abs(new_dist - ideal_range) < abs(current_dist - ideal_range):
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
    
    def adjacent_enemies(self, grid):
        """
        This function finds all enemies adjacent to the player.
        Inputs:
        self: Player object
        grid: a 2D numpy array representing the game grid, where each cell can be None or an Enemy object
        Outputs:
        adj: list of Enemy objects that are adjacent to the player
        """
        from enemy import Enemy
        my_y, my_x = self.loc
        adj = []
        
        # For melee, check only adjacent squares
        if self.strat == "melee":
            for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                ny, nx = my_y + dy, my_x + dx
                if 0 <= ny < grid.shape[0] and 0 <= nx < grid.shape[1]:
                    cell = grid[ny, nx]
                    if isinstance(cell, Enemy):
                        adj.append(cell)
        # For ranged, check all squares within attack range
        else:  # ranged strategy
            for y in range(grid.shape[0]):
                for x in range(grid.shape[1]):
                    dist = abs(my_y - y) + abs(my_x - x)
                    if dist <= self.attack_range:
                        cell = grid[y, x]
                        if isinstance(cell, Enemy):
                            adj.append(cell)
        
        return adj