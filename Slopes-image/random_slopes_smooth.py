import sys
import math
import random
import pygame as pg
import numpy as np

CLR_WHITE  = (255,255,255)
CLR_BLACK  = ( 0 , 0 , 0 )
CLR_BLUE   = ( 0 , 0 ,255)
CLR_YELLOW = (235,192, 52)

FPS = 60.0
SCR_SIZE = (800, 300)

# A hollow player class
class Player():
	def __init__(self):
		pass

# Init Pygame
pg.init()
scr = pg.display.set_mode(SCR_SIZE)
pg.display.set_caption("A Slope Game!")
clock = pg.time.Clock()

player = Player()
player.x      = 100
player.y      = 100
player.height = 10
player.width  = 10

# Map

# top and bottom limits for the map based on the screen size
map_y_min, map_y_max = 50, SCR_SIZE[1]-10

mx = 0.0
freq = (2*math.pi/SCR_SIZE[0]) # frequency of the sine wave
def new_element():
	global mx,freq

	# scale the new value so that it's always within the required range
	new = int(map_y_min + ((math.sin(mx)+1)/2)*(map_y_max-map_y_min))

	# update the sine wave 'sampler'
	mx += freq
	return new

def move_map(map, speed):
	# shift each element to left
	map = np.roll(map, -speed)
	
	# add new ground points to right to fill the empty space
	for el in range(speed):
		map[(-speed+el)] = new_element()
	return map

# these contain the x and y values of the slope
map_y = np.zeros(SCR_SIZE[0], dtype=int)
map_x = np.arange(SCR_SIZE[0], dtype=int)

# populate the map with random points
# first point is in the middle of the screen
map_y[0] = map_y_max-map_y_min
for x in range(1,len(map_y)):
	map_y[x] = new_element()

# how fast does the screen scroll to the left
scroll_speed = 5

exit = False
while not exit:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			exit = True
		if event.type == pg.KEYDOWN:
			# emergency exit
			if event.key == pg.K_q:
				exit = True

	scr.fill(CLR_BLACK)

	# Draw the Slope
	pg.draw.lines( scr, CLR_WHITE, False, list(zip(map_x, map_y)) )

	# Scroll the map forward by scroll speed
	map_y = move_map(map_y, scroll_speed)

	# Move the player vertically
	player.y = map_y[player.x]-player.height

	# Draw the Player
	pg.draw.rect(scr, CLR_YELLOW, pg.Rect( player.x, player.y, player.height, player.width ))

	pg.display.update()
	clock.tick(FPS)
