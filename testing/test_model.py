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