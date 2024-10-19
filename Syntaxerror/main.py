# import pygame
# import sys
# import pathfinding
# from pygame.sprite import Sprite
# from enemy import Enemy
# from settings import Settings
# from terrain import WFCTerrainGenerator
# from wall import Wall




# GREEN = (0, 255, 0)
# BLUE = (0, 0, 255)
# RED = (255, 0, 0)
# YELLOW = (255, 255, 0)

# class Game:
#     def __init__(self):
#         pygame.init()
#         self.settings = Settings()
#         self.screen = pygame.display.set_mode((
#             self.settings.screen_width,
#             self.settings.screen_height
#             ))
#         self.enemies = pygame.sprite.Group()
#         self.walls = pygame.sprite.Group()
#         self.mousedown = False
        
#         pygame.display.set_caption('Citedal Seige')
#         self.game_active = True 
#         self.terrain = WFCTerrainGenerator(
#             self.settings.screen_width//self.settings.cell_size,
#             self.settings.screen_height//self.settings.cell_size,
#             self.settings.mountain_rate, self.settings.tree_chance)
#         self.terrain.create_terrain( self.settings.clear_area_scale)
#         self.clock = pygame.time.Clock()
#         self.spawn_enemies()
        
        
#     def rungame(self):
#         while True:
#             self._check_events()
#             self._update_walls()
#             self.draw_grid()
#             self.draw_enemies()   
#             self.enemy_pathfind()
#             self.clock.tick(60)
#             pygame.display.flip()

#     def _check_events(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 sys.exit()
#             elif event.type == pygame.KEYDOWN:
#                 self._check_keydown_events(event)
#             elif event.type == pygame.KEYUP:
#                 self._check_keyup_events(event)
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 self._check_mouse_button_down_events(event)
#             elif event.type == pygame.MOUSEBUTTONUP:
#                 self._check_mouse_button_up_events(event)
    
#     def _check_keydown_events(self, event):
#         if event.key == pygame.K_ESCAPE:
#             sys.exit()
    
#     def _check_keyup_events(self, event):
#         pass
    
#     def _check_mouse_button_down_events(self, event):
#         if event.button == 1:
#             self.mousedown = True
        
    
#     def _check_mouse_button_up_events(self, event):
#         if event.button == 1:
#             self.mousedown = False
    
#     def draw_grid(self):
#         for y in range(self.terrain.height):
#             for x in range(self.terrain.width):
#                 rect = pygame.Rect(x * self.settings.cell_size, y * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size)
#                 if self.terrain.grid[y][x][0] == 0:  # Grass
#                     pygame.draw.rect(self.screen, (0,255,0), rect)
#                 elif self.terrain.grid[y][x][0] == 1:  # Water
#                     pygame.draw.rect(self.screen, (0,0,255), rect)
#                 elif self.terrain.grid[y][x][0] == 2:  # Mountain
#                     pygame.draw.rect(self.screen, (255,0,0), rect)
#                 elif self.terrain.grid[y][x][0] == 3:  # Forest
#                     pygame.draw.rect(self.screen, (255,255,0), rect)
                    
#     def _create_enemy(self, x_position, y_position):
#         enemy = Enemy(self)
#         enemy.start_pos = [x_position, y_position]

#         enemy.rect.x = enemy.start_pos[0] * self.settings.cell_size
#         enemy.rect.y = enemy.start_pos[1] * self.settings.cell_size
#         enemy.pos = enemy.rect.center
#         #print("enemy.start_pos", enemy.start_pos)
#         enemy.find_path()
#         self.enemies.add(enemy)
#         #print("enemy", enemy)
    
#     def draw_enemies(self):
#         self.enemies.update()
#         self.enemies.draw(self.screen)
#         #print(self.enemies.spritedict)
#         for enemy in self.enemies:
#             enemy.draw_path()
#     def spawn_enemies(self):
#         offset = 1
#         positions = [(0,0), (len(self.terrain.grid[0]) - 1, len(self.terrain.grid) - 1),(0, len(self.terrain.grid) - 1), (len(self.terrain.grid[0]) - 1, 0)]
#         for position in positions:
#             self._create_enemy(position[0], position[1])  
              
#     def enemy_pathfind(self):
#         for enemy in self.enemies:
#             enemy.find_path()
            
#     def _update_walls(self):
#         self.walls.update()
#         self.walls.draw(self.screen)
#         if self.mousedown:
#             self._create_new_walls()
            
#     def _create_new_walls(self):
#         mouse_x, mouse_y = pygame.mouse.get_pos()

