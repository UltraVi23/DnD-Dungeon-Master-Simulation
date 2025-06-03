import pytest
import numpy as np
import sys
import os
from agent import Agent

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_agent_location_initialization():
    agent = Agent(5, 10, "melee")
    assert agent.loc == (5, 10), "Agent location should match initialization values"

def test_agent_strategy_initialization():
    agent = Agent(5, 10, "melee")
    assert agent.strat == "melee", "Agent strategy should match initialization value"

def test_agent_type_default_initialization():
    agent = Agent(5, 10, "melee")
    assert agent.type == "player", "Agent type should default to player"

def test_agent_type_enemy_initialization():
    agent = Agent(5, 10, "melee", agent_type="enemy")
    assert agent.type == "enemy", "Agent type should be enemy when specified"

def test_agent_health_is_integer():
    agent = Agent(5, 10, "melee")
    assert isinstance(agent.health, int), "Agent health should be an integer"

def test_agent_health_within_range():
    agent = Agent(5, 10, "melee")
    assert 30 <= agent.health <= 60, "Agent health should be between 30 and 60"

def test_agent_strength_initialization():
    agent = Agent(5, 10, "melee")
    assert agent.strength == 4, "Agent strength should be initialized to 4"

def test_agent_damage_die_initialization():
    agent = Agent(5, 10, "melee")
    assert agent.damage_die == 8, "Agent damage die should be initialized to 8"

def test_agent_speed_initialization():
    agent = Agent(5, 10, "melee")
    assert agent.speed == 6, "Agent speed should be initialized to 6"

def test_agent_roll_returns_integer():
    agent = Agent(5, 5, "melee")
    result = agent.roll(20, 5)
    assert isinstance(result, int), "Roll should return an integer"

def test_agent_roll_within_range():
    agent = Agent(5, 5, "melee")
    result = agent.roll(20, 5)
    assert 6 <= result <= 25, "Roll should be within range of 1 + plus to die + plus"

def test_agent_attack_reduces_target_health():
    attacker = Agent(5, 5, "melee")
    target = Agent(6, 5, "melee", agent_type="enemy")
    initial_health = target.health
    grid = np.zeros((10, 10), dtype=object)
    attacker.attack(target, grid)
    assert target.health < initial_health, "Target health should be reduced after attack"

def test_agent_find_nearest_target_returns_closest():
    grid = np.zeros((10, 10), dtype=object)
    agent = Agent(5, 5, "melee")
    target1 = Agent(6, 5, "melee", agent_type="enemy")
    target2 = Agent(8, 8, "melee", agent_type="enemy")
    
    grid[5, 5] = agent
    grid[5, 6] = target1
    grid[8, 8] = target2
    
    nearest = agent.find_nearest_target(grid)
    assert nearest == target1, "Should find the closest target"

def test_agent_prevent_stacking():
    grid = np.zeros((10, 10), dtype=object)
    agent1 = Agent(5, 5, "melee")
    agent2 = Agent(6, 5, "melee")
    
    grid[5, 5] = agent1
    grid[5, 6] = agent2
    
    agent1.move_towards((6, 5), grid)
    assert grid[5, 5] == agent1, "Agent should remain in original position when blocked"

def test_agent_movement_within_speed():
    grid = np.zeros((10, 10), dtype=object)
    agent = Agent(0, 0, "melee")
    grid[0, 0] = agent
    
    agent.move_towards((10, 10), grid)
    current_x, current_y = agent.loc
    total_movement = abs(current_x) + abs(current_y)
    assert total_movement <= agent.speed, "Agent should not move more than speed allows"

def test_agent_movement_clears_original_position():
    grid = np.zeros((10, 10), dtype=object)
    agent = Agent(0, 0, "melee")
    grid[0, 0] = agent
    agent.move_towards((1, 0), grid)
    assert grid[0, 0] is None, "Original position should be empty after movement"

def test_agent_movement_updates_new_position():
    grid = np.zeros((10, 10), dtype=object)
    agent = Agent(0, 0, "melee")
    grid[0, 0] = agent
    agent.move_towards((1, 0), grid)
    assert grid[0, 1] == agent, "New position should contain the agent"

def test_player_attacks_enemy():
    grid = np.zeros((10, 10), dtype=object)
    player = Agent(5, 5, "melee", agent_type="player")
    enemy = Agent(5, 6, "melee", agent_type="enemy")
    grid[5, 5] = player
    grid[5, 6] = enemy
    initial_health = enemy.health
    player.attack(enemy, grid)
    assert enemy.health < initial_health, "Player should be able to damage enemy"

def test_enemy_attacks_player():
    grid = np.zeros((10, 10), dtype=object)
    enemy = Agent(5, 5, "melee", agent_type="enemy")
    player = Agent(5, 6, "melee", agent_type="player")
    grid[5, 5] = enemy
    grid[5, 6] = player
    initial_health = player.health
    enemy.attack(player, grid)
    assert player.health < initial_health, "Enemy should be able to damage player"

def test_player_cannot_attack_player():
    grid = np.zeros((10, 10), dtype=object)
    player1 = Agent(5, 5, "melee", agent_type="player")
    player2 = Agent(5, 6, "melee", agent_type="player")
    grid[5, 5] = player1
    grid[5, 6] = player2
    initial_health = player2.health
    player1.attack(player2, grid)
    assert player2.health == initial_health, "Player should not be able to damage another player"

def test_enemy_cannot_attack_enemy():
    grid = np.zeros((10, 10), dtype=object)
    enemy1 = Agent(5, 5, "melee", agent_type="enemy")
    enemy2 = Agent(5, 6, "melee", agent_type="enemy")
    grid[5, 5] = enemy1
    grid[5, 6] = enemy2
    initial_health = enemy2.health
    enemy1.attack(enemy2, grid)
    assert enemy2.health == initial_health, "Enemy should not be able to damage another enemy"

def test_player_finds_only_enemy_targets():
    grid = np.zeros((10, 10), dtype=object)
    player = Agent(5, 5, "melee", agent_type="player")
    other_player = Agent(5, 6, "melee", agent_type="player")
    enemy = Agent(5, 7, "melee", agent_type="enemy")
    grid[5, 5] = player
    grid[5, 6] = other_player
    grid[5, 7] = enemy
    target = player.find_nearest_target(grid)
    assert target == enemy, "Player should only target enemies"

def test_enemy_finds_only_player_targets():
    grid = np.zeros((10, 10), dtype=object)
    enemy = Agent(5, 5, "melee", agent_type="enemy")
    other_enemy = Agent(5, 6, "melee", agent_type="enemy")
    player = Agent(5, 7, "melee", agent_type="player")
    grid[5, 5] = enemy
    grid[5, 6] = other_enemy
    grid[5, 7] = player
    target = enemy.find_nearest_target(grid)
    assert target == player, "Enemy should only target players"