import pygame
from pygame.locals import *
import os
from main import Main

class Player(pygame.sprite.Sprite):
    def __init__(self):
        frog = pygame.image.load(r'media/img/player_0.png')
        self._display_surf.blit(frog, (100,100))
        velocity = 12
        run = True