#         # Convert mouse position to grid coordinates
#         grid_x = mouse_x // self.settings.cell_size
#         grid_y = mouse_y // self.settings.cell_size
#         if self.terrain.grid[grid_y][grid_x][0] == 0:
#             new_wall = Wall(self, grid_x, grid_y)
#             self.walls.add(new_wall)
#             # Place a wall in the grid
#             self.terrain.grid[grid_y][grid_x][0] = 4
        
            
        

# if __name__ == '__main__':
#     game = Game()
#     game.rungame()
import pygame
import sys
from pygame.sprite import Sprite
from enemy import Enemy
from settings import Settings
from terrain import WFCTerrainGenerator
from wall import Wall
from cannon import Cannon


GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
Ra =(200,4,3)

class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((
            self.settings.screen_width,
            self.settings.screen_height
        ))
        self.enemies = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.cannons = pygame.sprite.Group()
        self.mousedown = False

        pygame.display.set_caption('Citadel Siege')
        self.game_active = True 
        self.terrain = WFCTerrainGenerator(
            self.settings.screen_width//self.settings.cell_size,
            self.settings.screen_height//self.settings.cell_size,
            self.settings.mountain_rate, self.settings.tree_chance)
        self.terrain.create_terrain(self.settings.clear_area_scale)
        self.clock = pygame.time.Clock()
        self.spawn_enemies()

    def rungame(self):
        while True:
            self._check_events()
            self._update_walls()
            self.draw_grid()
            self.draw_enemies()   
            self.update_cannons()
            self.enemy_pathfind()
            #self.clock.tick(60)
            pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mouse_button_down_events(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._check_mouse_button_up_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:  # Place cannon on space key press
            self.place_cannon()

    def _check_keyup_events(self, event):
        pass

    def _check_mouse_button_down_events(self, event):
        if event.button == 1:
            self.mousedown = True

    def _check_mouse_button_up_events(self, event):
        if event.button == 1:
            self.mousedown = False

    def draw_grid(self):
        for y in range(self.terrain.height):
            for x in range(self.terrain.width):
                rect = pygame.Rect(x * self.settings.cell_size, y * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size)
                if self.terrain.grid[y][x][0] == 0:  # Grass
                    pygame.draw.rect(self.screen, (0, 255, 0), rect)
                elif self.terrain.grid[y][x][0] == 1:  # Water
                    pygame.draw.rect(self.screen, (0, 0, 255), rect)
                elif self.terrain.grid[y][x][0] == 2:  # Mountain
                    pygame.draw.rect(self.screen, (255, 0, 0), rect)
                elif self.terrain.grid[y][x][0] == 3:  # Forest
                    pygame.draw.rect(self.screen, (255, 255, 0), rect)

    def _create_enemy(self, x_position, y_position):
        enemy = Enemy(self)
        enemy.start_pos = [x_position, y_position]
        enemy.rect.x = enemy.start_pos[0] * self.settings.cell_size
        enemy.rect.y = enemy.start_pos[1] * self.settings.cell_size
        enemy.pos = enemy.rect.center
        enemy.find_path()
        self.enemies.add(enemy)

    def draw_enemies(self):
        self.enemies.update()
        self.enemies.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw_path()

    def spawn_enemies(self):
        positions = [
            (0, 0), 
            (len(self.terrain.grid[0]) - 1, len(self.terrain.grid) - 1),
            (0, len(self.terrain.grid) - 1), 
            (len(self.terrain.grid[0]) - 1, 0)
        ]
        for position in positions:
            self._create_enemy(position[0], position[1])

    def enemy_pathfind(self):
        for enemy in self.enemies:
            enemy.find_path()

    def _update_walls(self):
        self.walls.update()
        self.walls.draw(self.screen)
        if self.mousedown:
            self._create_new_walls()

    def _create_new_walls(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Convert mouse position to grid coordinates
        grid_x = mouse_x // self.settings.cell_size
        grid_y = mouse_y // self.settings.cell_size
        if self.terrain.grid[grid_y][grid_x][0] == 0:
            new_wall = Wall(self, grid_x, grid_y)
            self.walls.add(new_wall)
            # Place a wall in the grid
            self.terrain.grid[grid_y][grid_x][0] = 4
            
    def place_cannon(self):
        """Places a cannon at the mouse position when space is pressed"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x = mouse_x // self.settings.cell_size
        grid_y = mouse_y // self.settings.cell_size
        if self.terrain.grid[grid_y][grid_x][0] == 0:
            new_cannon = Cannon(self, mouse_x, mouse_y)
            self.cannons.add(new_cannon)
            # Place a wall in the grid
            self.terrain.grid[grid_y][grid_x][0] = 5
    
    def update_cannons(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.cannons.update(mouse_x, mouse_y)
        # self.cannons.draw(self.screen)
        
            
        

if __name__ == '__main__':
    game = Game()
    game.rungame()
  