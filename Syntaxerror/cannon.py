# cannon.py

import pygame
from bomb import Bomb  # Make sure to create the Bomb class as well

class Cannon(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((50, 50))  # Size of the cannon
        self.image.fill((255, 192, 203))  # Pink color for the cannon
        self.rect = self.image.get_rect(center=(game.settings.screen_width // 2, game.settings.screen_height // 2))
        self.x = self.rect.x
        self.y = self.rect.y
        self.attack_timer = 0  # Timer to control attack frequency
        self.health = 1000

    def update(self):
        self.attack_timer += 1  # Increment the attack timer
        if self.attack_timer >= 60:  # Attack every second (60 frames)
            self.attack_timer = 0
            self.target_enemy()

    def target_enemy(self):
        if self.game.enemies:
            # Find the closest enemy
            closest_enemy = min(self.game.enemies, key=lambda enemy: 
                (self.rect.centerx - enemy.rect.centerx) ** 2 + 
                (self.rect.centery - enemy.rect.centery) ** 2)
            bomb = Bomb(self, closest_enemy)
            self.game.bombs.add(bomb)  # Add bomb to the game
    def take_damage(self, damage):
        self.health -= damage
        print("cannon taking damage")
        if self.health <= 0:
            self.kill()
            self.game.game_over()
