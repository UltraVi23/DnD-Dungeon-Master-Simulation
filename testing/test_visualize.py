import sys
import os
import pytest
import numpy as np
import matplotlib.pyplot as plt
import visualize
from player import Player
from enemy import Enemy

# Add parent directory to path to allow importing from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_visualize_grid_creation():
    grid = np.zeros((10, 10), dtype=object)
    fig, ax = plt.subplots(figsize=(8, 8))
    visualize.visualize_grid(grid, message="Test Message", ax=ax)
    assert len(ax.images) > 0, "Grid visualization should create an image"


def test_visualize_grid_player_color():
    grid = np.zeros((10, 10), dtype=object)
    player = Player(5, 5, "melee")
    grid[5, 5] = player
    fig, ax = plt.subplots(figsize=(8, 8))
    visualize.visualize_grid(grid, message="Test Message", ax=ax)
    img_data = ax.images[0].get_array()
    assert (img_data[5, 5] > 0.5).any(), "Player position should have blue-ish color (value > 0.5)"


def test_visualize_grid_enemy_color():
    grid = np.zeros((10, 10), dtype=object)
    enemy = Enemy(5, 5, "attack_nearest")
    grid[5, 5] = enemy
    fig, ax = plt.subplots(figsize=(8, 8))
    visualize.visualize_grid(grid, message="Test Message", ax=ax)
    img_data = ax.images[0].get_array()
    assert (img_data[5, 5] > 0.5).any(), "Enemy position should have red-ish color (value > 0.5)"


def test_visualize_grid_empty_color():
    grid = np.zeros((10, 10), dtype=object)
    fig, ax = plt.subplots(figsize=(8, 8))
    visualize.visualize_grid(grid, message="Test Message", ax=ax)
    img_data = ax.images[0].get_array()
    # Check if the color values are closer to white (1.0) than colored positions
    assert (img_data[5, 5] >= 0.9).all(), "Empty position should have high color values (close to white)"


def test_visualize_grid_message_display():
    grid = np.zeros((10, 10), dtype=object)
    fig, ax = plt.subplots(figsize=(8, 8))
    test_message = "Test Message"
    visualize.visualize_grid(grid, message=test_message, ax=ax)
    assert ax.get_title() == test_message, "Grid should display the provided message as title"


def teardown_module(module):
    plt.close('all')