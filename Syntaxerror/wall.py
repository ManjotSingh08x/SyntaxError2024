import pygame
from pygame.sprite import Sprite

class Wall(Sprite):
    def __init__(self, game, x_position, y_position): 
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pygame.Surface((self.settings.enemy_size, self.settings.enemy_size))  # Create enemy surface
        self.image.fill((0, 0, 0))  # Fill it with a color, black in this case
        self.rect = self.image.get_rect()

        self.rect.x = x_position * self.settings.cell_size
        self.rect.y = y_position * self.settings.cell_size

    
    def draw(self, screen):
        pygame.draw.rect(self.screen, (0,0,0), self.rect)
        