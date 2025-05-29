import numpy as np
from enemy import Enemy

class Player(object):
    def __init__(self, loc_x, loc_y, strategy):
        self.loc = (loc_x, loc_y)
        self.strat = strategy # Melee or ranged
        self.health = np.random.randint(30,60)
        self.strength = 4
        self.damage_die = 8
        self.speed = 6 # number of grids not feet: 1 grid = 5 feet

    def roll(die, plus):
        return np.random.randint(1, die) + plus

    def do_action(self, grid):
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
            nearest_enemy = self.find_nearest_enemy(enemies)
            if nearest_enemy:
                self.move_towards(nearest_enemy.loc, grid)
            return "Attacked an enemy, then moved towards the nearest enemy." # this can be more specific later...
        
        # If not adjacent, move toward nearest enemy
        nearest_enemy = self.find_nearest_enemy(enemies)
        if nearest_enemy:
            self.move_towards(nearest_enemy.loc, grid)
        # After moving, try to attack if now adjacent
        adj = self.adjacent_enemies(grid)
        if adj:
            self.attack(adj[0], grid)
            return "Moved towards the nearest enemy, then attacked if adjacent."
        else:
            return "Moved towards the nearest enemy, but no attack possible."
    
    def find_nearest_enemy(self, enemies):
        def manhattan(loc1, loc2):
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
        damage = self.roll(self.damage_die, self.strength)
        enemy.health -= damage
        if enemy.health <= 0:
            ex, ey = enemy.loc
            grid[ey, ex] = None

    def move_towards(self, target_loc, grid):
        my_x, my_y = self.loc
        target_x, target_y = target_loc
        steps = 0

        while steps < self.speed and (my_x, my_y) != (target_x, target_y):
            options = []
            # Check all four directions
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = my_x + dx, my_y + dy
                if (0 <= nx < grid.shape[1]) and (0 <= ny < grid.shape[0]) and grid[ny, nx] is None:
                    dist = abs(nx - target_x) + abs(ny - target_y)
                    options.append((dist, nx, ny))
            if not options:
                break  # Blocked

            # Choose the move that gets closest to the target
            options.sort()
            _, new_x, new_y = options[0]
            grid[my_y, my_x] = None
            self.loc = (new_x, new_y)
            grid[new_x, new_y] = self
            steps += 1

    def adjacent_enemies(self, grid):
        my_x, my_y = self.loc
        adj = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = my_x + dx, my_y + dy
            if 0 <= nx < grid.shape[1] and 0 <= ny < grid.shape[0]:
                cell = grid[ny, nx]
                if isinstance(cell, Enemy):
                    adj.append(cell)
        return adj