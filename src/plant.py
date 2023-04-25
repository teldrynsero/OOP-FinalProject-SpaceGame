import pygame
from pygame.locals import *
import os
# from main import Main

# name, stage

class Plant():
    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.plant_bounds = pygame.Rect((x+16,y+124), (72,48))
        self.name = name + "_"
        self.stage = 0

        self.plant_point = (x,y)

    # def file(self):
        # self.file_name = self.name + str(self.stage)
        # self.image = pygame.image.load(self.file_name)
        # self._display_surf.blit(self.file_name, (self.x,self.y))
        if name == "honeyshroom":
            self.max_stage = 2
        elif name == "elaberries":
            self.max_stage = 3
        