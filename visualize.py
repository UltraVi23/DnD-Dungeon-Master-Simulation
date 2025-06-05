import matplotlib.pyplot as plt
import numpy as np
from enemy import Enemy
from player import Player

def visualize_grid(grid, message = "", ax = None, pause = 0.5, enemy_health=60):
    """
    Visualizes the game grid with players and enemies, updating the display with a message.
    Inputs:
    grid: a 2D numpy array representing the game grid, where each cell can be None, Player, or Enemy
    message: a string message to display on the grid
    ax: a matplotlib Axes object to draw the grid on; if None, uses the current Axes
    Outputs:
    None, but visualizes the grid and updates it in real-time.
    """
    if ax is None:
        ax = plt.gca()
    ax.clear()
    ax.set_xticks([])
    ax.set_yticks([])

    color_grid = np.zeros(grid.shape + (3,))  # RGB
    pmax_health = 60  # Adjust as needed
    emax_health = enemy_health  # Adjust as needed
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            cell = grid[y, x]
            # Checking both isinstance and class name for extra safety
            if isinstance(cell, Player) or (hasattr(cell, '__class__') and cell.__class__.__name__ == 'Player'):
                # Blue fades to white as health drops
                health_ratio = max(cell.health, 0) / pmax_health
                color_grid[y, x] = [1-health_ratio, 1-health_ratio, 1]  # White to blue
            elif isinstance(cell, Enemy) or (hasattr(cell, '__class__') and cell.__class__.__name__ == 'Enemy'):
                # Red fades to white as health drops
                health_ratio = max(cell.health, 0) / emax_health
                color_grid[y, x] = [1, 1-health_ratio, 1-health_ratio]  # White to red
            else:
                color_grid[y, x] = [0.92, 0.92, 0.92]  # Light gray for empty cells

    ax.imshow(color_grid, origin="lower")
    ax.set_title(message, fontsize=12, color="black", pad=20)
    plt.tight_layout()
    plt.pause(pause)