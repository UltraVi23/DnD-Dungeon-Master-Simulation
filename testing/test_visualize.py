import sys
import os
import pytest
import numpy as np
import matplotlib.pyplot as plt
import visualize
from player import Player
from enemy import Enemy

# Add parent directory to path to allow importing from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_visualize_grid():
    # Create a mock grid with players and enemies
    grid_size = (10, 10) # Small grid for testing
    grid = np.zeros(grid_size, dtype=object)

    # Create proper mock classes that inherit from the actual classes
    class MockPlayer(Player):
        def __init__(self):
            self.loc = None
            self.health = 50
            self.strength = 5
            self.damage_die = 6
            self.strat = 'melee'

    class MockEnemy(Enemy):
        def __init__(self):
            self.loc = None
            self.health = 40
            self.strength = 4
            self.damage_die = 8
            self.strat = 'attack_nearest'

    # Add players
    player_positions = [(i, i) for i in range(3)]
    for i, pos in enumerate(player_positions):
        player = MockPlayer()
        player.loc = pos
        grid[pos[1], pos[0]] = player

    # Add enemies
    enemy_positions = [(i + 5, i + 5) for i in range(3)]
    for i, pos in enumerate(enemy_positions):
        enemy = MockEnemy()
        enemy.loc = pos
        grid[pos[1], pos[0]] = enemy

    # Create a figure and axis for visualization
    fig, ax = plt.subplots(figsize=(8, 8))

    # Call the visualize_grid function
    visualize.visualize_grid(grid, message="Test Message", ax=ax)

    # Get the image data from the plot
    img_data = ax.images[0].get_array()

    # Verify player positions (should be value 1/blue)
    for pos in player_positions:
        assert img_data[pos[1], pos[0]] == 1, f"Player at position {pos} should be rendered as blue (value 1)"

    # Verify enemy positions (should be value 2/red)
    for pos in enemy_positions:
        assert img_data[pos[1], pos[0]] == 2, f"Enemy at position {pos} should be rendered as red (value 2)"

    # Verify empty spaces (should be value 0/white)
    empty_count = np.sum(img_data == 0)
    expected_empty = grid_size[0] * grid_size[1] - len(player_positions) - len(enemy_positions)
    assert empty_count == expected_empty, "Number of empty (white) cells is incorrect"

    # Check if the plot was created successfully
    assert ax.get_title() == "Test Message", "Title should match the provided message"
    
    plt.close(fig)  # Close the figure after testing