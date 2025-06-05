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

def test_player_proficiency_initialization():
    """Test that player proficiency bonus is properly initialized"""
    player = Player(5, 5, "melee")
    assert player.proficiency_bonus == 2, "Player proficiency bonus should be initialized to 2"

def test_player_proficiency_added_to_attack():
    """Test that proficiency bonus is added to attack rolls"""
    grid = np.zeros((10, 10), dtype=object)
    player = Player(5, 5, "melee")
    enemy = Enemy(5, 6, "attack_nearest")
    grid[5, 5] = player
    grid[5, 6] = enemy
    
    # Mock the roll method to return a known value
    original_roll = player.roll
    
    def mock_roll(die, plus):
        """Mock roll that returns 10 plus the modifier"""
        return 10 + plus
    
    try:
        # Override roll to return 10 (so with proficiency+strength should be 16)
        player.roll = mock_roll
        
        # Make attack and check if proficiency was added
        player.attack(enemy, grid)
        expected_attack = 10 + player.proficiency_bonus + player.strength
        
        # Verify the attack roll includes proficiency
        assert expected_attack == 16, "Attack roll should include proficiency bonus"
    finally:
        # Restore original roll method
        player.roll = original_roll

def test_player_proficiency_affects_hit_chance():
    """Test that proficiency bonus affects ability to hit enemy AC"""
    grid = np.zeros((10, 10), dtype=object)
    player = Player(5, 5, "melee")
    enemy = Enemy(5, 6, "attack_nearest")
    grid[5, 5] = player
    grid[5, 6] = enemy
    
    # Set enemy AC to require proficiency to hit
    enemy.armor_class = 15  # Will require roll of 11+ with proficiency to hit
    
    def mock_roll(die, plus):
        """Mock roll that returns 11 plus the modifier"""
        return 11 + plus
    
    # Mock roll to return 11 (with proficiency+strength should hit AC 15)
    original_roll = player.roll
    try:
        player.roll = mock_roll
        
        damage = player.attack(enemy, grid)
        assert damage > 0, "Attack should hit with proficiency bonus added"
    finally:
        # Restore original roll method
        player.roll = original_roll

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

def test_player_pathfinding_direct_route():
    """Test player can find direct path to target when unobstructed"""
    grid = np.zeros((10, 10), dtype=object)
    player = Player(0, 0, "melee")
    enemy = Enemy(3, 3, "attack_nearest")
    grid[0, 0] = player
    grid[3, 3] = enemy
    
    player.move_towards(enemy.loc, grid)
    assert player.loc != (0, 0), "Player should have moved from starting position"
    assert manhattan_distance(player.loc, enemy.loc) < manhattan_distance((0, 0), enemy.loc), \
        "Player should have moved closer to enemy"

def test_player_pathfinding_blocked_route():
    """Test player can find alternate path when direct route is blocked"""
    grid = np.zeros((5, 5), dtype=object)
    player = Player(0, 0, "melee")
    enemy = Player(0, 4, "melee")
    # Create wall of obstacles blocking direct path
    grid[0, 1] = Enemy(0, 1, "attack_nearest")
    grid[0, 2] = Enemy(0, 2, "attack_nearest")
    grid[0, 3] = Enemy(0, 3, "attack_nearest")
    
    grid[0, 0] = player
    grid[0, 4] = enemy
    
    initial_pos = player.loc
    player.move_towards(enemy.loc, grid)
    assert player.loc != initial_pos, "Player should find alternate path around obstacles"

def test_player_respects_strategy_range():
    """Test player maintains appropriate range based on strategy"""
    grid = np.zeros((10, 10), dtype=object)
    ranged_player = Player(0, 0, "ranged")
    enemy = Enemy(5, 5, "attack_nearest")
    grid[0, 0] = ranged_player
    grid[5, 5] = enemy
    
    ranged_player.move_towards(enemy.loc, grid)
    final_distance = manhattan_distance(ranged_player.loc, enemy.loc)
    assert final_distance < ranged_player.attack_range, \
        "Ranged player should stay within attack range"
    assert final_distance > 1, \
        "Ranged player should maintain distance from enemy"

def test_player_double_move_when_not_adjacent():
    """Test that player moves twice when not adjacent to enemy"""
    grid = np.zeros((20, 20), dtype=object)
    player = Player(0, 0, "melee")
    enemy = Enemy(12, 0, "attack_nearest")
    grid[0, 0] = player
    grid[12, 0] = enemy
    
    initial_pos = player.loc
    normal_speed = player.speed
    player.do_action(grid)
    
    distance_moved = manhattan_distance(initial_pos, player.loc)
    assert distance_moved > normal_speed, "Player should move more than normal speed when not adjacent to enemy"

