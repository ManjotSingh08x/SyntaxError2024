import pygame

class Wall(Sprite):
    def __init__(self, x_position, y_position): 
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x_position
        self.rect.y = y_position
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)