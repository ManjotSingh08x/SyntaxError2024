import pygame
import sys
import pathfinding
import serial
from pygame.sprite import Sprite
from enemy import Enemy
from player import Player
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
        # self.clock = pygame.time.Clock()
        self.set_controller_port()
        self.spawn_enemies()
        self.spawn_player()
        self.arduino_connected = True
        
        
        
    def rungame(self):
        while True:
            self._check_events()
            self.draw_grid()
            if self.arduino_connected:
                self.move_player_arduino()
            else:
                self.move_player_keyboard()
            self.draw_enemies()
            self.draw_player()   

            pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                    
    def _check_keydown_events(self, event):
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:  # Place cannon on space key press
            self.place_cannon()
        else:
            self.move_player_keyboard(event.key)

    def _check_keyup_events(self, event):
        pass
    
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
            
    def spawn_player(self):
        self.player = Player(self)
        self.player.rect.x = self.player.start_pos[0] * self.settings.cell_size
        self.player.rect.y = self.player.start_pos[1] * self.settings.cell_size
        # self.player.draw(self.screen)
        
    def draw_player(self):
        self.player.update()
        self.player.draw(self.screen)
        
    def set_controller_port(self):
        try:
            if sys.platform == 'linux':
                try:
                    self.ard = serial.Serial("/dev/ttyACM0", 9600)


                except:
                    try:
                        self.ard = serial.Serial("/dev/ttyACM1", 9600)

                    except Exception as e:
                        print(e)
                        self.arduino_connected = False
            elif sys.platform == 'win32':
                try:
                    self.ard = serial.Serial("COM5", 9600)
                except:
                    try:
                        self.ard = serial.Serial("COM4", 9600)
                    except:
                        try:
                            self.ard = serial.Serial("COM3", 9600)
                        except Exception as e:
                            print(e)
                            self.arduino_connected = False
        except Exception as e:
            print(e)
            self.arduino_connected = False
            
    def move_player_arduino(self):
        try:
            line = self.ard.readline()
            line_s = line.decode()
            splitted_line = line_s.split("||")
            print(line)
            x = int(splitted_line[0].strip(" ").strip("\n"))
            y = int(splitted_line[1].strip(" ").strip("\n"))
            bj = bool(int(splitted_line[2].strip(" ").strip("\n")))
            b1 = bool(int(splitted_line[3].strip(" ").strip("\n")))
            b2 = bool(int(splitted_line[4].strip(" ").strip("\n")))
            b3 = bool(int(splitted_line[5].strip(" ").strip("\n")))

            x_default = 504
            y_default = 513
            x_max = 1023
            y_max = 1023
            
            del_x = (x-x_default)/(x_max-x_default)
            del_y = (y-y_default)/(y_max-y_default)
            
            # print(del_y)
            if abs(del_x)<0.02:
                del_x = 0
                
            if abs(del_y)<0.02:
                del_y = 0
            
            max_speed_x = self.settings.player_max_speed
            max_speed_y = self.settings.player_max_speed
        
            speed_x = del_x*max_speed_x
            speed_y = del_y*max_speed_y
            
            self.player.rect.x += speed_x
            self.player.rect.y += speed_y
            
            self.run_button_functions(bj, b1, b2. b3)

        except Exception as e:
            print(e)
            
        self.draw_player()
    
    def run_button_functions(self, bj, b1, b2, b3):
        pass
    
    def move_player_keyboard(self):
        keys = pygame.key.get_pressed()
        print(keys)
        # if keys[pygame.K_LEFT]:
        #     self.player.rect.x -= self.settings.player_speed
        # if keys[pygame.K_RIGHT]:
        #     self.player.rect.x += self.settings.player_speed
        # if keys[pygame.K_UP]:
        #     self.player.rect.y -= self.settings.player_speed
        # if keys[pygame.K_DOWN]:
        #     self.player.rect.y += self.settings.player_speed
        
        

if __name__ == '__main__':
    game = Game()
    game.rungame()
    

