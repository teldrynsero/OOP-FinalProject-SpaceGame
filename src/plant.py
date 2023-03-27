import pygame
from pygame.locals import *
import os
# from main import Main

# name, stage

class Plant():
    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.name = name + "_"
        self.stage = "0"
    # def file(self):
        self.file_name = self.name + self.stage
        # self.image = pygame.image.load(self.file_name)
        # self._display_surf.blit(self.file_name, (self.x,self.y))
        