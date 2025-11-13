from enum import Enum
import time

import pygame, os
pygame.font.init()

from constants import *
SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_H))

from main_menu import *
from ui_misc import *
from serde import *
from ball import Ball
from level import Level
from block import Block, StaticBlock, MovingBlock

FPS = 60

pygame.display.set_caption("Shoot Your Shot")
CLOCK = pygame.time.Clock()

def create_borders():
    rects = [
            (0,0,SCREEN_W,BORDER_SIZE), 
            (0,SCREEN_H-BORDER_SIZE,SCREEN_W,BORDER_SIZE), 
            (0,BORDER_SIZE,BORDER_SIZE,SCREEN_H-BORDER_SIZE), 
            (SCREEN_W-BORDER_SIZE,BORDER_SIZE,BORDER_SIZE,SCREEN_H)    
            ]
    return [ Block(StaticBlock(v[0],v[1],v[2],v[3])) for v in rects ]

objs = create_borders()
LEVEL_0 = Level((SCREEN_W/2,SCREEN_H/2),(SCREEN_W/2,BORDER_SIZE+BALL_RADIUS + 5),objs)

class AppState(Enum):
    Menu = 1,
    Playing = 2

class App:
    def __init__(self):
        self.state = AppState.Menu
        def play():
            #level = LEVELS[self.inner.selected_level]
            level = LEVEL_0
            self.inner = level
            self.state = AppState.Playing
        self.inner = Menu(play)

    def handle_input(self,event):
        return self.inner.handle_input(event)

    def update(self):
        self.inner.update()
    
    def draw(self):
        self.inner.draw()

    def switch_to_level(self,level):
        self.state = AppState.Playing
        self.inner = level


def main_loop():
    app = App()
    running = True

    while running:
        SCREEN.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break 
            if app.handle_input(event):
                continue
        app.update()
        app.draw()


        pygame.display.flip()
        CLOCK.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main_loop()
