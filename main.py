from random import uniform
from typing import List, Tuple

import pygame
from os.path import join
import random

from numpy.random import randint
from pygame.time import get_ticks


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
        if not self.can_shoot and pygame.time.get_ticks() - self.laser_shoot_time >= self.cooldown_duration:
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

        self.rect.clamp_ip(pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf,self.rect.midtop, (all_sprites, laser_srites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()
        self.laser_timer()

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
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
    spinning = False

    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.original_surf = surf
        self.image = self.original_surf
        self.rect = self.image.get_frect(center=pos)
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = 300
        self.rotation = 0
        self.spin_axeleration = 0

    def update(self, dt):
        # movement of meteors
        self.rect.center += self.direction * self.speed * dt
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.kill()

        # meteors' spinning
        if Meteor.spinning:
            self.spin_axeleration = pygame.time.get_ticks()/1000
            self.rotation += 500 * dt
            self.speed += dt + self.spin_axeleration
            self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
            self.rect = self.image.get_frect(center = self.rect.center)

    @classmethod
    def start_spin(self):
        Meteor.spinning = True

    @classmethod
    def stop_spin(self):
        Meteor.spinning = False

    @classmethod
    def get_spin(self):
        return Meteor.spinning

class Heart(pygame.sprite.Sprite):
    def __init__(self, surf, pos, ind, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midtop = (pos, 15))
        self.index = ind

    def kills(self):
        self.image = pygame.transform.scale(pygame.image.load(join('images', 'gheart.png')).convert_alpha(), (30, 30))
        self.rect.y = 22

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frame_index += 40 * dt #Якщо ти збільшуєш self.frame_index на більше на більше значення за кожну ітерацію циклу (наприклад, на 40 * dt), індекс швидше досягне наступного цілого числа (інд наступного кадру).
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()


def collisions(player, hearts):
    for laser in laser_srites:
        if pygame.sprite.spritecollide(laser, meteors_sprites, True):
            explosion_sound.play()
            player.gain_score()
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)

    if pygame.sprite.spritecollide(player, meteors_sprites, True, pygame.sprite.collide_mask):
        damage_sound.play()
        player.loose_life()
        hearts[player.lives].kills()

def display_score(player, current_time, flag):
    #time
    colour = (210, 36, 36) if flag else (255, 255, 255)
    time_font = pygame.font.SysFont(join('images', 'Oxanium-Bold.ttf'), 60 if flag else 45)
    position = (110, 65) if flag else (100, 60)

    c_time = current_time//1000
    time_surf = time_font.render(f'{c_time // 60}:{c_time % 60}', True, colour)
    time_rect = time_surf.get_frect(midbottom = position)
    display_surface.blit(time_surf, time_rect)

    #score
    score_surf = font.render(f'score: {player.score}', True, (255, 255, 255))
    score_rect = score_surf.get_frect(midbottom = (WINDOW_WIDTH/2, WINDOW_HEIGHT - 15))
    display_surface.blit(score_surf, score_rect)
    pygame.draw.rect(display_surface, (240,240,240), score_rect.inflate(25,15), 4, 10)

def display_pause():
    pause_rect = pause_surf.get_frect(midbottom = (40, 60))
    display_surface.blit(pause_surf, pause_rect)
    return pause_rect

def display_alarm(text, countdown_time, start_time):
    elapsed_time = pygame.time.get_ticks() - start_time
    remaining_time = max(-1, countdown_time - (elapsed_time // 1000))  # Convert to seconds

    if remaining_time > 0:
        alarm_surf = font.render(f'{text} in {remaining_time}...', True, (210, 36, 36))
    else:
        alarm_surf = font.render(f'{text} now!', True, (210, 36, 36))
        Meteor.start_spin()

    alarm_rect = alarm_surf.get_frect(midtop =(WINDOW_WIDTH/2, 20))
    display_surface.blit(alarm_surf, alarm_rect)

    return remaining_time


#general setup
pygame.init()
pygame.display.set_caption('My game')
WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
last_spin_time = 0
spin_start_time = -1
spin_duration = randint(10000, 20000)
remaining_time = 10000
stars, hearts = [], []
running = True

#import
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
surf = pygame.image.load(join('images', 'heart.png')).convert_alpha()
heart_surf = pygame.transform.scale(surf, (50, 50))

p_surf = pygame.image.load(join('images', 'pause.png')).convert_alpha()
pause_surf = pygame.transform.scale(p_surf, (40, 40))

font = pygame.font.SysFont(join('images', 'Oxanium-Bold.ttf'), 45)
explosion_frames = [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() for i in range (21)]

# Sound setup
laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
damage_sound = pygame.mixer.Sound(join('audio', 'damage.ogg'))
game_music = pygame.mixer.Sound(join('audio', 'game_music.wav'))

game_music.set_volume(0.3)
explosion_sound.set_volume(0.2)
laser_sound.set_volume(0.3)
game_music.play(loops = -1)

# Pause setup
paused = False
pause_start_time = 0
pause_duration = 0
text_scale = 1.0
current_time = 0

#sprites groups
all_sprites = pygame.sprite.Group()
meteors_sprites = pygame.sprite.Group()
laser_srites = pygame.sprite.Group()

#creating sprites objects
player = Player(all_sprites)
hearts = [Heart(heart_surf,  WINDOW_WIDTH - 50 - heart_surf.get_width() * i, i, all_sprites) for i in range(player.lives)]
Star.new_position()
stars = [Star(all_sprites,star_surf) for _ in range(20)]

#events
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

super_meteor_event = pygame.event.custom_type()
pygame.time.set_timer(super_meteor_event, 60000)

star_event = pygame.event.custom_type()
pygame.time.set_timer(star_event, 70)

while running:
    current_time = pygame.time.get_ticks() - pause_duration
    dt = clock.tick() / 1000  #run frames/sec (if it's empty, it will run comp's max per sec) get_fsp (your comp max)
                                # dt - delta time - time it took comp to render one frame (1/time in brackets)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            pause_rect = display_pause()

            if pause_rect.collidepoint(mouse_pos):
                if paused:
                    paused = False
                    pause_duration += current_time - pause_start_time
                    game_music.set_volume(0.3)
                else:
                    paused = True
                    pause_start_time = pygame.time.get_ticks()
                    game_music.set_volume(0.07)

        if event.type == star_event and not paused:
            Star.new_position()
            for index, star in enumerate(stars):
                star.change_pos(index)

        if event.type == super_meteor_event and not paused:
            spin_start_time = current_time
            last_spin_time = current_time + spin_duration

        if event.type == meteor_event and not paused:
            Meteor((all_sprites, meteors_sprites), meteor_surf, (random.randint(10, WINDOW_WIDTH), random.randint(-200, 0)))


    if not paused:
        all_sprites.update(dt)
        display_surface.fill('#3a2e3f') #rosybrown1

        if spin_start_time >= 0:
            remaining_time = display_alarm("Super meteor rain", 3, spin_start_time)
        if current_time > last_spin_time:
            spin_start_time = -1
            Meteor.stop_spin()


        collisions(player, hearts)
        all_sprites.draw(display_surface)
        display_pause()
        display_score(player, current_time, Meteor.get_spin())

        if player.lives <= 0:
            running = False

        pygame.display.update()

pygame.quit()