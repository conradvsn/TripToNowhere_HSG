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
from power import *
from random import choice, randrange
vec = pygame.math.Vector2

class Plateforme(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLATEFORME_COUCHE
        self.groups = game.all_sprites, game.plateformes
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet.get_image(1046,1444,315,95),
                  self.game.spritesheet.get_image(155,1546,141,59),
                  self.game.spritesheet.get_image(91,1340,287,85),
                  self.game.spritesheet.get_image(1054,1566,252,89)]
        self.image = choice(images)
        self.image.set_colorkey(NOIR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < POW_SPAWN_PCT:
            Power(self.game, self)
