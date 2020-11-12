import pygame
from color import Color

class Screen:
    def __init__(self, width=800, height=800, font_type="cambria", font_size=35, clock_tick=50, path_assets="assets/car/", background = "space.jpg"):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont(font_type, font_size)
        self.clock = pygame.time.Clock()
        self.clock_tick = clock_tick
        self.path_assets = path_assets
        self.background = pygame.image.load(self.path_assets + background)
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

    def refresh_background(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0,0))
    
    def draw_resources_obstacles(self, resources_obstacles_list):
        for ro in resources_obstacles_list:
            self.screen.blit(ro.img, (ro.x, ro.y))

    def draw_laser(self, laser_list):
        for laser in laser_list:
            self.screen.blit(laser.img, (laser.x, laser.y))

    def draw_player(self, player):
        self.screen.blit(player.img, (player.x, player.y))  
        
    def draw_label(self, text, var, x, y, color=Color.RED, font_type="cambria", font_size=35):
        font = pygame.font.SysFont(font_type, font_size)
        label = font.render(f"{text}: {var}", 1, color)
        self.screen.blit(label, (x, y))
        
    def draw_text(self, text, x, y, color=Color.RED, font_type="cambria", font_size=35):
        font = pygame.font.SysFont(font_type, font_size)
        label = font.render(text, 1, color)
        label_rect = label.get_rect(center=(x, y))
        self.screen.blit(label, label_rect) 

    def update_screen(self, game, player):
        self.refresh_background()
        self.draw_resources_obstacles(game.resources_obstacles_list)
        self.draw_laser(game.laser_list)
        self.draw_player(player)
        self.draw_label("Score", game.score, self.width-200, self.height-40, color=Color.RED)
        self.draw_label("Life", game.life, self.width-200, self.height-80, color=Color.RED)
        self.draw_label("Speed", game.speed, self.width-200, self.height-120, color=Color.RED)
        # how many FPS game have
        self.clock.tick(self.clock_tick)
        pygame.display.update()