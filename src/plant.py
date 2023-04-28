import pygame
from pygame.locals import *
# import os
from publisher import Publisher

# name, stage

class Plant(Publisher):
    def __init__(self, name, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.plant_bounds = pygame.Rect((x+16,y+124), (72,48))
        self.name = name
        self.file_name = self.name + "_"
        self.stage = 0
        self._harvested = False
        self.plant_point = (x,y)
        if name == "honeyshroom":
            self.max_stage = 2
        elif name == "elaberries":
            self.max_stage = 3
    
    @property
    def harvested(self):
        return self._harvested
 
    @harvested.setter # when a plant is changed to "harvested," notify "subscribed" objects
    def harvested(self, value):
        self._harvested = value
        self.notify()