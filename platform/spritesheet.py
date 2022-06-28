#-------------------------------------------------------------------------------
# Name : Trip to NOWHERE
#
# Author : Conrad and ARIS
#
# Created : 15/04/11
#
#Copyright : (c) Conrad and ARIS
#-------------------------------------------------------------------------------

import pygame
from options import *
from random import choice, randrange
vec = pygame.math.Vector2

class Spritesheet(object):
# utility class for loading and parsing Spritesheets
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        #grab an img out of a larger spritesheet
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width // 2, height // 2))
        return image
