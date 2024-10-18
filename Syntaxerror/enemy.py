from pygame.sprite import Sprite
import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.terrain = game.terrain

        # Create the enemy image and rect
        self.image = pygame.Surface((self.settings.enemy_size, self.settings.enemy_size))  # Create enemy surface
        self.image.fill((0, 0, 0))  # Fill it with a color, black in this case
        self.rect = self.image.get_rect()

        # Grid and position settings
        self.grid_pos = [0, 0]  # Starting grid position
        self.grid_size = self.settings.cell_size

        # Target position (the center of the screen in terms of grid)
        self.target_x = self.settings.screen_width // (self.settings.cell_size * 2)
        self.target_y = self.settings.screen_height // (self.settings.cell_size * 2)
        self.target_grid_position = [self.target_x, self.target_y]

        # Pixel position for smooth movement
        self.x = float(self.grid_pos[0] * self.grid_size)
        self.y = float(self.grid_pos[1] * self.grid_size)

        # Set the initial rect position in pixels
        self.rect.topleft = (self.x, self.y)

        # Pathfinding: Find a path from start to target (returns grid positions)
        self.path = self.find_path()

        # Movement attributes
        self.current_point = 0  # Track which point in the path we're currently moving towards
        if self.path:
            self.target_point = self.path[self.current_point + 1]  # Next point in the path
            self.calculate_direction()  # Prepare direction for movement

    def calculate_direction(self):
        """Calculate the direction vector from current position to the next grid point."""
        current_pos = pygame.math.Vector2(self.rect.center)
        target_grid = pygame.math.Vector2(self.target_point)

        # Convert grid position to pixel position
        target_pos = pygame.math.Vector2(target_grid[0] * self.grid_size, target_grid[1] * self.grid_size)
        
        # Compute direction vector (normalized)
        self.direction = (target_pos - current_pos).normalize()

    def move_along_line(self):
        """Move the enemy smoothly towards the next point in the path."""
        current_pos = pygame.math.Vector2(self.rect.center)
        target_grid = pygame.math.Vector2(self.target_point)

        # Convert grid position to pixel position
        target_pos = pygame.math.Vector2(target_grid[0] * self.grid_size, target_grid[1] * self.grid_size)

        # Calculate distance to the target point
        distance = current_pos.distance_to(target_pos)

        # If close to the target point, snap to it and go to the next point
        if distance < self.settings.enemy_speed:
            self.rect.center = target_pos  # Snap to target position
            self.current_point += 1  # Go to the next point

            # If there are more points in the path, continue moving
            if self.current_point < len(self.path) - 1:
                self.target_point = self.path[self.current_point + 1]
                self.calculate_direction()  # Recalculate direction
        else:
            # Move in the direction of the next point by speed
            movement = self.direction * self.settings.enemy_speed
            self.rect.center += movement

    def update(self):
        """Update the enemy's movement."""
        self.move_along_line()

        
    def find_path(self):
        """Use A* pathfinding to find the path from start_pos to end_pos"""
        # Create the pathfinding grid
        
        grid = Grid(matrix=self.terrain.output_formatted_grid())
        
        # Get the start and end nodes
        start_node = grid.node(self.start_pos[0], self.start_pos[1])
        end_node = grid.node(self.target_grid_position[0], self.target_grid_position[1])
        
        # Use A* algorithm to find the path
        finder = AStarFinder()
        path, _ = finder.find_path(start_node, end_node, grid)
        
        return path
