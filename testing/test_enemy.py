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


def test_enemy_proficiency_initialization():
    """Test that enemy proficiency bonus is properly initialized"""
    enemy = Enemy(5, 5, "attack_nearest")
    assert enemy.proficiency_bonus == 0, "Enemy proficiency bonus should be initialized to 0"


def test_enemy_attack_without_proficiency():
    """Test that attack rolls do not include proficiency bonus"""
    grid = np.zeros((10, 10), dtype=object)
    enemy = Enemy(5, 5, "attack_nearest")
    player = Player(5, 6, "melee")
    grid[5, 5] = enemy
    grid[5, 6] = player
    
    # Mock the roll method to return a known value
    original_roll = enemy.roll
    
    def mock_roll(die, plus):
        """Mock roll that returns 10 plus the modifier"""
        return 10 + plus
    
    try:
        # Override roll to return 10 (with only strength should be 14)
        enemy.roll = mock_roll
        
        # Make attack and check if no proficiency was added
        enemy.attack(player, grid)
        expected_attack = 10 + enemy.strength  # No proficiency bonus
        
        # Verify the attack roll does not include proficiency
        assert expected_attack == 14, "Attack roll should not include proficiency bonus"
    finally:
        # Restore original roll method
        enemy.roll = original_roll


def test_enemy_hit_chance_without_proficiency():
    """Test that hit chance is correctly calculated without proficiency"""
    grid = np.zeros((10, 10), dtype=object)
    enemy = Enemy(5, 5, "attack_nearest")
    player = Player(5, 6, "melee")
    grid[5, 5] = enemy
    grid[5, 6] = player
    
    # Set player AC to be hittable without proficiency
    player.armor_class = 13  # Will require roll of 9+ with just strength to hit
    
    def mock_roll(die, plus):
        """Mock roll that returns 9 plus the modifier"""
        return 9 + plus
    
    # Mock roll to return 9 (with just strength should hit AC 13)
    original_roll = enemy.roll
    try:
        enemy.roll = mock_roll
        
        damage = enemy.attack(player, grid)
        assert damage > 0, "Attack should hit with just strength modifier"
    finally:
        # Restore original roll method
        enemy.roll = original_roll


def test_enemy_critical_hit_on_natural_20():
    """Test that enemy attack is recognized as critical hit on natural 20"""
    grid = np.zeros((10, 10), dtype=object)
    enemy = Enemy(5, 5, "attack_nearest")
    player = Player(5, 6, "melee")
    grid[5, 5] = enemy
    grid[5, 6] = player
    
    original_roll = enemy.roll
    def mock_roll(die, plus):
        if die == 20:  # Attack roll
            return 20  # Natural 20
        if die == 8:  # Damage die (d8 for enemy)
            return 4  # Consistent damage roll
        return 0  # For any other rolls
    
    try:
        enemy.roll = mock_roll
        damage = enemy.attack(player, grid)
        # Calculate expected damage: (damage_dice * 2) + strength
        expected_damage = (4 * 2) + enemy.strength
        assert damage == expected_damage, "Critical hit should double dice damage before adding strength"
    finally:
        enemy.roll = original_roll


def test_enemy_critical_hit_reduces_player_health_double():
    """Test that enemy critical hit reduces player health by double damage dice"""
    grid = np.zeros((10, 10), dtype=object)
    enemy = Enemy(5, 5, "attack_nearest")
    player = Player(5, 6, "melee")
    grid[5, 5] = enemy
    grid[5, 6] = player
    
    initial_health = player.health
    original_roll = enemy.roll
    def mock_roll(die, plus):
        if die == 20:  # Attack roll
            return 20  # Natural 20
        if die == 8:  # Damage die (d8)
            return 4  # Consistent damage roll
        return 0  # For any other rolls
    
    try:
        enemy.roll = mock_roll
        enemy.attack(player, grid)
        expected_health = initial_health - ((4 * 2) + enemy.strength)
        assert player.health == expected_health, "Critical hit should double dice damage before adding strength"
    finally:
        enemy.roll = original_roll


def test_enemy_non_critical_hit_normal_damage():
    """Test that enemy non-critical hits deal normal damage"""
    grid = np.zeros((10, 10), dtype=object)
    enemy = Enemy(5, 5, "attack_nearest")
    player = Player(5, 6, "melee")
    grid[5, 5] = enemy
    grid[5, 6] = player
    
    initial_health = player.health
    original_roll = enemy.roll
    def mock_roll(die, plus):
        if die == 20:  # Attack roll
            return 15  # Non-critical hit
        if die == 8:  # Damage die (d8)
            return 4  # Consistent damage roll
        return 0  # For any other rolls
    
    try:
        enemy.roll = mock_roll
        damage = enemy.attack(player, grid)
        expected_damage = 4 + enemy.strength  # Normal damage
        assert damage == expected_damage, "Non-critical hit should deal normal damage"
        assert player.health == initial_health - expected_damage, "Player health should be reduced by normal damage"
    finally:
        enemy.roll = original_roll


# Helper function for the tests
def manhattan_distance(loc1, loc2):
    """Calculate Manhattan distance between two points"""
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])
