import random
import pygame
from color import Color
from space_objects import Resources_Obstacles, Laser

class Game:
    n_levels = 10
    initial_speed = 5
    speed_jump = 1
    max_speed = 9
    pnt_nex_lvl = 50
    
    resources_obstacles =[ 
            {"img":"comet.png", "sound":"explosion.wav", "size":60, "life":-20, "score":0},
            {"img":"empire_ship.png", "sound":"explosion.wav", "size":80, "life":-15, "score":0},
            {"img":"diamond.png", "sound":"explosion.wav", "size":60, "life":0, "score":20},
            {"img": "tools.png", "sound": "explosion.wav", "size": 40, "life": 10, "score": 0}
        ]
    probability_of_objects = [0.3, 0.4, 0.25, 0.05]
    
    def __init__(self):
        self.life = 100
        self.score = 0
        self.speed = self.initial_speed
        self.level = 1
        self.resources_obstacles_list = []
        self.laser_list = []
        self.name_player = ""
        self.record_names, self.record_scores = self.read_records()
        self.ammunition = 100

    def read_records(self):
        with open("assets/records.txt", 'r') as f:
            records = f.readlines()
        record_names = [line.split()[0] for line in records]
        record_scores = [int(line.split()[1]) for line in records]
        return record_names, record_scores

    """
    Function creates objects 'above' the game screen. With every iteration game lowers them down
    number of pixels equal to Game.speed. When sumaric number of passed pixels surpass or equals to 
    height of the screen function is reapeted.
    """
    def create_resources_obstacles(self, screen_width, screen_height):
        resources_obstacles_number = random.randint(3+self.level, 10+self.level)
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
        if self.ammunition >= 20:
            laser = Laser(player_x, player_y, player_size)
            self.laser_list.append(laser)
            self.ammunition -= 20

    def update_resources_obstacles_positions(self, screen_height):
        for ro in self.resources_obstacles_list:
            if ro.y < screen_height:
                ro.y += self.speed
            else:
                self.resources_obstacles_list.remove(ro)

    def update_lasers_positions(self, pixels):
        for laser in self.laser_list:
            if laser.y > 0:
                laser.y -= self.speed
            else:
                self.laser_list.remove(laser)
                            
    def set_level_speed(self):
        self.level = min(int(self.score/self.pnt_nex_lvl),self.n_levels)
        self.speed = min(self.initial_speed + self.level*self.speed_jump, 
                         self.max_speed)
        
    def collision_check(self, player):
        for ro in self.resources_obstacles_list:
            if ro.detect_collision(player):
                self.life = min(self.life+ro.life, 100)
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
    def end_game(self, screen, game, index):
        screen.refresh_background()
        screen.draw_centered_text(text="YOU LOST!", x=0.5*screen.width, y=0.2*screen.height,
                         color=Color.RED, font_type="cambria", font_size=80)
        screen.draw_centered_text(text=f"YOUR SCORE: {game.score}", x=0.5*screen.width, y=0.3*screen.height,
                         color=Color.RED, font_type="cambria", font_size=50)

        if index is not None:
            self.record_names[index] = self.name_player
            self.record_scores[index] = game.score

            screen.draw_centered_text(text=f"ENTER YOUR NAME", x=0.5 * screen.width,
                                      y=0.4 * screen.height,color=Color.RED, font_type="cambria", font_size=40)

            for i in range(len(self.record_scores)):
                screen.draw_centered_text(text=f"{i+1}. {self.record_names[i]}: {self.record_scores[i]}", x=0.5 * screen.width,
                                          y=(0.5+0.05*i) * screen.height,color=Color.RED, font_type="cambria", font_size=40)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        with open("assets/" + 'records.txt', 'w') as file:
                            for i in range(len(self.record_scores)):
                                file.write(f"{self.record_names[i]} {self.record_scores[i]}\n")
                        return True
                    elif event.key == pygame.K_BACKSPACE:
                        self.name_player = self.name_player[:-1]
                    else:
                        self.name_player += event.unicode.upper()

        else:
            for event in pygame.event.get():
                return event.type == pygame.QUIT
