from pygame.sprite import Sprite
import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

import pygame
from pygame.sprite import Sprite

# sprite_sheet = pygame.image.load('assets\player\player.png')

class Player(Sprite):
    def __init__(self, game):
        super().__init__()
        
        self.screen = game.screen
        self.game = game
        self.settings = game.settings
        self.terrain = game.terrain
        self.building = False
        self.health = self.settings.player_health
        self.moving = False
        # movement settings for rendering
        frame_width = 192 
        frame_height = 192 
        rows = 8 
        columns = 6 

        # spritesheet_image_player = pygame.image.load("assets/factions/player/knight/Warrior_Blue.png").convert_alpha()
        
        # self.frames_player = self.load_spritesheet(spritesheet_image_player, frame_width, frame_height, rows, columns)
        # self.mod_frames_player = []
        # for frame in self.frames_player:
        #     self.mod_frames_player.append(pygame.transform.scale(frame, (50, 50)))


        # self.walking_player = self.mod_frames_player[0:6]
        # self.jumping_player = self.mod_frames_player[6:12]
        # self.swording_player = self.mod_frames_player[12:18]
    

        # Create the enemy image and rect
        self.image = pygame.image.load(r"assets\player.png")
        self.rect = self.image.get_rect()

        # Grid and position settings
        self.start_pos = [self.settings.screen_width // (self.settings.cell_size * 2), self.settings.screen_height // (self.settings.cell_size * 2)-1]
        self.grid_pos = [self.settings.screen_width // (self.settings.cell_size * 2), self.settings.screen_height // (self.settings.cell_size * 2)-1]  # Starting grid position
        self.grid_size = self.settings.cell_size
        
        
        
    def calculate(self):
        collided_enemies = pygame.sprite.spritecollide(self, self.game.enemies, False)
        for enemy in collided_enemies:
            if self.game.player_attack:
                enemy.take_damage(1)
                
    
                #player attack animations

            
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            self.game.gameOverScreen()
    
    def load_spritesheet(self, spritesheet, frame_width, frame_height, rows, columns):
        frames = []
        for row in range(rows):
            for col in range(columns):
                # Calculate the position of each frame in the spritesheet
                x = col * frame_width
                y = row * frame_height
                # Extract the frame
                frame = spritesheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
                frames.append(frame)
        return frames
    