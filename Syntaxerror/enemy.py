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
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.terrain = game.terrain

        # Create the enemy image and rect
        self.image = pygame.image.load('assets/enemy.png').convert_alpha()  # Create enemy surface
        # self.image.fill((0, 0, 0))  # Fill it with a color, black in this case
        self.rect = self.image.get_rect()
        
        # movement settings for rendering
        self.pos = self.rect.center
        self.direction = pygame.math.Vector2(0, 0)

        # Grid and position settings
        self.start_pos = [0, 0]
        self.grid_pos = [0, 0]  # Starting grid position
        self.grid_size = self.settings.cell_size

        # Target position (the center of the screen in terms of grid)
        self.target_x = self.settings.screen_width // (self.settings.cell_size * 2)
        self.target_y = self.settings.screen_height // (self.settings.cell_size * 2)
        self.target_grid_position = [self.target_x, self.target_y]
        self.path = self.find_path()
        self.collision_rects = []
        self.speed = self.settings.enemy_speed*(1 + self.settings.difficulty_scaling*self.game.current_level)
        self.health = self.settings.enemy_health*(1 + self.settings.difficulty_scaling*self.game.current_level)
        self.attack_damage = self.settings.enemy_attack_damage*(1 + self.settings.difficulty_scaling*self.game.current_level)
        
        # attacking confiurations
        self.attacking = False
        


        
    def find_path(self):
        """Use A* pathfinding to find the path from start_pos to end_pos"""
        # Create the pathfinding grid
        
        grid = Grid(matrix=self.terrain.output_formatted_grid())
        #print(self.terrain.output_formatted_grid())
        # Get the start and end nodes
        #print(self.start_pos[0], self.start_pos[1])
        start_x, start_y = self.get_coord()
        start_node = grid.node(start_x, start_y)
        #print("end positions", self.target_grid_position[0], self.target_grid_position[1])
        end_node = grid.node(self.target_grid_position[0], self.target_grid_position[1])
        
        # Use A* algorithm to find the path
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, _ = finder.find_path(start_node, end_node, grid)
        #print('path',path)
        self.path = path
        self.create_collision_rects()
    
    def draw_path(self):
        # print(self.path)
        if self.path:
            points = []
            for point in self.path:
                if point == 0:
                    continue
                x, y = point
                points.append(((x + 0.5) * self.grid_size, (y + 0.5) * self.grid_size))
            if self.game.settings.show_path:    
                if len(points) > 1:
                    pygame.draw.lines(self.screen, (255, 0, 0), False, points, 2)
            
    def update(self):
        if not self.attacking:
            self.pos += self.direction * self.speed
            self.check_collisions()
            self.rect.center = self.pos
        
        collided_walls =pygame.sprite.spritecollide(self, self.game.walls, False)
        collided_cannons = pygame.sprite.spritecollide(self, self.game.cannons, False)
        collided_players = pygame.sprite.spritecollide(self, self.game.players, False)
        if collided_walls:
            self.attacking = True
            for wall in collided_walls:
                wall.take_damage(self.attack_damage)
                if wall.health <= 0:
                    self.attacking = False     
        elif collided_cannons:
            self.attacking = True
            for cannon in collided_cannons:
                cannon.take_damage(self.attack_damage)
                if cannon.health <= 0:
                    self.game.gameOverScreen()
                    self.attacking = False
        elif collided_players:
            self.attacking = True
            for player in collided_players:
                player.take_damage(self.attack_damage)
            
        else:
            self.attacking = False

        
        
    def take_damage(self, damage):
        self.health -= damage

        if self.health <= 0:
            self.kill()
    def get_coord(self):
        x = self.rect.centerx // self.settings.cell_size
        y = self.rect.centery // self.settings.cell_size
        return (x, y)
    
    def create_collision_rects(self):
        if self.path:
            self.collision_rects = []
            for point in self.path:
                x = (point.x + 0.5) * self.grid_size
                y = (point.y + 0.5) * self.grid_size
                rect = pygame.Rect(x - 2, y - 2, 4, 4)
                self.collision_rects.append(rect)
                
    def check_collisions(self):
        if self.collision_rects:
            for rect in self.collision_rects:
                if rect.collidepoint(self.pos):
                    del self.collision_rects[0]
                    self.get_direction()
                    
    def get_direction(self):
        if self.collision_rects:
            start = pygame.math.Vector2(self.pos)
            end = pygame.math.Vector2(self.collision_rects[0].center)
            self.direction = (end - start).normalize()
        else:
            self.direction = pygame.math.Vector2(0,0)
            self.path = [0]  