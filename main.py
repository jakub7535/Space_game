import sys
import pygame
from time import sleep
from player import Player, Space_Objects
from screen import Screen
from game import Game


def play_game(screen, player, game):
    # next_level = True
    background_sound = "background.wav"

    #     pygame.mixer.music.load(path_assets + background_sound)
    #     pygame.mixer.music.play(-1)
    # how many pixel passed
    pixels = 0
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
            pixels += game.speed

            game.update_resources_obstacles_positions(screen.height)
            game.update_lasers_positions(screen.height)
            game.set_level_speed()
            screen.update_screen(game, player)

        else:
            game_over = Game.end_game(screen, game, player)
            if game_over:
                sys.exit()
                break


if __name__ == "__main__":
    path_assets = "assets/car/"
    pygame.init()
    screen = Screen(path_assets=path_assets)
    player = Player(x=screen.width / 2, y=screen.height - 100, path_assets=path_assets)
    game = Game()

    play_game(screen, player, game)