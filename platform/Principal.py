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
import random
from options import *
from sprites import *
from os import path

# pass = fait rien sinon message d'erreur
class Game(object):
    #__init__
    def __init__(self):
        pygame.init()
        #Pour le son
        pygame.mixer.init()
        # Ecran d'affichage
        self.fenetre = pygame.display.set_mode((WIDTH, HEIGHT))
        # Nom de la fenetre
        pygame.display.set_caption("TRIP TO NOWHERE")
        # Pour le fps
        self.temps = pygame.time.Clock()
        #Innitialliser la fenetre du jeu
        self.running = True
        self.police = pygame.font.match_font(POLICE)
        self.load_data()
    #graphics loading
    def load_data(self):
            # load high score
        self.localisation = path.dirname(__file__)
        img_localisation = path.join(self.localisation, 'img')
        with open(path.join(self.localisation, MS_FICHIER), 'w') as f:
            try :
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # charger le spritesheet
        self.spritesheet = Spritesheet(path.join(img_localisation, SPRITESHEET))
        # charger fond_écran
        self.fondecran = Background(path.join(img_localisation, BACKGROUND))
        #Commandes liées au son
        self.son_dir = path.join(self.localisation, 'son')
        self.son_saut = pygame.mixer.Sound(path.join(self.son_dir, SON_SAUT))
        self.son_boost = pygame.mixer.Sound(path.join(self.son_dir, SON_BOOST))
    def new(self):
        #Commencer le jeu
        self.score = 0
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.plateformes = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.joueur = Joueur(self)
        for plat in Plateforme_liste:
            p = Plateforme(self, *plat)
        self.mob_timer = 0
        pygame.mixer.music.load(path.join(self.son_dir, 'Son2.ogg'))
        self.run()
    def run(self):
        #Boucle du jeu principale
        # Garder la boucle à la même vitesse
        pygame.mixer.music.play(loops=-1)
        self.actif = True
        while self.actif:
            self.temps.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(500)
    def update(self):
        #Game loop - update
        # Update
        self.all_sprites.update()

        # spawn un mob
        now = pygame.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)
        #percuter un mob
        mob_collisions = pygame.sprite.spritecollide(self.joueur, self.mobs, False, pygame.sprite.collide_mask)
        if mob_collisions:
            self.actif = False
        #savoir si le joueur touche quelque chose s'il tombe
        if self.joueur.vit.y > 0:
            collisions = pygame.sprite.spritecollide(self.joueur, self.plateformes, False)
            for plateforme in collisions :
                if collisions:
                    lowest = collisions[0]
                    for collision in collisions :
                        if collision.rect.bottom > lowest.rect.bottom:
                            lowest = collision
                        if self.joueur.pos.x < lowest.rect.right + 10 and \
                        self.joueur.pos.x > lowest.rect.left - 10 :
                            if self.joueur.pos.y < lowest.rect.centery:
                                self.joueur.pos.y = lowest.rect.top
                                self.joueur.vit.y = 0
                                self.joueur.jumping = False

    #            if plateforme.type =='forte':
    #                collisions_f = pygame.sprite.spritecollide(self.joueur, self.plateformes, False)
    #                for collision in collisions :
    #                    if collisions_f:
    #                        self.actif = False

        #qd le joueur arrive à la limite de l'écran 1/4 du haut
        if self.joueur.rect.top <= HEIGHT / 4 :
            self.joueur.pos.y  += max(abs(self.joueur.vit.y), 2)
            for mob in self.mobs :
                mob.rect.y += max(abs(self.joueur.vit.y), 2)
            for plat in self.plateformes :
                plat.rect.y += max(abs(self.joueur.vit.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        #touche le powerup
        power_collision = pygame.sprite.spritecollide(self.joueur, self.powerups, True)
        for power in power_collision:
            if power.type == 'boost':
                self.son_boost.play()
                self.joueur.vit.y = -BOOST_POWER
                self.joueur.jumping = False
            if power.type == 'score':
                self.score += 100



        # Mort
        if self.joueur.rect.bottom > HEIGHT :
            for sprite in self.all_sprites :
                sprite.rect.y -= max(self.joueur.vit.y, 10)
                if sprite.rect.bottom < 0 :
                    sprite.kill()
        if len(self.plateformes) == 0:
            self.actif = False

        #Nouvelles Plateformes
        while len(self.plateformes) <6:
            width = random.randrange(50,100)
            p = Plateforme(self, random.randrange(0, WIDTH - width),
                           random.randrange(-75, -30))
    def events(self):
        #Game Loop - events
        # Process input (events)
        for event in pygame.event.get():
            #Fermer la fenetre
            if event.type == pygame.QUIT:
                if self.actif:
                    self.actif = False
                self.running = False

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE:
                    self.joueur.saut()
                    self.son_saut.play()
            if event.type == pygame.KEYUP :
                if event.key == pygame.K_SPACE:
                    self.joueur.saut_cut()
    def draw(self):
        #Game loop - draw
        # Draw
        self.fenetre.fill(BGCOLOR)
        self.fondecran.blit(self.fenetre)
        self.all_sprites.draw(self.fenetre)
        self.draw_text(str(self.score), 25, BLANC, WIDTH / 2, 15)
        pygame.display.flip()
    def show_start_screen(self):
        #Ecran de démarrage
        pygame.mixer.music.load(path.join(self.son_dir, 'intro.ogg',))
        pygame.mixer.music.play(loops=-1)
        self.actif = True
        self.fenetre.fill(BGCOLOR)
        self.draw_text(TITRE, 48, BLANC, WIDTH / 2, HEIGHT / 4)
        self.draw_text("The arrows to navigate and the space bar to jump", 18, BLANC, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to start", 18, BLANC, WIDTH / 2, HEIGHT * 3/4 )
        self.draw_text("Best score : " + str(self.highscore), 22, BLANC, WIDTH / 2, 15)
        pygame.display.flip()
        self.wait_for_key()
        pygame.mixer.music.fadeout(500)
    def show_go_screen(self):
        #Pour ne pas etre bloqué par l'ecran lorsque l'on clique sur la croix
        pygame.mixer.music.load(path.join(self.son_dir, 'Gameover.ogg',))
        pygame.mixer.music.play(loops=-1)
        self.actif = True
        if not self.running :
            return
        #Ecran de fin - Game over
        self.draw_text("Game Over!", 48, BLANC, WIDTH / 2, HEIGHT / 4)
        self.draw_text("You were almost there. :-) Score: " + str(self.score), 18, BLANC, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play again", 18, BLANC, WIDTH / 2, HEIGHT * 3/4 )
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW BEST SCORE.", 22, BLANC, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.localisation, MS_FICHIER), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("Best score: " + str(self.highscore), 22, BLANC, WIDTH / 2, HEIGHT / 2 + 40)
        pygame.display.flip()
        self.wait_for_key()
        pygame.mixer.music.fadeout(500)
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.temps.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False
    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.police, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.fenetre.blit(text_surface, text_rect)
g = Game()
#start screen
g.show_start_screen()
while g.running:
    g.new()
    #game over
    g.show_go_screen()

pygame.quit()
