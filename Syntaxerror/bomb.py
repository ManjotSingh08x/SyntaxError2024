# bomb.py

import pygame

class Bomb(pygame.sprite.Sprite):
    def __init__(self, cannon, enemy):
        super().__init__()
        self.game = cannon.game
        self.enemy = enemy
        self.image = pygame.Surface((10, 10))  # Size of the bomb
        self.image.fill((255, 0, 0))  # Color of the bomb
        self.rect = self.image.get_rect(center=cannon.rect.center)
        self.target_pos = self.enemy.rect.center
        self.speed = 5
        self.damage = 1
        self.direction = self._calculate_direction()

    def _calculate_direction(self):
        current_pos = pygame.math.Vector2(self.rect.center)
        target_pos = pygame.math.Vector2(self.target_pos)
        direction = target_pos - current_pos
        
        if direction.length() == 0:
            # If the bullet is at the target position, return a default direction
            # or potentially signal that the bullet should be removed
            return pygame.math.Vector2(0, 1)  # Default downward direction
        else:
            return direction.normalize()

    def update(self):
        # Move the bomb
        movement = self.direction * self.speed
        self.rect.move_ip(movement)
    
        # Check for collision with any enemy
        collided_enemies = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if collided_enemies:
            # Hit an enemy
            enemy = collided_enemies[0]  # Get the first collided enemy
            enemy.take_damage(self.damage)  # Assuming bombs have a damage attribute
            self.kill()  # Remove the bomb
        else:
            # Update target position and direction if no collision occurred
            self.target_pos = self.enemy.rect.center
            self._calculate_direction()
            
        if (self.rect.right < 0 or self.rect.left > self.game.settings.screen_width or
            self.rect.bottom < 0 or self.rect.top > self.game.settings.screen_height):
            self.kill()
