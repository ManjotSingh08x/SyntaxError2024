import pygame
import sys
import pathfinding
from pygame.sprite import Sprite
from enemy import Enemy
from settings import Settings
from terrain import WFCTerrainGenerator


GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((
            self.settings.screen_width,
            self.settings.screen_height
            ))
        self.enemies = pygame.sprite.Group()
        
        pygame.display.set_caption('Citedal Seige')
        self.game_active = True 
        self.terrain = WFCTerrainGenerator(
            self.settings.screen_width//self.settings.cell_size,
            self.settings.screen_height//self.settings.cell_size,
            self.settings.mountain_rate, self.settings.tree_chance)
        self.terrain.create_terrain( self.settings.clear_area_scale)
        self.clock = pygame.time.Clock()
        self.spawn_enemies()
        
        
    def rungame(self):
        while True:
            self._check_events()
            self.draw_grid()
            self.draw_enemies()   
            #self.enemy_pathfind()
            self.clock.tick(60)
            pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
    
    def draw_grid(self):
        for y in range(self.terrain.height):
            for x in range(self.terrain.width):
                rect = pygame.Rect(x * self.settings.cell_size, y * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size)
                if self.terrain.grid[y][x][0] == 0:  # Grass
                    pygame.draw.rect(self.screen, (0,255,0), rect)
                elif self.terrain.grid[y][x][0] == 1:  # Water
                    pygame.draw.rect(self.screen, (0,0,255), rect)
                elif self.terrain.grid[y][x][0] == 2:  # Mountain
                    pygame.draw.rect(self.screen, (255,0,0), rect)
                elif self.terrain.grid[y][x][0] == 3:  # Forest
                    pygame.draw.rect(self.screen, (255,255,0), rect)
                    
    def _create_enemy(self, x_position, y_position):
        enemy = Enemy(self)
        enemy.start_pos = [x_position, y_position]

        enemy.rect.x = enemy.start_pos[0] * self.settings.cell_size
        enemy.rect.y = enemy.start_pos[1] * self.settings.cell_size
        #print("enemy.start_pos", enemy.start_pos)
        enemy.find_path()
        self.enemies.add(enemy)
        #print("enemy", enemy)
    
    def draw_enemies(self):
        self.enemies.update()
        self.enemies.draw(self.screen)
        #print(self.enemies.spritedict)
        for enemy in self.enemies:
            enemy.draw_path()
    def spawn_enemies(self):
        offset = 1
        positions = [(0,0), (len(self.terrain.grid[0]) - 1, len(self.terrain.grid) - 1),(0, len(self.terrain.grid) - 1), (len(self.terrain.grid[0]) - 1, 0)]
        for position in positions:
            self._create_enemy(position[0], position[1])  
    
    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move_next()
            
    def enemy_pathfind(self):
        for enemy in self.enemies:
            enemy.find_path()
            
        

if __name__ == '__main__':
    game = Game()
    game.rungame()
    

