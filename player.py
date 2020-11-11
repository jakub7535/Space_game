import pygame

# every object on the screen
class Space_Objects:
    def __init__(self, x=0, y=0, size=50, path_assets="assets/car/", img="battleship.png", sound="explosion.wav"):
        self.x = x 
        self.y = y
        self.size = size
        self.path_assets = path_assets
        self.img = pygame.image.load(path_assets + img)
        self.img = pygame.transform.scale(self.img, (self.size, self.size))  
        self.sound = pygame.mixer.Sound(path_assets + sound) 
        
    def detect_collision(self, other):
        if (other.x+other.size>=self.x and other.x<=(self.x + self.size)) and (other.y+other.size>=self.y and other.y<=(self.y + self.size)):
            return True
        return False

# spaceship that player pilot
class Player(Space_Objects):    
    def __init__(self, x=0, y=0, size=80 ,path_assets="assets/car/", img="battleship.png", sound="explosion.wav"):
        super().__init__(x, y, size, path_assets, img, sound)         
    def shot(self):
        pass
    
# collision with those objects can change life and score
class Resources_Obstacles(Space_Objects):
    def __init__(self, x=0, y=0, size=50, path_assets="assets/car/", img="battleship.png", sound="explosion.wav", life=0, score=0):
        super().__init__(x, y, size, path_assets, img, sound)
        # how collision affect life and points of a player
        self.life = life
        self.score = score