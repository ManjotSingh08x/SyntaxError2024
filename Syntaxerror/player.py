from pygame.sprite import Sprite
import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

import pygame
from pygame.sprite import Sprite

sprite_sheet = pygame.image.load('assets\player\player.png')

class Player(Sprite):
    def __init__(self, game):
        super().__init__()
        
        self.screen = game.screen
        self.game = game
        self.settings = game.settings
        self.terrain = game.terrain
        self.building = False
        self.health = self.settings.player_health
        # movement settings for rendering

        # Create the enemy image and rect
        self.image = pygame.Surface((self.settings.player_size, self.settings.player_size))  # Create enemy surface
        self.image.fill((0, 255, 255))  # Fill it with a color, black in this case
        self.rect = self.image.get_rect()

        # Grid and position settings
        self.start_pos = [self.settings.screen_width // (self.settings.cell_size * 2), self.settings.screen_height // (self.settings.cell_size * 2)]
        self.grid_pos = [self.settings.screen_width // (self.settings.cell_size * 2), self.settings.screen_height // (self.settings.cell_size * 2)]  # Starting grid position
        self.grid_size = self.settings.cell_size
        
        
        
    def calculate(self):
        collided_enemies = pygame.sprite.spritecollide(self, self.game.enemies, False)
        for enemy in collided_enemies:
            if self.game.player_attack:
                enemy.take_damage(1)
                print("mar rha hu")
                #player attack animations

            
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    def take_damage(self, damage):
        self.health -= damage
        print(self.health)
        print("player taking damage")
        if self.health <= 0:
            self.kill()
            self.game.gameOverScreen()