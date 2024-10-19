import pygame
import math

class RotatingRectangle:
    def __init__(self, width, height, x, y, color):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color
        self.angle = 0  # Initial angle

    def update(self, target_x, target_y, screen):
        # Calculate the angle to rotate towards the target
        dx = target_x - self.x
        dy = target_y - self.y
        self.angle = math.degrees(math.atan2(-dy, dx)) - 90

        # Create the surface for the rectangle
        rect_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        rect_surf.fill(self.color)

        # Rotate the rectangle 
        rotated_surf = pygame.transform.rotate(rect_surf, self.angle)
        rotated_rect = rotated_surf.get_rect(center=(self.x, self.y))

        # Draw the rotated rectangle on the screen
        screen.blit(rotated_surf, rotated_rect)
