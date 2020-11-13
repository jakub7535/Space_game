import sys
import pygame
from time import sleep
from space_objects import Player, Laser
from screen import Screen
from game import Game


def play_game(screen, player, game):
    # next_level = True
    background_sound = "background.wav"

    #     pygame.mixer.music.load(path_assets + background_sound)
    #     pygame.mixer.music.play(-1)
    # how many pixel passed
    pixels = 0
    index_calculated = False
    while True:
        if game.life > 0:
            game.collision_check(player)
            game.laser_hit_check()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and player.x > 0:
                        player.x -= 0.5 * player.size
                    elif event.key == pygame.K_RIGHT and player.x < (screen.width - player.size):
                        player.x += 0.5 * player.size
                    elif event.key == pygame.K_a:
                        game.create_laser(player.x, player.y, player.size)


            # when to create new resources and obstacles
            if pixels % screen.height >= 0 and pixels % screen.height < game.speed:
                game.create_resources_obstacles(screen.width, screen.height)
                game.ammunition = min(game.ammunition + 20, 100)
            pixels += game.speed

            game.update_resources_obstacles_positions(screen.height)
            game.update_lasers_positions(pixels)
            game.set_level_speed()
            screen.update_screen(game, player)
            pygame.display.update()
        else:
            pygame.display.update()
            # Where player would be in top scores
            if not index_calculated:
                index = next((i for i, record_score in enumerate(game.record_scores)
                              if game.score > record_score), None)
                index_calculated=True
            game_over = game.end_game(screen, game, index)
            if game_over:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                break

if __name__ == "__main__":
    pygame.init()
    screen = Screen()
    player = Player(x=screen.width / 2, y=screen.height - 100)
    game = Game()

    play_game(screen, player, game)