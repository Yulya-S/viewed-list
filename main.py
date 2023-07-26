import pygame.mouse
import sqlite3
import base64

from code.items import *

def window():
    end_game = True
    menu = Menu()
    while end_game:
        clock.tick(30)
        menu.draw(pygame.mouse.get_pos())
        pygame.display.update()
        for event in pygame.event.get():
            menu.press(event)
            if event.type == pygame.QUIT:
                end_game = False
    pygame.quit()

window()
