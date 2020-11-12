import random
import pygame
from time import sleep
from copy import deepcopy
from player import Player, Resources_Obstacles, Laser

class Game:
    n_levels = 6
    initial_speed = 5
    speed_jump = 1
    pnt_nex_lvl = 50
    
    resources_obstacles =[ 
            {"img":"comet.png", "sound":"explosion.wav", "size":100, "life":-10, "score":0},
           {"img":"ufo.png", "sound":"explosion.wav", "size":80, "life":-15, "score":0},
           {"img":"diamond.png", "sound":"explosion.wav", "size":60, "life":0, "score":30}
        ]
    probability_of_objects = [0.2, 0.3, 0.5]
    
    def __init__(self):
        self.life = 100
        self.score = 0
        self.speed = self.initial_speed
        self.level = 1
        self.resources_obstacles_list = []
        self.laser_list = []
    
    
    """
    Function creates objects 'above' the game screen. With every iteration game lowers them down
    number of pixels equal to Game.speed. When sumaric number of passed pixels surpass or equals to 
    height of the screen function is reapeted.
    """
    def create_resources_obstacles(self, screen_width, screen_height):
        resources_obstacles_number = random.randint(3,10)
        for i in range(resources_obstacles_number):
            # parameters of new objects of Obstacles_Resources
            ro_param = random.choices(self.resources_obstacles, self.probability_of_objects)[0]            
            ro_x = random.randint(0, screen_width)
            ro_y = random.randint(-screen_height, 0)
            new_ro = Resources_Obstacles(x=ro_x, y=ro_y,
                                    img=ro_param["img"],sound=ro_param["sound"],
                                    size=ro_param["size"],life=ro_param["life"],
                                    score=ro_param["score"])
            self.resources_obstacles_list.append(new_ro)

    def create_laser(self, player_x, player_y, player_size):
        laser = Laser(player_x, player_y, player_size)
        self.laser_list.append(laser)

    def update_resources_obstacles_positions(self, screen_height):
        for ro in self.resources_obstacles_list:
            if ro.y < screen_height:
                ro.y += self.speed
            else:
                self.resources_obstacles_list.remove(ro)

    def update_lasers_positions(self, screen_height):
        for laser in self.laser_list:
            if laser.y > 0:
                laser.y -= self.speed
            else:
                self.laser_list.remove(laser)
                            
    def set_level_speed(self):
        self.level = min(int(self.score/self.pnt_nex_lvl),self.n_levels)
        self.speed = min(self.initial_speed + self.level*self.speed_jump, 
                         self.initial_speed + self.n_levels*self.speed_jump) 
        
    def collision_check(self, player):
        for ro in self.resources_obstacles_list:
            if ro.detect_collision(player):
                self.life += ro.life
                self.score += ro.score
                self.resources_obstacles_list.remove(ro)
                #enemy.sound.play()
        return False

    def laser_hit_check(self):
        for laser in self.laser_list:
            for ro in self.resources_obstacles_list:
                if ro.detect_collision(laser):
                    self.resources_obstacles_list.remove(ro)
                    self.laser_list.remove(laser)
                    #enemy.sound.play()
        return False
    
    # function run after player have lost
    def end_game(screen, game, player):
        screen.update_screen(game, player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                return True
            else:
                return False

