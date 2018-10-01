# big thank you to the pygame lesson series at kidscancode.org
# all sprites found at http://spritedatabase.net/
# cartoon network / kirby's dreamland 3 / dragon ball z: chou saiya densetsu
# original music / sound effects by me / ian hundere / https://soundcloud.com/grassnose / https://grassnose.bandcamp.com

import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')


WIDTH = 1000
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#init pygame / create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("eggy mceggy and friends")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def text_draw(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, ((23, 11, 128)))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

class Eggy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(eggy_img, (44, 48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH - 40 
        self.rect.bottom = HEIGHT / 2
        self.speedx = 0 
        self.speedy = 0
        self.pew_delay = 125
        self.last_pew = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()


    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 0:
            self.hidden = False
            self.rect.centerx = WIDTH - 40
            self.rect.bottom =HEIGHT / 2
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if keystate[pygame.K_SPACE]:
            self.shoot()
        
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.y < 0:
            self.rect.y = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0  
        
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_pew > self.pew_delay:
            self.last_pew = now
            triangle = Triangle(self.rect.centerx, self.rect.top)
            all_sprites.add(triangle)
            triangles.add(triangle)
            pew_sound.play()
        
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH - 40 / 2, HEIGHT / 2)
        screen.fill(pygame.Color("black"))
        

class Buds(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(bud_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % -360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(1, 8)
    
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT - 40)

class Triangle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(laser_img, (15, 14))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y + 30
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.x += self.speedy
        # delete if moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 35

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    screen.blit(background, background_rect)
    text_draw(screen, "eggy mceggy and friends", 105, WIDTH / 2, HEIGHT / 1.75)
    text_draw(screen, "space makes triangles / arrows to move", 30, WIDTH / 2, HEIGHT / 1.90)
    text_draw(screen, "press a key to start", 30, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True 
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# load sprites
background = pygame.image.load(path.join(img_dir, "clouds2.png")).convert()
background_rect = background.get_rect()
eggy_img = pygame.image.load(path.join(img_dir, "player.png")).convert()
eggy_mini_img = pygame.transform.scale(eggy_img, (22, 24))
eggy_mini_img.set_colorkey(BLACK)
laser_img = pygame.image.load(path.join(img_dir, "laser.png")).convert()
bud_images = []
bud_list = ["enemy.png", "enemy2.png", "enemy3.png", "enemy4.png"]

for img in bud_list:
    bud_images.append(pygame.image.load(path.join(img_dir, img)).convert())
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['eggy'] = []

for i in range(3):
    filename = '{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (65, 65))
    explosion_anim['lg'].append(img_lg)

for j in range(5):
    filename = 'p{}.png'.format(j)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img = pygame.transform.scale(img, (40,40))
    explosion_anim['eggy'].append(img)

# load snds
pew_sound = pygame.mixer.Sound(path.join(snd_dir, 'shoot.ogg'))
by_snds = []
for snd in ['kill1.ogg', 'kill2.ogg', 'kill3.ogg']:
    by_snds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
eggy_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'blo.ogg'))
pygame.mixer.music.load(path.join(snd_dir, 'ligawok.mp3'))

pygame.mixer.music.play(loops=-1)

# game loop
no_game = True
running = True
while running:
    if no_game:
        show_go_screen()
        no_game = False
        all_sprites = pygame.sprite.Group()
        buds = pygame.sprite.Group()
        triangles = pygame.sprite.Group()
        eggy = Eggy()
        all_sprites.add(eggy)
        for i in range(8):
            m = Buds()
            all_sprites.add(m)
            buds.add(m)
        score = 0

    # keep loop running at the right speed
    clock.tick(FPS)
    # process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                eggy.shoot()


    # update
    all_sprites.update()

    # check if triangle touches buds
    hits = pygame.sprite.groupcollide(buds, triangles, True, True)
    for hit in hits:
        score += 100 - hit.radius
        random.choice(by_snds).play()
        expl = Explosion(hit.rect.center, 'lg')
        m = Buds()
        all_sprites.add(expl, m)
        buds.add(m)

    # you poof / explod done
    if eggy.lives == 0 and not die.alive():
        no_game = True



    # was triangle given
    hits = pygame.sprite.spritecollide(eggy, buds, True, pygame.sprite.pygame.sprite.collide_circle)
    for hit in hits: 
        eggy_die_sound.play()
        die = Explosion(eggy.rect.center, 'eggy')
        all_sprites.add(die)
        eggy.hide()
        eggy.lives -= 1


    if eggy.lives == 0 and not die.alive():
        no_game = True

            

    # draw stuff
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    text_draw(screen, str(score), 80, WIDTH / 1.10, 10)
    draw_lives(screen, WIDTH - 995, 5, eggy.lives, eggy_mini_img)
    # after draw, flip the display
    pygame.display.flip()

pygame.quit()
