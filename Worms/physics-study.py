import time
import pygame as pg
from pygame import Vector2 as Vec

FPS = 100
g = 9.81
G = Vec(0,-g)

class Object:
	def __init__(self):
		self.pos = Vec(0, 10)
		self.vel = Vec(0, 0)

	def update(self, delta):
		# acceleration update:
		a = G  # + other acceleration sources

		# velocity update: v = v + at = [m/s] + [m/s^2][s]
		self.vel += a * delta

		# position update:
		self.pos += delta * self.vel

obj = Object()

clock = pg.time.Clock()
delta = 0.0
tick_count = 0

running = True
start_time = time.monotonic()
while running:
	if (time.monotonic() - start_time) >= 10:
		running = False

	obj.update(delta)

	delta = clock.tick( FPS ) / 1000
	#print(f"Time: {time.monotonic() - start_time} s\t delta: {delta} s\t pos: ({round(obj.pos.x, 2)},{round(obj.pos.y, 2)})")
	tick_count += 1

print(f"\nTime: {time.monotonic() - start_time} s\t delta: {delta} s\t pos: ({round(obj.pos.x, 2)},{round(obj.pos.y, 2)})")
print(f"Velocity: ({round(obj.vel.x, 2)},{round(obj.vel.y, 2)})")