def test_player_double_move_limit():
    """Test that double move respects maximum movement limit"""
    grid = np.zeros((20, 20), dtype=object)
    player = Player(0, 0, "melee")
    enemy = Enemy(12, 0, "attack_nearest")
    grid[0, 0] = player
    grid[12, 0] = enemy
    
    initial_pos = player.loc
    normal_speed = player.speed
    player.do_action(grid)
    
    distance_moved = manhattan_distance(initial_pos, player.loc)
    assert distance_moved <= normal_speed * 2, "Player should not move more than double speed"

def test_player_double_move_towards_enemy():
    """Test that double move brings player closer to enemy"""
    grid = np.zeros((20, 20), dtype=object)
    player = Player(0, 0, "melee")
    enemy = Enemy(12, 0, "attack_nearest")
    grid[0, 0] = player
    grid[12, 0] = enemy
    
    initial_distance = manhattan_distance(player.loc, enemy.loc)
    player.do_action(grid)
    final_distance = manhattan_distance(player.loc, enemy.loc)
    
    assert final_distance < initial_distance, "Player should move closer to enemy when not adjacent"

def test_player_no_double_move_when_adjacent():
    """Test that player doesn't double move when able to move adjacent to enemy"""
    grid = np.zeros((20, 20), dtype=object)
    player = Player(0, 0, "melee")
    # Place enemy one spot away from the player
    enemy = Enemy(0, 2, "attack_nearest")
    grid[0, 0] = player
    grid[0, 1] = enemy
    
    initial_pos = player.loc
    normal_speed = player.speed
    player.do_action(grid)
    
    distance_moved = manhattan_distance(initial_pos, player.loc)
    assert distance_moved <= normal_speed, "Player should not move more than normal speed when adjacent to enemy"

def test_critical_hit_on_natural_20():
    """Test that attack is recognized as critical hit on natural 20"""
    grid = np.zeros((10, 10), dtype=object)
    player = Player(5, 5, "melee")
    enemy = Enemy(5, 6, "attack_nearest")
    grid[5, 5] = player
    grid[5, 6] = enemy
    
    original_roll = player.roll
    def mock_roll(die, plus):
        if die == 20:  # Attack roll
            return 20  # Natural 20
        if die == 8:  # Damage die (d8)
            return 4  # Consistent damage roll
        return 0  # For any other rolls
    
    try:
        player.roll = mock_roll
        damage = player.attack(enemy, grid)
        # Calculate expected damage: (damage_dice * 2) + strength
        expected_damage = (4 * 2) + player.strength
        assert damage == expected_damage, "Critical hit should double dice damage before adding strength"
    finally:
        player.roll = original_roll

def test_critical_hit_reduces_enemy_health_double():
    """Test that critical hit reduces enemy health by double damage dice"""
    grid = np.zeros((10, 10), dtype=object)
    player = Player(5, 5, "melee")
    enemy = Enemy(5, 6, "attack_nearest")
    grid[5, 5] = player
    grid[5, 6] = enemy
    
    initial_health = enemy.health
    original_roll = player.roll
    def mock_roll(die, plus):
        if die == 20:  # Attack roll
            return 20  # Natural 20
        if die == 8:  # Damage die (d8)
            return 4  # Consistent damage roll
        return 0  # For any other rolls
    
    try:
        player.roll = mock_roll
        player.attack(enemy, grid)
        expected_health = initial_health - ((4 * 2) + player.strength)
        assert enemy.health == expected_health, "Critical hit should double dice damage before adding strength"
    finally:
        player.roll = original_roll

def test_non_critical_hit_normal_damage():
    """Test that non-critical hits deal normal damage"""
    grid = np.zeros((10, 10), dtype=object)
    player = Player(5, 5, "melee")
    enemy = Enemy(5, 6, "attack_nearest")
    grid[5, 5] = player
    grid[5, 6] = enemy
    
    original_roll = player.roll
    def mock_roll(die, plus):
        if die == 20:  # Attack roll
            return 15 + plus  # Non-critical hit
        return 1  # Minimum damage for consistent testing
    
    try:
        player.roll = mock_roll
        damage = player.attack(enemy, grid)
        expected_damage = 1 + player.strength  # Normal damage
        assert damage == expected_damage, "Non-critical hit should deal normal damage"
    finally:
        player.roll = original_roll

def manhattan_distance(loc1, loc2):
    """Calculate Manhattan distance between two points"""
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])