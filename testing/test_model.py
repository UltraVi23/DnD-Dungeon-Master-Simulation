import pytest
import sys
import os

# Add parent directory to path to allow importing from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import Model
from player import Player
from enemy import Enemy
import numpy as np

def test_model_initialization():
    model = Model()
    
    assert model.GRID_X == 100, "GRID_X should be initialized to 100"
    assert model.GRID_Y == 100, "GRID_Y should be initialized to 100"
    
    assert model.NUM_PLAYERS == 5, "NUM_PLAYERS should be initialized to 5"
    assert model.NUM_ENEMIES == 10, "NUM_ENEMIES should be initialized to 10"
    
    assert model.grid.shape == (model.GRID_Y, model.GRID_X), "Grid shape should match GRID_Y and GRID_X"
    
    # Count players and enemies separately in the grid
    player_count = sum(1 for x in model.grid.flat if isinstance(x, Player))
    enemy_count = sum(1 for x in model.grid.flat if isinstance(x, Enemy))
    
    assert player_count == model.NUM_PLAYERS, "Grid should contain correct number of players"
    assert enemy_count == model.NUM_ENEMIES, "Grid should contain correct number of enemies"
    
    assert len(model.initiative_order) == model.NUM_PLAYERS + model.NUM_ENEMIES, "Initiative order should contain all players and enemies"
    
    for agent in model.initiative_order:
        assert hasattr(agent, 'loc'), "Each agent should have a location attribute"
        assert hasattr(agent, 'strat'), "Each agent should have a strategy attribute"
        
def test_roll_initiative():
    model = Model()
    initiative_order = model.roll_initiative()
    
    assert len(initiative_order) == model.NUM_PLAYERS + model.NUM_ENEMIES, "Initiative order should contain all players and enemies"
    
    player_count = sum(isinstance(agent, Player) for agent in initiative_order)
    enemy_count = sum(isinstance(agent, Enemy) for agent in initiative_order)
    
    assert player_count == model.NUM_PLAYERS, "Number of players in initiative order should match NUM_PLAYERS"
    assert enemy_count == model.NUM_ENEMIES, "Number of enemies in initiative order should match NUM_ENEMIES"