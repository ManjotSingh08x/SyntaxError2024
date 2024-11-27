class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.cell_size = 32
        self.cell_color = (255, 255, 255)
        self.player_color = (0, 0, 255)
        self.mountain_rate = 0.25
        self.tree_chance = 0.1
        self.clear_area_scale = 0.6
        self.wall_health = 500
        self.enemy_damage = 1
        self.enemy_health = 3
        self.player_size = 20
        self.cannon_color = (0,0,0)
        self.cannon_size = self.cell_size
        self.enemy_size = self.cell_size
        self.timer = 20
        self.player_health = 1000
        self.cannon_health = 2500
        self.difficulty_scaling = 0.5
        self.enemy_attack_damage = 1.1
        self.walls_left = 25
        self.show_path = True
        
        # current best settings
        # self.mountain_rate = 0.25
        # self.tree_chance = 0.05
        # self.clear_area_scale = 0.8