from pygame.sprite import Sprite
import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class Enemy(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.terrain = game.terrain



        self.image = pygame.Surface((self.settings.enemy_size, self.settings.enemy_size))  # Creates a simple 50x50 surface for the enemy
        self.image.fill((0, 0, 0))  # Fill it with a color, red in this case
        
        # Define the rect attribute to position the sprite
        self.rect = self.image.get_rect()
        # self.rect.topleft = (x, y)  # Set initial position
        
        
        self.start_pos = [0,0]
        self.grid_pos = self.start_pos
        self.grid_size = self.settings.cell_size
        self.target_x = self.settings.screen_width//(self.settings.cell_size*2)
        self.target_y = self.settings.screen_height//(self.settings.cell_size*2)
        self.target_grid_position = [self.target_x, self.target_y]
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.path = self.find_path()
        

        
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

    def update(self):
        """Move along the path"""
        if self.path:
            # Move to the next position in the path
            next_pos = self.path[0]
            self.position = next_pos
            
            # Update the rectangle position
            self.rect.x = self.position[0] * self.grid_size
            self.rect.y = self.position[1] * self.grid_size
            
            # Remove the current position from the path
            self.path.pop(0)
        
        
    