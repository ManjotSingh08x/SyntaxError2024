import pygame
import sys
import pathfinding
import serial
from pygame.sprite import Sprite
from enemy import Enemy
from settings import Settings
from terrain import WFCTerrainGenerator
from wall import Wall
<<<<<<< HEAD
from cannon import Cannon  # Import the Cannon class
from bomb import Bomb      # Import the Bomb class
=======
from player import Player
import serial.tools.list_ports
from cannon import Cannon
from bomb import Bomb


>>>>>>> 1eeebb61e7e93512018c9fee76df55d6816d0784

GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.enemies = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
<<<<<<< HEAD
        self.bombs = pygame.sprite.Group()  # Group for bombs
        self.cannons = pygame.sprite.Group()  # Group for cannons
=======
        self.cannons = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
>>>>>>> 1eeebb61e7e93512018c9fee76df55d6816d0784
        self.mousedown = False

        pygame.display.set_caption('Citadel Siege')
        self.game_active = True 
        self.terrain = WFCTerrainGenerator(
            self.settings.screen_width // self.settings.cell_size,
            self.settings.screen_height // self.settings.cell_size,
            self.settings.mountain_rate, self.settings.tree_chance)
        self.terrain.create_terrain(self.settings.clear_area_scale)
        self.clock = pygame.time.Clock()
        self.spawn_enemies()
<<<<<<< HEAD
        self.place_cannon()  # Automatically place cannon in the center
=======
        # self.set_controller_port()
        self.spawn_player()
        self.arduino_connected = False
        ports = serial.tools.list_ports.comports()
        poorts = [port.device for port in ports]
        self.place_cannon()

    # List available ports
        
        print("Available Serial Ports:")
        for port in poorts:
            print(port)

        # Check connection for each available port
        for port in poorts:
            if self.check_arduino_connection(port):
                print("checked arduino connected")
                self.arduino_connected = True
                self.set_controller_port()
                break  # Exit loop if connection is successful

>>>>>>> 1eeebb61e7e93512018c9fee76df55d6816d0784

    def rungame(self):
        while True:
            self._check_events()
            self.draw_grid()
<<<<<<< HEAD
            self.draw_enemies()
            self._update_walls()
            self._update_bombs()  # Update bombs
            self._update_cannons()  # Update cannons
=======
            if self.arduino_connected:
                self.move_player_arduino()
            else:
                self.move_player_keyboard()
            self._update_bombs()  # Update bombs
            self._update_cannons()  # Update cannons
            self.draw_player()
            self.draw_enemies()   

>>>>>>> 1eeebb61e7e93512018c9fee76df55d6816d0784
            self.enemy_pathfind()
            self.clock.tick(60)
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
        grid_x = mouse_x // self.settings.cell_size
        grid_y = mouse_y // self.settings.cell_size
        if self.terrain.grid[grid_y][grid_x][0] == 0:
            new_wall = Wall(self, grid_x, grid_y)
            self.walls.add(new_wall)
            self.terrain.grid[grid_y][grid_x][0] = 4
<<<<<<< HEAD

=======
            

        
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
            print("entered contoller port try block")
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
                print("entered win32 contoller port try block")
                try:
                    print('1')
                    self.ard = serial.Serial("COM5", 9600)
                except:
                    try:
                        print(2)
                        self.ard = serial.Serial("COM4", 9600)
                        print(self.ard)
                    except:
                        print(2.5)
                        try:
                            print(3)
                            self.ard = serial.Serial("COM3", 9600)
                        except Exception as e:
                            print("error")
                            print(e)
                            self.arduino_connected = False
        except Exception as e:
            print("reached end error")
            print(e)
            self.arduino_connected = False
            
    def check_arduino_connection(self, port_name):
        try:
            # Attempt to open the specified serial port
            with serial.Serial(port_name, baudrate=9600, timeout=1) as ser:
                print(f"Connected to Arduino on {port_name}")
                return True
        except serial.SerialException as e:
            print(f"Failed to connect to Arduino on {port_name}: {e}")
            return False
        
            
    def move_player_arduino(self):
        try:
            line = self.ard.readline()
            line_s = line.decode()
            splitted_line = line_s.split("||")

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
            
            self.run_button_functions(bj, b1, b2, b3)

        except Exception as e:
            print(e)
            


        self.draw_player()

    def run_button_functions(self, bj, b1, b2, b3):
        pass
    
    def move_player_keyboard(self):
        keys = pygame.key.get_pressed()
        print(keys)
        
>>>>>>> 1eeebb61e7e93512018c9fee76df55d6816d0784
    def place_cannon(self):
        cannon = Cannon(self)  # Create the cannon at the center
        self.cannons.add(cannon)

    def _update_bombs(self):
        self.bombs.update()
        self.bombs.draw(self.screen)

    def _update_cannons(self):
        self.cannons.update()
        self.cannons.draw(self.screen)
<<<<<<< HEAD
=======
        
    def game_over(self):
        #sys.exit()
        pass
        
            
        
>>>>>>> 1eeebb61e7e93512018c9fee76df55d6816d0784

if __name__ == '__main__':
    game = Game()
    game.rungame()
