import sys
import random
import pygame as pg
import numpy as np

CLR_WHITE = (255,255,255)
CLR_BLACK = ( 0 , 0 , 0 )
CLR_BLUE  = ( 0 , 0 ,255)

FPS = 60.0
# FPS = 10.0
SCR_SIZE = (250, 100)

class Player():
	def __init__(self):
		pass

pg.init()
scr = pg.display.set_mode(SCR_SIZE)
pg.display.set_caption("A Slope Game!")
clock = pg.time.Clock()

player = Player()
player.x = 100
player.y = 100

# Map
MAP_SIZE_X = 4000
map_y_min, map_y_max = 10, SCR_SIZE[1]-10

'''
for x in range(MAP_SIZE_X):
	map_y[x] = int(map_y_min + random.random()*(map_y_max-map_y_min))
'''
def new_element():
	return int(map_y_min + random.random()*(map_y_max-map_y_min))

def move_map(map, speed):
	# shift each element to left
	map = np.roll(map, -speed)
	
	# add new ground points
	for el in range(speed):
		map[(-speed+el)] = new_element()

	return map

map_y = np.zeros(SCR_SIZE[0])
map_x = np.arange(MAP_SIZE_X)

# populate the map with random points
for x in range(len(map_y)):
	map_y[x] = new_element()

# tells the visible area of the map
view_bounds = np.array([0, SCR_SIZE[0]])
scroll_speed = 2

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
	# map_visible_y = map_y[ view_bounds[0] : view_bounds[1] ]
	
	pg.draw.lines( scr, CLR_WHITE, False, list(zip(map_x, map_y)) )

	# scroll the map forward
	map_y = move_map(map_y, scroll_speed)
	print(map_y)

	# Draw the Player
	pg.draw.rect(scr, CLR_BLUE, pg.Rect( player.x, player.y, 10, 10 ))

	pg.display.update()
	clock.tick(FPS)

pg.quit()
sys.exit()
