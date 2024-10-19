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
        #
        
    def update(self, target_x, target_y):
        
        dx = target_x - self.x
        dy = target_y - self.y
        self.angle = math.degrees(math.atan2(-dy, dx)) - 90
        
        rect_surf = pygame.Surface((self.settings.cell_size, self.settings.cell_size), pygame.SRCALPHA)
        rect_surf.fill(self.color)
        
        rotated_surf = pygame.transform.rotate(rect_surf, self.angle)
        rotated_rect = rotated_surf.get_rect(center = (self.x,self.y))
        self.screen.blit(rotated_surf, rotated_rect)

