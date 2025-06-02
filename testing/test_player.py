import sys
import os
from player import Player
from enemy import Enemy
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_roll_returns_integer():
    player = Player(5, 5, "melee")
    result = player.roll(20, 5)
    assert isinstance(result, int), "Roll should return an integer"

def test_roll_within_range():
    player = Player(5, 5, "melee")
    result = player.roll(20, 5)
    assert 6 <= result <= 25, "Roll should be within range of 1 + plus to die + plus"

def test_player_location_initialization():
    player = Player(5, 10, "melee")
    assert player.loc == (5, 10), "Player location should match initialization values"

def test_player_strategy_initialization():
    player = Player(5, 10, "melee")
    assert player.strat == "melee", "Player strategy should match initialization value"

def test_player_health_is_integer():
    player = Player(5, 10, "melee")
    assert isinstance(player.health, int), "Player health should be an integer"

def test_player_health_within_range():
    player = Player(5, 10, "melee")
    assert 30 <= player.health <= 60, "Player health should be between 30 and 60"

def test_player_strength_initialization():
    player = Player(5, 10, "melee")
    assert player.strength == 4, "Player strength should be initialized to 4"

def test_player_damage_die_initialization():
    player = Player(5, 10, "melee")
    assert player.damage_die == 8, "Player damage die should be initialized to 8"

def test_player_speed_initialization():
    player = Player(5, 10, "melee")
    assert player.speed == 6, "Player speed should be initialized to 6"

def test_player_attack_returns_integer():
    player = Player(5, 5, "melee")
    enemy = Enemy(6, 5, "attack_nearest")
    grid = np.zeros((10, 10), dtype=object)
    grid[5, 5] = player
    grid[5, 6] = enemy
    message = player.attack(enemy, grid)
    assert isinstance(message, int), "Attack should return damage dealt as an integer"

def test_player_attack_reduces_enemy_health():
    player = Player(5, 5, "melee")
    enemy = Enemy(6, 5, "attack_nearest")
    initial_enemy_health = enemy.health
    grid = np.zeros((10, 10), dtype=object)
    grid[5, 5] = player
    grid[5, 6] = enemy
    damage = player.attack(enemy, grid)
    assert enemy.health == initial_enemy_health - damage, "Enemy health should be reduced by damage amount"