import pytest
import sys
import os
from enemy import Enemy
from player import Player
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_enemy_roll_returns_integer():
    enemy = Enemy(0, 0, "attack_nearest")
    result = enemy.roll(20, 5)
    assert isinstance(result, int), "Roll should return an integer"


def test_enemy_roll_within_range():
    enemy = Enemy(0, 0, "attack_nearest")
    result = enemy.roll(20, 5)
    assert 6 <= result <= 25, "Roll should be within range of 1 + plus to die + plus"


def test_enemy_location_initialization():
    enemy = Enemy(5, 10, "attack_nearest")
    assert enemy.loc == (5, 10), "Enemy location should match initialization values"


def test_enemy_strategy_initialization():
    enemy = Enemy(5, 10, "attack_nearest")
    assert enemy.strat == "attack_nearest", "Enemy strategy should match initialization value"


def test_enemy_health_is_integer():
    enemy = Enemy(5, 10, "attack_nearest")
    assert isinstance(enemy.health, int), "Enemy health should be an integer"


def test_enemy_health_within_range():
    enemy = Enemy(5, 10, "attack_nearest")
    assert 30 <= enemy.health <= 60, "Enemy health should be between 30 and 60"


def test_enemy_strength_initialization():
    enemy = Enemy(5, 10, "attack_nearest")
    assert enemy.strength == 4, "Enemy strength should be initialized to 4"


def test_enemy_damage_die_initialization():
    enemy = Enemy(5, 10, "attack_nearest")
    assert enemy.damage_die == 8, "Enemy damage die should be initialized to 8"


def test_enemy_speed_initialization():
    enemy = Enemy(5, 10, "attack_nearest")
    assert enemy.speed == 6, "Enemy speed should be initialized to 6"


def test_enemy_attack_returns_integer():
    enemy = Enemy(6, 5, "attack_nearest")
    player = Player(5, 5, "melee")
    grid = np.zeros((10, 10), dtype=object)
    grid[5, 5] = player
    grid[5, 6] = enemy
    message = enemy.attack(player, grid)
    assert isinstance(message, int), "Attack should return damage dealt as an integer"


def test_enemy_attack_reduces_player_health():
    enemy = Enemy(6, 5, "attack_nearest")
    player = Player(5, 5, "melee")
    initial_player_health = player.health
    grid = np.zeros((10, 10), dtype=object)
    grid[5, 5] = player
    grid[5, 6] = enemy
    damage = enemy.attack(player, grid)
    assert player.health == initial_player_health - damage, "Player health should be reduced by damage amount"


def test_enemy_pathfinding_direct_route():
    """Test enemy can find direct path to target when unobstructed"""
    grid = np.zeros((10, 10), dtype=object)
    enemy = Enemy(0, 0, "attack_nearest")
    player = Player(3, 3, "melee")
    grid[0, 0] = enemy
    grid[3, 3] = player
    
    enemy.move_towards(player.loc, grid)
    assert enemy.loc != (0, 0), "Enemy should have moved from starting position"
    assert manhattan_distance(enemy.loc, player.loc) < manhattan_distance((0, 0), player.loc), \
        "Enemy should have moved closer to player"


def test_enemy_pathfinding_blocked_route():
    """Test enemy can find alternate path when direct route is blocked"""
    grid = np.zeros((5, 5), dtype=object)
    enemy = Enemy(0, 0, "attack_nearest")
    player = Player(0, 4, "melee")
    # Create wall of enemies blocking direct path
    blocking_enemy1 = Enemy(0, 1, "attack_nearest")
    blocking_enemy2 = Enemy(0, 2, "attack_nearest")
    blocking_enemy3 = Enemy(0, 3, "attack_nearest")
    
    grid[0, 0] = enemy
    grid[0, 4] = player
    grid[0, 1] = blocking_enemy1
    grid[0, 2] = blocking_enemy2
    grid[0, 3] = blocking_enemy3
    
    initial_pos = enemy.loc
    enemy.move_towards(player.loc, grid)
    assert enemy.loc != initial_pos, "Enemy should find alternate path around obstacles"
    assert manhattan_distance(enemy.loc, player.loc) < manhattan_distance(initial_pos, player.loc), \
        "Enemy should have moved closer to player despite obstacles"


def test_enemy_respects_speed_limit():
    """Test enemy movement is limited by speed attribute"""
    grid = np.zeros((10, 10), dtype=object)
    enemy = Enemy(0, 0, "attack_nearest")
    player = Player(9, 9, "melee")
    enemy.speed = 3  # Set speed limit
    
    grid[0, 0] = enemy
    grid[9, 9] = player
    
    initial_pos = enemy.loc
    enemy.move_towards(player.loc, grid)
    
    assert manhattan_distance(enemy.loc, initial_pos) <= enemy.speed, \
        f"Enemy moved {manhattan_distance(enemy.loc, initial_pos)} spaces but speed limit is {enemy.speed}"


def test_enemy_handles_unreachable_target():
    """Test enemy behavior when target is completely unreachable"""
    grid = np.zeros((5, 5), dtype=object)
    enemy = Enemy(0, 0, "attack_nearest")
    player = Player(4, 4, "melee")
    # Create wall of enemies blocking all possible paths
    for i in range(5):
        for j in range(5):
            if (i, j) != (0, 0) and (i, j) != (4, 4):
                grid[i, j] = Enemy(i, j, "attack_nearest")
    
    grid[0, 0] = enemy
    grid[4, 4] = player
    
    initial_pos = enemy.loc
    enemy.move_towards(player.loc, grid)
    assert enemy.loc == initial_pos, "Enemy should stay in place when target is unreachable"


# Helper function for the tests
def manhattan_distance(loc1, loc2):
    """Calculate Manhattan distance between two points"""
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])
