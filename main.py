import pygame
from os.path import join
import random

#general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True

surf = pygame.Surface((100,200))
pygame.display.set_caption('My game')
player_direction = 0.1
y = 1
clock = pygame.time.Clock()

path = join('images', 'player.png')
star_path = join('images', 'star.png')
meteor_path = join('images', 'meteor.png')
laser_path = join('images', 'laser.png')

player_surf = pygame.image.load(path).convert_alpha()
player_rect = player_surf.get_frect(center = (70, WINDOW_HEIGHT-100))

star = pygame.image.load(star_path).convert_alpha()
star_positions = [(random.randint(50, 1200), random.randint(50, 650)) for _ in range(20)]

meteor = pygame.image.load(meteor_path).convert_alpha()
meteor_positions = [(random.randint(50, 1200), random.randint(-3000, -15)) for _ in range(20)]

laser = pygame.image.load(laser_path).convert_alpha()
laser_rect = player_surf.get_frect(bottomleft = player_rect.midtop)


while running:
    clock.tick(500)  #run frames per second (if it's empty, it will run comp's maximum per second)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill('rosybrown1')
    y += 0.5

    if y%2 == 5:
        star_positions = [(random.randint(50, 1200), random.randint(50, 650)) for _ in range(20)]

    for x in star_positions:
        display_surface.blit(star, x)


    for x1, y1 in meteor_positions:
        display_surface.blit(meteor, (x1, y1+y))

    if y == WINDOW_HEIGHT + 3500:
        meteor_positions = [(random.randint(50, 1200), random.randint(-3000, -15)) for _ in range(20)]
        y = 1

    player_rect.x += player_direction * 10
    laser_rect.x += player_direction * 10
    if player_rect.right >= WINDOW_WIDTH  or player_rect.left <= 0:
        player_direction *= -1
    player_rect.left += player_direction
    laser_rect.left += player_direction

    display_surface.blit(player_surf, player_rect.topleft)
    display_surface.blit(laser, laser_rect.topleft)
    pygame.display.update()

pygame.quit()