class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.cell_size = 32
        self.cell_color = (255, 255, 255)
        self.player_color = (0, 0, 255)
        self.mountain_rate = 1
        self.tree_chance = 0.05
        self.clear_area_scale = 0.6
        self.enemy_speed = 1
        self.enemy_size = self.cell_size
        
        # current best settings
        # self.mountain_rate = 0.25
        # self.tree_chance = 0.05
        # self.clear_area_scale = 0.8