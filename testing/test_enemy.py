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
