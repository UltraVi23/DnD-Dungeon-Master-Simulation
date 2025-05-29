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
        # choose an action to do (move, attack)
        # update grid

        # for movement go somewhere based on chosen action, move up till max movement if possible
        pass

    def attack(self, player, grid):
        """
        This function simulates attacking an player, dealing damage based on the enemy's damage dice.
        Inputs:
        self: Player object
        enemy: an Enemy object to attack
        grid: a 2D numpy array representing the game grid, where each cell can be None or an Enemy object
        Outputs:
        None, but updates the enemy's health and removes it from the grid if defeated
        """
        # Roll to hit
        roll_to_hit = self.roll(20, self.strength)
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