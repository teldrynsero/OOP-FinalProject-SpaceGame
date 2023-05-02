import pygame
from pygame.locals import *
# import os
from publisher import Publisher

# name, stage

class Plant(Publisher):
    """plants to be watered then harvested

    Args:
        Publisher (class): Observer pattern - allows plants to manage "subscribers"
    """
    def __init__(self, name, x, y):
        """initializing location and type of plant, managing status of plant

        Args:
            name (string): type of plant
            x (int): player x position
            y (int): player y position
        """
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
        """can be called to check the harvest status of the plant

        Returns:
            bool: whether or not the plant has been harvested
        """
        return self._harvested
 
    @harvested.setter # when a plant is changed to "harvested," notify "subscribed" objects
    def harvested(self, value):
        """is called to change the harvest status of the plant, will notify subscribers of the plant that it has been changed

        Args:
            value (bool): new harvest status of the plant
        """
        self._harvested = value
        self.notify()