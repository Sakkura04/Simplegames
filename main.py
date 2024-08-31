from random import uniform
from typing import List, Tuple

import pygame
from os.path import join
import random

from numpy.random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        path = join('images', 'player.png')
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.direction = pygame.Vector2()
        self.speed = 300
        self.lives = 5
        self.score = 0

        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 300

        self.mask = pygame.mask.from_surface(self.image)

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def loose_life(self):
        self.lives -= 1

    def gain_score(self):
        self.score += 1

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) + int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_a]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_s]) + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_w]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.speed * self.direction * dt #to reduce power difference in computers

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf,self.rect.midtop, (all_sprites, laser_srites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        self.laser_timer()

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        self.direction = pygame.Vector2()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom <= 0:
            self.kill()

class Star(pygame.sprite.Sprite):
    positions = []  # Class-level attribute for star positions

    def __init__(self, groups,star_surf):
        super().__init__(groups)
        self.image = star_surf
        self.rect = self.image.get_frect()

    def change_pos(self, ind):
        self.rect.topleft = self.positions[ind]

    @classmethod
    def new_position(cls):
        cls.positions = [(random.randint(5, 1300), random.randint(5, 750)) for _ in range(20)]

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 300

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.kill()

class Heart(pygame.sprite.Sprite):
    def __init__(self, surf, pos, ind, groups):
        super().__init__(groups)
        self.image = surf
        self.y_pos = 15
        self.rect = self.image.get_frect(midtop = (pos, self.y_pos))
        self.index = ind

    def kills(self):
        self.image = pygame.transform.scale(pygame.image.load(join('images', 'gheart.png')).convert_alpha(), (30, 30))
        self.rect.y = 22


def collisions(player, hearts):
    good_collision = pygame.sprite.groupcollide(laser_srites, meteors_sprites, True, True)
    if good_collision:
        player.gain_score()

    collision = pygame.sprite.spritecollide(player, meteors_sprites, True)
    if collision:
        player.loose_life()
        hearts.pop(player.lives).kills()

def display_score(player):
    #time
    c_time = pygame.time.get_ticks()//1000
    time_surf = font.render(f'{c_time // 60}:{c_time % 60}', True, (255, 255, 255))
    time_rect = time_surf.get_frect(midbottom = (60, 60))
    display_surface.blit(time_surf, time_rect)

    #score
    score_surf = font.render(f'score: {player.score}', True, (255, 255, 255))
    score_rect = score_surf.get_frect(midbottom = (WINDOW_WIDTH/2, WINDOW_HEIGHT - 15))
    display_surface.blit(score_surf, score_rect)
    pygame.draw.rect(display_surface, (240,240,240), score_rect.inflate(25,15), 4, 10)


#general setup
pygame.init()
pygame.display.set_caption('My game')
WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
stars = []
hearts = []
running = True

#import
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
surf = pygame.image.load(join('images', 'heart.png')).convert_alpha()
heart_surf = pygame.transform.scale(surf, (50, 50))
font = pygame.font.SysFont(join('images', 'Oxanium-Bold.ttf'), 45)


#sprites groups
all_sprites = pygame.sprite.Group()
meteors_sprites = pygame.sprite.Group()
laser_srites = pygame.sprite.Group()

#creating sprites objectsі
Star.new_position()
for _ in range(20):
    stars.append(Star(all_sprites,star_surf))

for x in range(5):
    hearts.append(Heart(heart_surf, WINDOW_WIDTH - 50 - heart_surf.get_width()*x, x, all_sprites))

player = Player(all_sprites)

#events
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

star_event = pygame.event.custom_type()
pygame.time.set_timer(star_event, 70)

while running:
    dt = clock.tick() / 1000  #run frames/sec (if it's empty, it will run comp's max per sec) get_fsp (your comp max)
                     # dt - delta time - time it took comp to render one frame (1/time in brackets)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor((all_sprites, meteors_sprites), meteor_surf, (random.randint(10, WINDOW_WIDTH), random.randint(-200, 0)))
        if event.type == star_event:
            Star.new_position()
            for index, star in enumerate(stars):
                star.change_pos(index)

    all_sprites.update(dt)
    display_surface.fill('#3a2e3f') #rosybrown1
    display_score(player)

    collisions(player, hearts)
    if player.lives <= 0:
        running = False

    all_sprites.draw(display_surface)
    pygame.display.update()

pygame.quit()