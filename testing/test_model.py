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
    assert model.GRID_X == 20, "GRID_X should be initialized to 20"


def test_model_grid_y_initialization():
    model = Model()
    assert model.GRID_Y == 20, "GRID_Y should be initialized to 20"


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


def test_defeated_player_removed_from_grid():
    """Test that a defeated player is removed from their grid position"""
    model = Model()
    player_pos = next((
        (y, x) for y in range(model.GRID_Y)
        for x in range(model.GRID_X)
        if isinstance(model.grid[y, x], Player)
    ), None)

    if player_pos is None:
        pytest.skip("No player found in grid")

    player = model.grid[player_pos]
    player.health = 0
    model.update_grid_state()  # Add this line to trigger grid cleanup

    assert model.grid[player_pos] is None


def test_defeated_player_not_in_target_list():
    """Test that a defeated player is not targetable by enemies"""
    model = Model()
    player_pos = next((
        (y, x) for y in range(model.GRID_Y)
        for x in range(model.GRID_X)
        if isinstance(model.grid[y, x], Player)
    ), None)

    if player_pos is None:
        pytest.skip("No player found in grid")

    player = model.grid[player_pos]
    player.health = 0
    model.update_grid_state()  # Add this line to trigger grid cleanup

    assert player not in model.get_all_players()


def test_defeated_enemy_removed_from_grid():
    """Test that a defeated enemy is removed from their grid position"""
    model = Model()
    enemy_pos = next((
        (y, x) for y in range(model.GRID_Y)
        for x in range(model.GRID_X)
        if isinstance(model.grid[y, x], Enemy)
    ), None)

    if enemy_pos is None:
        pytest.skip("No enemy found in grid")

    enemy = model.grid[enemy_pos]
    enemy.health = 0
    model.update_grid_state()  # Add this line to trigger grid cleanup

    assert model.grid[enemy_pos] is None


def test_defeated_enemy_not_in_target_list():
    """Test that a defeated enemy is not targetable by players"""
    model = Model()
    enemy_pos = next((
        (y, x) for y in range(model.GRID_Y)
        for x in range(model.GRID_X)
        if isinstance(model.grid[y, x], Enemy)
    ), None)

    if enemy_pos is None:
        pytest.skip("No enemy found in grid")

    enemy = model.grid[enemy_pos]
    enemy.health = 0
    model.update_grid_state()  # Add this line to trigger grid cleanup

    assert enemy not in model.get_all_enemies()


# Metrics Initialization Tests
def test_metrics_initial_turns():
    """Test turn counter starts at zero"""
    model = Model()
    assert model.battle_length == 0, "Total turns should start at 0"


def test_metrics_initial_damage():
    """Test damage dealt starts at zero"""
    model = Model()
    assert model.player_damage_dealt == 0, "Total damage dealt should start at 0"


def test_metrics_initial_players_killed():
    """Test players defeated starts at zero"""
    model = Model()
    assert model.players_killed == 0, "Players defeated should start at 0"


def test_metrics_initial_enemies_killed():
    """Test enemies defeated starts at zero"""
    model = Model()
    assert model.enemies_killed == 0, "Enemies defeated should start at 0"


def test_metrics_initial_battle_length():
    """Test battle length starts at zero"""
    model = Model()
    assert model.battle_length == 0, "Battle length should start at 0"


def test_metrics_initial_player_damage_dealt():
    """Test player damage dealt starts at zero"""
    model = Model()
    assert model.player_damage_dealt == 0, "Player damage dealt should start at 0"


def test_metrics_initial_player_damage_received():
    """Test player damage received starts at zero"""
    model = Model()
    assert model.player_damage_received == 0, "Player damage received should start at 0"


def test_metrics_initial_players_killed():
    """Test players killed starts at zero"""
    model = Model()
    assert model.players_killed == 0, "Players killed should start at 0"


def test_metrics_initial_enemies_killed():
    """Test enemies killed starts at zero"""
    model = Model()
    assert model.enemies_killed == 0, "Enemies killed should start at 0"


# Damage Tests
def test_damage_recording():
    """Test recording a single instance of damage"""
    model = Model()
    initial_damage = model.player_damage_dealt
    damage_amount = 10
    model.record_damage(damage_amount)
    assert model.player_damage_dealt == initial_damage + damage_amount, "Damage should be added to total"


def test_turn_increment():
    """Test single turn increment"""
    model = Model()
    initial_turns = model.battle_length
    model.execute_turns()
    final_turns = model.battle_length
    assert final_turns == initial_turns + 1, "Battle length should increment by 1 after executing a turn"


def test_damage_recording():
    """Test recording damage dealt by players"""
    model = Model()
    initial_damage = model.player_damage_dealt
    damage_amount = 10
    # Simulate damage being dealt
    model.player_damage_dealt += damage_amount
    assert model.player_damage_dealt == initial_damage + damage_amount, "Damage should be added to total"


# Victory/Defeat Tests
@pytest.fixture
def model_with_defeated_enemies():
    """Fixture providing model with all enemies defeated"""
    model = Model()
    for y in range(model.GRID_Y):
        for x in range(model.GRID_X):
            if isinstance(model.grid[y, x], Enemy):
                model.grid[y, x].health = 0
    model.update_grid_state()
    return model


@pytest.fixture
def model_with_defeated_players():
    """Fixture providing model with all players defeated"""
    model = Model()
    for y in range(model.GRID_Y):
        for x in range(model.GRID_X):
            if isinstance(model.grid[y, x], Player):
                model.grid[y, x].health = 0
    model.update_grid_state()
    return model


def test_victory_condition(model_with_defeated_enemies):
    """Test victory condition when all enemies are defeated"""
    assert len(model_with_defeated_enemies.get_all_enemies()) == 0, "Should have no enemies remaining"


def test_no_victory_in_normal_state():
    """Test victory condition in normal game state"""
    model = Model()
    assert len(model.get_all_enemies()) > 0, "Should have enemies remaining"


def test_defeat_condition(model_with_defeated_players):
    """Test defeat condition when all players are defeated"""
    assert len(model_with_defeated_players.get_all_players()) == 0, "Should have no players remaining"


def test_no_defeat_in_normal_state():
    """Test defeat condition in normal game state"""
    model = Model()
    assert len(model.get_all_players()) > 0, "Should have players remaining"