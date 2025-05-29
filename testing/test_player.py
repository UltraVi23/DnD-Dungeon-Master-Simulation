import sys
import os
from player import Player
import numpy as np

# Add parent directory to path to allow importing from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def test_roll():
    die = 20
    plus = 5
    
    result = Player.roll(die, plus)
    
    assert isinstance(result, int), "Roll should return an integer"
    assert result >= plus + 1 and result <= die + plus, "Roll should be within the range of 1 to die + plus"
    
def test_player_initialization():
    loc_x = 5
    loc_y = 10
    strategy = "melee"
    
    player = Player(loc_x, loc_y, strategy)
    
    assert player.loc == (loc_x, loc_y), "Player location should match initialization values"
    assert player.strat == strategy, "Player strategy should match initialization value"
    assert isinstance(player.health, int), "Player health should be an integer"
    assert 30 <= player.health <= 60, "Player health should be between 30 and 60"
    assert player.strength == 4, "Player strength should be initialized to 4"
    assert player.damage_die == 8, "Player damage die should be initialized to 8"
    assert player.speed == 6, "Player speed should be initialized to 6"