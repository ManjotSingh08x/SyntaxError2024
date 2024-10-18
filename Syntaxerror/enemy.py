from pygame.sprite import Sprite
import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

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
        self.start_pos = [0, 0]
        self.grid_pos = [0, 0]  # Starting grid position
        self.grid_size = self.settings.cell_size

        # Target position (the center of the screen in terms of grid)
        self.target_x = self.settings.screen_width // (self.settings.cell_size * 2)
        self.target_y = self.settings.screen_height // (self.settings.cell_size * 2)
        self.target_grid_position = [self.target_x, self.target_y]
        self.path = self.find_path()


        
    def find_path(self):
        """Use A* pathfinding to find the path from start_pos to end_pos"""
        # Create the pathfinding grid
        
        grid = Grid(matrix=self.terrain.output_formatted_grid())
        #print(self.terrain.output_formatted_grid())
        # Get the start and end nodes
        #print(self.start_pos[0], self.start_pos[1])
        start_node = grid.node(self.start_pos[0], self.start_pos[1])
        #print("end positions", self.target_grid_position[0], self.target_grid_position[1])
        end_node = grid.node(self.target_grid_position[0], self.target_grid_position[1])
        
        # Use A* algorithm to find the path
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, _ = finder.find_path(start_node, end_node, grid)
        #print('path',path)
        self.path = path
    
    def draw_path(self):
        # print(self.path)
        if self.path:
            points = []
            for point in self.path:
                x, y = point
                points.append(((x + 0.5) * self.grid_size, (y + 0.5) * self.grid_size))
            # print(points)
            pygame.draw.lines(self.screen, (255, 0, 0), False, points, 2)
            #print("path drawn")
