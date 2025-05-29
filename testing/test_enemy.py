import pytest
import sys
import os
from enemy import Enemy
import numpy as np

# Add parent directory to path to allow importing from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_roll():
    die = 20
    plus = 5
    
    result = Enemy.roll(die, plus)
    
    assert isinstance(result, int), "Roll should return an integer"
    assert result >= plus + 1 and result <= die + plus, "Roll should be within the range of 1 to die + plus"
    
def test_enemy_initialization():
    loc_x = 5
    loc_y = 10
    strategy = "attack_nearest"
    
    enemy = Enemy(loc_x, loc_y, strategy)
    
    assert enemy.loc == (loc_x, loc_y), "Enemy location should match initialization values"
    assert enemy.strat == strategy, "Enemy strategy should match initialization value"
    assert isinstance(enemy.health, int), "Enemy health should be an integer"
    assert 30 <= enemy.health <= 60, "Enemy health should be between 30 and 60"
    assert enemy.strength == 4, "Enemy strength should be initialized to 4"
    assert enemy.damage_die == 8, "Enemy damage die should be initialized to 8"
    assert enemy.speed == 6, "Enemy speed should be initialized to 6"
