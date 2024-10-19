# bomb.py

import pygame

class Bomb(pygame.sprite.Sprite):
    def __init__(self, cannon, target_pos):
        super().__init__()
        self.image = pygame.Surface((10, 10))  # Size of the bomb
        self.image.fill((255, 0, 0))  # Color of the bomb
        self.rect = self.image.get_rect(center=cannon.rect.center)
        self.target_pos = target_pos
        self.speed = 5
        self.direction = self._calculate_direction()

    def _calculate_direction(self):
        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery
        distance = (dx**2 + dy**2) ** 0.5
        return (dx / distance, dy / distance)

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        # Check if bomb has reached the target
        if self.rect.collidepoint(self.target_pos):
            self.kill()  # Remove bomb when it reaches the target
            # Here, you can add logic to deal damage to the enemy
