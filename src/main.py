# /// script
# dependencies = [
#  "pygame",
#  "perlin_noise",
# ]
# ///
import asyncio
import pygame
import perlin_noise

import platform
import sys

if platform.system() == "Windows":
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

import constants
from game import Game
from game_scene.main_menu import MainMenuScene
from ui import *

game = Game()

async def main():
    global game
    
    game.start(MainMenuScene(game))

    clock = pygame.time.Clock()
    while not game.should_quit_game:
        current_monitor_refresh_rate = pygame.display.get_current_refresh_rate()
        delta = clock.tick_busy_loop(current_monitor_refresh_rate) / 1000 # Fixes stuttering for some reason
        delta = min(delta, 1 / 30) # Prevents weird issues if, for example, the window is moved and the main thread is blocked

        if delta:
            pygame.display.set_caption(f"{constants.GAME_NAME} | {(1.0 / delta):.2f}fps")
        
        game.run(delta)
        
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())