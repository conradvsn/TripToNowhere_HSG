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

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location=[0,0], repeat_tile=True):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.repeat_tile = repeat_tile

    def blit(self, screen):
        if self.repeat_tile:
            times_w = int(WIDTH / self.rect.size[0]) + 1
            times_h = int(HEIGHT / self.rect.size[1]) + 1
            rect = self.rect.copy()# get base rect
            for w in range(0, times_w):
                for h in range(0, times_h):
                    # redefine rect coordinates
                    rect.left = w * self.rect.size[0]
                    rect.top = h * self.rect.size[1]
                    # blit !
                    screen.blit(self.image, rect)
        else:
            screen.blit(self.image, self.rect)
