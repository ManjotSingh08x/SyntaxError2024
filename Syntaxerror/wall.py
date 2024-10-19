import pygame
from pygame.sprite import Sprite

class Wall(Sprite):
    def __init__(self, game, x_position, y_position): 
        super().__init__()
        self.screen = game.screen
        self.game = game
        self.settings = self.game.settings
        self.health = self.settings.wall_health
        self.x = x_position
        self.y = y_position
        self.settings = game.settings
        self.image = pygame.Surface((self.settings.enemy_size, self.settings.enemy_size))  # Create enemy surface
        self.image.fill((150, 75, 0))  # Fill it with a color, black in this case
        self.rect = self.image.get_rect()

        self.rect.x = x_position * self.settings.cell_size
        self.rect.y = y_position * self.settings.cell_size

    
    def draw(self, screen):
        pygame.draw.rect(self.screen, (0,0,0), self.rect)
        
    def take_damage(self, damage):
        self.health -= damage
        print("wall taking damage")
        if self.health <= 0:
            self.game.terrain.grid[self.y][self.x][0] = 0
            self.kill()
        