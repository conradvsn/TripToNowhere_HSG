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

class Power(pygame.sprite.Sprite):
    def __init__(self, game, plat):

        self.groups = game.all_sprites, game.powerups
        self._layer = POWER_COUCHE
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(['boost', 'score'])
        powerup_images = {}
        powerup_images['boost'] = self.game.spritesheet.get_image(1148,1281,111,155)
        powerup_images['score'] = self.game.spritesheet.get_image(180,1650,81,79)
        self.image = powerup_images[self.type]
        self.image.set_colorkey(NOIR)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top -5
    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.plateformes.has(self.plat):
            self.kill()
