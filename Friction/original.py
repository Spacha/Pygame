# import sys
from random import randint
import pygame
from pygame.locals import *
pygame.init()


clock = pygame.time.Clock()

fps = 60
up = False
down = False
player_location = [250 ,200]
friction = 0.9
force = 4
misy = randint(0, 400)
missile_loc = [590,misy]

player = pygame.image.load("spaceship.png")
missile = pygame.image.load("missile.png")

Window_size = (600,400)
pygame.display.set_caption("The Game")
screen = pygame.display.set_mode(Window_size, 0, 0)

player_rect = pygame.Rect(player_location[0], player_location[1], player.get_width(), player.get_height())
missile_rect = pygame.Rect(missile_loc[0], missile_loc[1], missile.get_width(), missile.get_height())

drag = 0.0
def vertical_velocity():
    global force, drag
    vel =  force / (drag + 1)
    drag += 0.05
    return vel

go = True
while go:

    screen.fill((146, 244, 255))
    pygame.draw.rect(screen, (0,0,0), player_rect)
    pygame.draw.rect(screen, (255,0,0), missile_rect)

    player_rect.x = int(player_location[0])
    player_rect.y = int(player_location[1])

    # player_location[1] *= friction

    if up == True:
        player_location[1] -= vertical_velocity()
    if down == True:
        player_location[1] += vertical_velocity()

    for event in pygame.event.get():
        if event.type == QUIT:
            go = False
        if event.type == KEYDOWN:
            if event.key == K_UP:
                up = True
            if event.key == K_DOWN:
                down = True
        if event.type == KEYUP:
            if event.key == K_UP:
                up = False
                drag = 0.0
            if event.key == K_DOWN:
                down = False
                drag = 0.0

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
