import pygame

# every object on the screen
class Space_Objects:
    def __init__(self, x=0, y=0, size=50, img="battleship.png", sound="explosion.wav"):
        self.x = x 
        self.y = y
        self.size = size
        self.img = pygame.image.load("assets/" + img)
        self.img = pygame.transform.scale(self.img, (self.size, self.size))  
        self.sound = pygame.mixer.Sound("assets/" + sound)
        
    def detect_collision(self, other):
        if (other.x+other.size>=self.x and other.x<=(self.x + self.size)) and (other.y+other.size>=self.y and other.y<=(self.y + self.size)):
            return True
        return False

# spaceship that player pilot
class Player(Space_Objects):    
    def __init__(self, x=0, y=0, size=80 , img="battleship.png", sound="explosion.wav"):
        super().__init__(x, y, size, img, sound)

# laser destroys any object
class Laser(Space_Objects):
    def __init__(self, player_x=0, player_y=0, player_size=0, size=40, img="laser.png"):
        self.x = player_x + int(0.5*(player_size - size))
        self.y = player_y - int(size)
        self.size = size
        self.img = pygame.image.load("assets/" + img)
        self.img = pygame.transform.scale(self.img, (self.size, self.size))
    
# collision with those objects can change life and score
class Resources_Obstacles(Space_Objects):
    def __init__(self, x=0, y=0, size=50, img="battleship.png", sound="explosion.wav", life=0, score=0):
        super().__init__(x, y, size, img, sound)
        # how collision affect life and points of a player
        self.life = life
        self.score = score