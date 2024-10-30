




class Enemy:
    def __init__(self, game):
        self.health = 50
        self.image = pygame.image.load("enemy.png")
        self.direction = 1 #corresponds to left or right
        self.speed = 5
        self.x = 0
        
    def move(self):
        if self.direction == 1:
            self.x -= self.speed # moving right
        else:
            self.x += self.speed # moving left
        
        if self.collides(wall):
            self.direction *= -1 #change direction