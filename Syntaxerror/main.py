import pygame
import sys
import pathfinding
import time
from pygame.sprite import Sprite
from enemy import Enemy
import settings_base
from terrain import WFCTerrainGenerator
from wall import Wall
from cannon import Cannon  # Import the Cannon class
from bomb import Bomb      # Import the Bomb class
from player import Player
import serial.tools.list_ports
from cannon import Cannon
from bomb import Bomb



GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)                       
WHITE = (255,255,255)

class Settings_Ard(settings_base.Settings):
    def __init__(self):
        super().__init__()
        self.enemy_speed = 1
        self.player_max_speed = 15
    
class Settings_Key(settings_base.Settings):
    def __init__(self):
        super().__init__()
        self.enemy_speed = 0.05
        self.player_max_speed = 15

class Game:
    def __init__(self):
        pygame.init()
        self.settings = settings_base.Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.enemies = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()  # Group for bombs
        self.cannons = pygame.sprite.Group()  # Group for cannons
        self.players = pygame.sprite.Group()
        self.mountains = []
        self.water = []
        self.trees = []
        self.grasses = []
        self.attackmode =  False# 0 = buildmode, 1 = attackmode
        self.mousedown = False
        self.font = pygame.font.Font(None, 50)
        self.current_level = 1
        self.player_attack = False

        pygame.display.set_caption('Citadel Siege')
        self.game_active = True 
        
        self.hs_running = True
        self.gv_running = False
        self.game_running = False
        self.use_arduino = False
        self.arduino_connected = False
        
        self.terrain = WFCTerrainGenerator(
        self.settings.screen_width // self.settings.cell_size,
        self.settings.screen_height // self.settings.cell_size,
        self.settings.mountain_rate, self.settings.tree_chance)
        self.terrain.create_terrain(self.settings.clear_area_scale)
        self.clock = pygame.time.Clock()
        self.runHomeScreen()

    def display_levels(self):
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)
        
        level_str = str(self.current_level)
        self.level_image = self.font.render(level_str, True,
            self.text_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen.get_rect().right
        self.level_rect.top = 10 + self.screen.get_rect().top
        self.screen.blit(self.level_image, self.level_rect)
    def runHomeScreen(self):
        while self.hs_running:
            self.screen.fill(YELLOW)
            button1_rect = pygame.Rect(self.settings.screen_width // 2 - 150, self.settings.screen_height // 2 - 100, 300, 70)
            button2_rect = pygame.Rect(self.settings.screen_width // 2 - 150, self.settings.screen_height // 2 + 50, 300, 70)

            # Get the mouse position
            mouse_pos = pygame.mouse.get_pos()

            # Change button colors on hover
            if button1_rect.collidepoint(mouse_pos):
                button1_color = BLUE
            else:
                button1_color = GREEN

            if button2_rect.collidepoint(mouse_pos):
                button2_color = BLUE
            else:
                button2_color = RED

            # Draw the buttons
            pygame.draw.rect(self.screen, button1_color, button1_rect)
            pygame.draw.rect(self.screen, button2_color, button2_rect)

            # Draw button text
            self.draw_text("Use Arduino", self.font, WHITE, self.screen, self.settings.screen_width // 2, self.settings.screen_height // 2 - 65)
            self.draw_text("Use Keyboard", self.font, WHITE, self.screen, self.settings.screen_width // 2, self.settings.screen_height // 2 + 85)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button1_rect.collidepoint(event.pos):
                        self.use_arduino = True
                        self.hs_running = False
                    if button2_rect.collidepoint(event.pos):
                        self.use_arduino = False
                        self.hs_running = False
                        
            pygame.display.flip()
                        
        self.screen.fill(YELLOW)
        if self.use_arduino:
            self.settings = Settings_Ard()
            
            ports = serial.tools.list_ports.comports()
            for port in ports:
                print(port)
                if 'Arduino' in port.description:
                    try:
                        self.ard = serial.Serial(port.device, 9600)
                    except Exception as e:
                        print(e)
                        print("couldn't connect to arduino")
                        sys.exit()
                    self.arduino_connected = True
                    break
                
            if not self.arduino_connected:
                print("No connected arduino found")
                sys.exit()
        else:
            
            self.settings = Settings_Key()
            self.settings.player_max_speed = 4
            self.settings.enemy_speed = 1
            
        self.spawn_player()
        self.spawn_enemies()
        self.place_cannon()  # Automatically place cannon in the center

        self.game_running = True
        self.rungame()
    def rungame(self):
        self.set_timer()
        while self.game_running:
            if not self.attackmode:
                
                self.buildmode()
                # swtiches from buildmode to attackmode
                if self.past_time()>self.settings.timer:
                    print("TIME OVER")
                    self.attackmode = True
                    self.spawn_enemies()
                    print("switched attackmode")
                    
            else:
                # swtiches from attackmode to buildmode
                self.attackmodefunc()
                if len(self.enemies)==0:
                    self.attackmode = False
                    self.set_timer()
                    self.current_level += 1
            self.display_levels()
              # Update cannons
            self.enemy_pathfind()
            pygame.display.flip()
    
    def set_timer(self):
        self.start_time = time.time()
    
    def past_time(self):
        return time.time() - self.start_time
    
    def buildmode(self):
        self._check_events()
        self.draw_grid()
        self._update_walls()
        self._update_cannons()
        # self.player.config_player_build()
        
        if self.use_arduino:
            self.move_player_arduino()
        else:
            self.move_player_keyboard()
            self.clock.tick(60)
        self.draw_player()
    def attackmodefunc(self):
        self._check_events()
        self.draw_grid()
        self._update_walls()
        self.draw_enemies()
        # self.player.config_player_attack()
        if self.use_arduino:
            self.move_player_arduino()
        else:
            self.move_player_keyboard()
            self.clock.tick(60)
        self._update_cannons()
        self._update_bombs()  # Update bombs
        self.draw_player()
        self.draw_enemies()  
            
    def draw_text(self, text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x, y))
        surface.blit(text_obj, text_rect)

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
            self.game_running = False
        elif event.key == pygame.K_SPACE:
            self.player.building = True
        elif event.key == pygame.K_f:
            self.player_attack = True

    def _check_keyup_events(self, event):
        if event.key == pygame.K_SPACE:
            self.player.building = False
        elif event.key == pygame.K_f:
            self.player_attack = False

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
                    self.grasses.append(rect)
                elif self.terrain.grid[y][x][0] == 1:  # Water
                    pygame.draw.rect(self.screen, (0, 0, 255), rect)
                    self.water.append(rect)
                elif self.terrain.grid[y][x][0] == 2:  # Mountain
                    pygame.draw.rect(self.screen, (255, 0, 0), rect)
                    self.mountains.append(rect)
                elif self.terrain.grid[y][x][0] == 3:  # Forest
                    pygame.draw.rect(self.screen, (255, 255, 0), rect)
                    self.trees.append(rect)


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
            self._create_new_walls_at_mouse()
        elif self.player.building:
            self._create_new_walls_at_player()

    def _create_new_walls_at_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x = mouse_x // self.settings.cell_size
        grid_y = mouse_y // self.settings.cell_size
        if self.terrain.grid[grid_y][grid_x][0] == 0:
            new_wall = Wall(self, grid_x, grid_y)
            self.walls.add(new_wall)
            self.terrain.grid[grid_y][grid_x][0] = 4
    
    def _create_new_walls_at_player(self):
        grid_x = self.player.rect.centerx // self.settings.cell_size
        grid_y = self.player.rect.centery // self.settings.cell_size
        if not self.attackmode:
            if self.terrain.grid[grid_y][grid_x][0] == 0:
                new_wall = Wall(self, grid_x, grid_y)
                self.walls.add(new_wall)
                self.terrain.grid[grid_y][grid_x][0] = 4

    def spawn_player(self):
        self.player = Player(self)
        self.player.rect.x = self.player.start_pos[0] * self.settings.cell_size
        self.player.rect.y = self.player.start_pos[1] * self.settings.cell_size
        self.players.add(self.player)
        self.player.draw(self.screen)
        
    def draw_player(self):
        self.player.calculate()
        self.player.update()
        self.player.draw(self.screen)
        
    
    
    def move_player_arduino(self):
        try:
            line = self.ard.readline()
            line_s = line.decode()
            splitted_line = line_s.split("||")

            x = int(splitted_line[0].strip(" ").strip("\n"))
            y = int(splitted_line[1].strip(" ").strip("\n"))
            bj = not bool(int(splitted_line[2].strip(" ").strip("\n")))
            b1 = not bool(int(splitted_line[3].strip(" ").strip("\n")))
            b2 = not bool(int(splitted_line[4].strip(" ").strip("\n")))
            b3 = not bool(int(splitted_line[5].strip(" ").strip("\n")))

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
            
            
            new_rect = pygame.Rect(self.player.rect.x+ speed_x, self.player.rect.y+speed_y, self.settings.player_size, self.settings.player_size)

            
            collision = False
            for wall in self.mountains:
                if new_rect.colliderect(wall):
                    collision = True
                    break
            for wall in self.water:
                if new_rect.colliderect(wall):
                    collision = True
                    break
                
            if not collision:
                self.player.rect.x += speed_x
                self.player.rect.y += speed_y
                
            self.player.rect.clamp_ip(self.screen.get_rect())
            self.run_button_functions(bj, b1, b2, b3)
            

        except Exception as e:
            print(e)
            


        self.draw_player()

    def run_button_functions(self, bj, b1, b2, b3):
        if b1:
            print("b1 pressed")
            self.player.building = True
        else:
            self.player.building = False
        if b2:
            print("b2 pressed")
            self.player_attack = True
        else:
            self.player_attack = False
        if b3:
            print("b3 pressed")
        if bj:
            print("bj pressed")
    
    def move_player_keyboard(self):
        
        keys = pygame.key.get_pressed()
        
        # Initialize movement vector
        movement = pygame.math.Vector2(0, 0)
        
        # Check for arrow key presses and update movement vector
        if keys[pygame.K_LEFT]:
            movement.x -= 1
        if keys[pygame.K_RIGHT]:
            movement.x += 1
        if keys[pygame.K_UP]:
            movement.y -= 1
        if keys[pygame.K_DOWN]:
            movement.y += 1
        
        # Normalize the movement vector if it's not zero
        if movement.length() > 0:
            movement = movement.normalize()
        
        # Apply movement
    
        
        new_rect = pygame.Rect(self.player.rect.x+ movement.x * self.settings.player_max_speed, self.player.rect.y+movement.y * self.settings.player_max_speed, self.settings.player_size, self.settings.player_size)

        
        collision = False
        for wall in self.mountains:
            if new_rect.colliderect(wall):
                collision = True
                break
        for wall in self.water:
            if new_rect.colliderect(wall):
                collision = True
                break
            
        if not collision:
            self.player.rect.x += movement.x * self.settings.player_max_speed
            self.player.rect.y += movement.y * self.settings.player_max_speed
            
        
        # Ensure player stays within screen bounds
        self.player.rect.clamp_ip(self.screen.get_rect())
        
    def place_cannon(self):
        cannon = Cannon(self)  # Create the cannon at the center
        self.cannons.add(cannon)

    def _update_bombs(self):
        self.bombs.update()
        self.bombs.draw(self.screen)

    def _update_cannons(self):
        self.cannons.update()
        self.cannons.draw(self.screen)

    
    def gameOverScreen(self):
        self.game_running = False
        while True:
            print('game over')
            self.screen.fill(YELLOW)
            
            # Change button colors on hover
            # Draw the buttons

            # Draw button text
            self.draw_text("Game Over", self.font, WHITE, self.screen, self.settings.screen_width // 2, self.settings.screen_height // 2 - 65)
            self.draw_text(f"Score: {self.current_level*100-100}", self.font, WHITE, self.screen, self.settings.screen_width // 2, self.settings.screen_height//2+85)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
            
            
        
if __name__ == '__main__':
    game = Game()
    
    if game.use_arduino:
        game.ard.close()
