import matplotlib.pyplot as plt
import numpy as np
from enemy import Enemy
from player import Player

def visualize_grid(grid, message="", ax=None):
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

    color_grid = np.zeros(grid.shape)
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            cell = grid[y, x]
            # Checking both isinstance and class name for extra safety
            if isinstance(cell, Player) or (hasattr(cell, '__class__') and cell.__class__.__name__ == 'Player'):
                color_grid[y, x] = 1
            elif isinstance(cell, Enemy) or (hasattr(cell, '__class__') and cell.__class__.__name__ == 'Enemy'):
                color_grid[y, x] = 2

    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(["white", "blue", "red"]) # white for empty, blue for Player, red for Enemy
    ax.imshow(color_grid, cmap=cmap, origin="lower")
    ax.set_title(message, fontsize=12, color="black", pad=20)
    plt.tight_layout()
    plt.pause(0.5)