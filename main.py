from PIL import Image
import pygame as pg
import numpy as np
import time
import sys

CLR_WHITE = (255,255,255)
CLR_BLACK = ( 0 , 0 , 0 )
CLR_BLUE  = ( 0 , 0 ,255)

class Vector():
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Game():
	def __init__(self, scr_size, fps):
		self.scr_size = scr_size
		self.fps = fps
		self.gravity = 1.5

		# init pygame
		pg.init()
		self.scr = pg.display.set_mode(self.scr_size)
		pg.display.set_caption("A Slope Game!")
		self.clock = pg.time.Clock()
		self.background_clr = CLR_BLACK

		# world settings
		self.ground = None
		self.objects = []

	def update(self):
		for obj in self.objects:
			obj.update() # start by calculating the new position

			# change object velocity if necessary
			if not obj.static:
				self.check_ground(obj)

	def check_ground(self, obj):
		ground_h = self.ground.height_at(obj.position.x)
		
		'''
		if obj.bottom() >= (ground_h - 2):
			if not obj.on_ground:
				obj.on_ground = True
		else:
			if obj.on_ground:
				obj.on_ground = False
		'''

		if obj.bottom() >= ground_h:
			obj.velocity.y = 0
			obj.position.y = ground_h - obj.height

			# if there's vertical motion, update it using
			# 'derivative' of the ground slope
			#if abs(obj.velocity.x) > 0:
			#	obj.velocity.x = 

			if not obj.on_ground:
				obj.on_ground = True
		else:
			obj.velocity.y += self.gravity

			if obj.on_ground:
				obj.on_ground = False

	def draw(self):
		self.scr.fill(self.background_clr)

		for obj in self.objects:
			obj.draw(self.scr)

	def tick(self):
		self.clock.tick(self.fps)

	def set_ground(self, ground):
		self.add_obj(ground)
		self.ground = ground

	def add_obj(self, obj):
		self.objects.append(obj)


class GameObject():
	def __init__(self, label, static=False):
		self.position = Vector(0, 0)
		self.velocity = Vector(0, 0)
		self.label = label
		self.static = static

		self.width = 0
		self.height = 0

		self.on_ground = False

	def update(self):
		if not self.static:
			self.position.x = int(self.position.x + self.velocity.x)
			self.position.y = int(self.position.y + self.velocity.y)

	def bottom(self):
		return int(self.position.y + self.height)

class Player(GameObject):
	def __init__(self, x, y, height, width, clr):
		# construct parent
		GameObject.__init__(self, 'Player')

		self.height = height
		self.width = width
		self.color = clr

		self.position.x = 100
		self.position.y = 100

	def draw(self, scr):
		pg.draw.rect(scr, self.color, self.rect())

	def rect(self):
		return pg.Rect(self.position.x, self.position.y, self.width, self.height)

	# Controls
	def move_left(self):
		self.velocity.x -= 1.0

	def move_right(self):
		self.velocity.x += 1.0

	def jump(self):
		if self.on_ground:
			print("Jump!")
			self.velocity.y = -5.0


class Ground(GameObject):
	def __init__(self, x=0, y=0):
		# construct parent
		GameObject.__init__(self, 'Slope', static=True)

		self.position.x = x
		self.position.y = y

		IMG_FILENAME = "hills1.png"
		self.sprite = pg.image.load(IMG_FILENAME)
		self.bitmap = Image.open(IMG_FILENAME)
		self.img_to_map()

	def draw(self, scr):
		scr.blit(self.sprite, (self.position.x, self.position.y))

	def height_at(self, x):
		x_idx = x - self.position.x

		# object is outside the slope, cannot collide
		if x_idx < 0 or x_idx > (len(self.height_map) - 1):
			return 0

		return self.position.y + self.height_map[x_idx]

	def img_to_map(self):
		def pxl_is_ground(px):
			return px > 0

		bitmap = np.array(self.bitmap)

		bitmap = np.apply_along_axis(pxl_is_ground, 2, bitmap)
		bitmap = np.any(bitmap, axis=2)

		self.height_map = np.zeros(bitmap.shape[1], dtype=int)
		for x,col in enumerate(bitmap.T):
			for y,is_ground in enumerate(col):

				# first ground pixel found! Save the location to the 'height map'
				if is_ground:
					self.height_map[x] = int(y)
					break   # next column


# -------------------------------
#         INIT THE GAME
# -------------------------------
FPS = 60.0
# SCR_SIZE = (700, 800)
SCR_SIZE = (1000, 960)

game = Game(SCR_SIZE, FPS)

# make the player
player = Player(100, 200, 10, 10, CLR_BLUE)
game.add_obj(player)

# make the ground
ground = Ground(0, 300)
game.set_ground(ground)

exit = False
while not exit:
	loop_start_time = time.time()
	last_check_time = loop_start_time

	# -------------------------------
	#         Handle Events
	# -------------------------------
	for event in pg.event.get():
		if event.type == pg.QUIT:
			exit = True
		if event.type == pg.KEYDOWN:
			# emergency exit
			if event.key == pg.K_q:
				exit = True
			if event.key == pg.K_SPACE:
				player.jump()
			if event.key == pg.K_LEFT:
				player.move_left()
			if event.key == pg.K_RIGHT:
				player.move_right()

	events_time = round((time.time() - last_check_time)*1000, 2)
	last_check_time = time.time()
	# -------------------------------
	#         Update Game
	# -------------------------------
	
	game.update()

	update_time = round((time.time() - last_check_time)*1000, 2)
	last_check_time = time.time()
	# -------------------------------
	#         Draw Graphics
	# -------------------------------
	game.draw()
	pg.display.update()
	draw_time = round((time.time() - last_check_time)*1000, 2)

	game.tick()

	total_time = round((time.time() - loop_start_time)*1000, 2)
	print("Events: {}ms, Update: {} ms, Draw: {} ms, Total: {} ms".format(
		events_time,
		update_time,
		draw_time,
		total_time
	))

pg.quit()
sys.exit()