import pytest
import sys
import os
import numpy as np
from model import Model
from player import Player
from enemy import Enemy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_model_grid_x_initialization():
    model = Model()
    assert model.GRID_X == 100, "GRID_X should be initialized to 100"


def test_model_grid_y_initialization():
    model = Model()
    assert model.GRID_Y == 100, "GRID_Y should be initialized to 100"


def test_model_num_players_initialization():
    model = Model()
    assert model.NUM_PLAYERS == 5, "NUM_PLAYERS should be initialized to 5"


def test_model_num_enemies_initialization():
    model = Model()
    assert model.NUM_ENEMIES == 10, "NUM_ENEMIES should be initialized to 10"


def test_model_grid_shape():
    model = Model()
    assert model.grid.shape == (model.GRID_Y, model.GRID_X), "Grid shape should match GRID_Y and GRID_X"


def test_model_player_count():
    model = Model()
    player_count = sum(1 for x in model.grid.flat if isinstance(x, Player))
    assert player_count == model.NUM_PLAYERS, "Grid should contain correct number of players"


def test_model_enemy_count():
    model = Model()
    enemy_count = sum(1 for x in model.grid.flat if isinstance(x, Enemy))
    assert enemy_count == model.NUM_ENEMIES, "Grid should contain correct number of enemies"


def test_defeated_player_removed_from_grid():
    """Test that a defeated player is removed from their grid position"""
    model = Model()
    player_pos = next((
        (y, x) for y in range(model.GRID_Y)
        for x in range(model.GRID_X)
        if isinstance(model.grid[y, x], Player)
    ), None)

    if player_pos is None:
        pytest.skip("No player found in grid")

    player = model.grid[player_pos]
    player.health = 0
    model.update_grid_state()  # Add this line to trigger grid cleanup

    assert model.grid[player_pos] is None


def test_defeated_player_not_in_target_list():
    """Test that a defeated player is not targetable by enemies"""
    model = Model()
    player_pos = next((
        (y, x) for y in range(model.GRID_Y)
        for x in range(model.GRID_X)
        if isinstance(model.grid[y, x], Player)
    ), None)

    if player_pos is None:
        pytest.skip("No player found in grid")

    player = model.grid[player_pos]
    player.health = 0
    model.update_grid_state()  # Add this line to trigger grid cleanup

    assert player not in model.get_all_players()


def test_defeated_enemy_removed_from_grid():
    """Test that a defeated enemy is removed from their grid position"""
    model = Model()
    enemy_pos = next((
        (y, x) for y in range(model.GRID_Y)
        for x in range(model.GRID_X)
        if isinstance(model.grid[y, x], Enemy)
    ), None)

    if enemy_pos is None:
        pytest.skip("No enemy found in grid")

    enemy = model.grid[enemy_pos]
    enemy.health = 0
    model.update_grid_state()  # Add this line to trigger grid cleanup

    assert model.grid[enemy_pos] is None


def test_defeated_enemy_not_in_target_list():
    """Test that a defeated enemy is not targetable by players"""
    model = Model()
    enemy_pos = next((
        (y, x) for y in range(model.GRID_Y)
        for x in range(model.GRID_X)
        if isinstance(model.grid[y, x], Enemy)
    ), None)

    if enemy_pos is None:
        pytest.skip("No enemy found in grid")

    enemy = model.grid[enemy_pos]
    enemy.health = 0
    model.update_grid_state()  # Add this line to trigger grid cleanup

    assert enemy not in model.get_all_enemies()