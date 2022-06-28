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

class Joueur(pygame.sprite.Sprite):
    #Sprites du joueur
    def __init__(self, game):
        self._layer = JOUEUR_COUCHE
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        #Il connait mtn le jeu comme une copie
        self.game = game
        self.walking = False
        self.jumping = False
        #plusieurs animation
        self.current_frame = 1
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[1]
        #enlever fond noir
        self.rect = self.image.get_rect()
        #mettre au millieu
        self.rect.center = (40, HEIGHT -100)
        self.pos = vec(40, HEIGHT -100)
        self.vit = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
            self.standing_frames = [self.game.spritesheet.get_image(911, 49, 127, 145),
                                   self.game.spritesheet.get_image(774, 63, 130, 130)]
            for frame in self.standing_frames:
                frame.set_colorkey(NOIR)
            self.walk_frames_r = [self.game.spritesheet.get_image(337, 413, 124, 139),
                                  self.game.spritesheet.get_image(464, 411, 80, 137),
                                  self.game.spritesheet.get_image(546, 405, 94, 145),
                                  self.game.spritesheet.get_image(805, 413, 88, 139),
                                  self.game.spritesheet.get_image(893, 410, 98, 124)]
            for frame in self.walk_frames_r:
                frame.set_colorkey(NOIR)
            self.walk_frames_l = []
            for frame in self.walk_frames_r:
                frame.set_colorkey(NOIR)
                self.walk_frames_l.append(pygame.transform.flip(frame, True, False))
                #true hori/verti
            self.jump_frames = [self.game.spritesheet.get_image(383, 208, 79, 186),
                               self.game.spritesheet.get_image(483, 220, 108, 170)]
            for frame in self.jump_frames:
                frame.set_colorkey(NOIR)

    def saut_cut(self):
        if self.jumping:
            if self.vit.y < -3:
                self.vit.y = -3

    def saut(self):
        # saut seuleument si position sur plateforme
        self.rect.x += 1
        collisions = pygame.sprite.spritecollide(self, self.game.plateformes, False)
        self.rect.x -= 1
        if collisions and not self.jumping:
            self.game.son_saut.play
            self.jumping = True
            self.vit.y = -JOUEUR_SAUT


    def update(self):
        self.animate()
        #gravité
        self.acc = vec(0, JOUEUR_GRAVITE)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -JOUEUR_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = JOUEUR_ACC
#Initiallisation des frottements
        self.acc.x += self.vit.x * JOUEUR_FROTTEMENTS
#Equation liée aux mouvements
        self.vit += self.acc
        #pb niveau de la vitesse et du perso pour qu'il passe en mode standing
        if abs(self.vit.x) < 0.1:
            self.vit.x = 0

        self.pos += self.vit + 0.5 * self.acc
#Pour ne pas sortir de la fenetre
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0  - self.rect.width / 2 :
            self.pos.x = WIDTH + self.rect.width / 2
#Pour ne pas passer à travers la plateforme
        self.rect.midbottom = self.pos

    def animate(self):
            now = pygame.time.get_ticks()
            #pas egale
            if self.vit.x !=0:
                self.walking = True
            else:
                self.walking = False
                #show walk animation
            if self.walking:
                if now - self.last_update > 250:
                    self.last_update = now
                    self.current_frame = (self.current_frame +1) % len(self.walk_frames_l)
                    bottom = self.rect.bottom
                    if self.vit.x > 0:
                        self.image = self.walk_frames_r[self.current_frame]
                    else:
                        self.image = self.walk_frames_l[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom

            if not self.jumping and not self.walking:
                if now - self.last_update > 350:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                    bottom = self.rect.bottom
                    self.image = self.standing_frames[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
            #perfect collision
            self.mask = pygame.mask.from_surface(self.image)
