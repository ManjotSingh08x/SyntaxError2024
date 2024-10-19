from pygame.sprite import Sprite
import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

import pygame
from pygame.sprite import Sprite

class Player(Sprite):
    def __init__(self, game):
        super().__init__()
        
        self.screen = game.screen
        self.game = game
        self.settings = game.settings
        self.terrain = game.terrain
        self.building = False

        # Create the enemy image and rect
        self.image = pygame.Surface((self.settings.enemy_size, self.settings.enemy_size))  # Create enemy surface
        self.image.fill((0, 255, 255))  # Fill it with a color, black in this case
        self.rect = self.image.get_rect()

        # Grid and position settings
        self.start_pos = [self.settings.screen_width // (self.settings.cell_size * 2), self.settings.screen_height // (self.settings.cell_size * 2)]
        self.grid_pos = [self.settings.screen_width // (self.settings.cell_size * 2), self.settings.screen_height // (self.settings.cell_size * 2)]  # Starting grid position
        self.grid_size = self.settings.cell_size

    def draw(self, surface):
        surface.blit(self.image, self.rect)
