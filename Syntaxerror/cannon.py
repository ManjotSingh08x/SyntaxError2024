import pygame
import math


class Cannon(pygame.sprite.Sprite):

    def __init__(self, game, x_position, y_position):
        super().__init__()
        self.game = game
        self.settings = self.game.settings
        self.screen = game.screen
        self.x = x_position
        self.y = y_position
        self.color = self.settings.cannon_color
        self.angle = 0
        self.base_image = pygame.image.load('images/cannon-base.png').convert_alpha()
        self.base_rect = self.base_image.get_rect()
        self.base_rect.center = (self.x, self.y)
        
    def update(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        self.angle = math.degrees(math.atan2(-dy, dx)) - 90
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

