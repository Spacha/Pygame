import pygame
 
WIDTH = 1024
HEIGHT = 768

offset_x, old_offset_x = 0,0
offset_y, old_offset_y = 0,0
 
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.set_alpha(None)

def to_pixels(x, y):
	global offset_x, offset_y
	center_x = (WIDTH // 2) + offset_x
	center_y = (HEIGHT // 2) + offset_y
	return center_x + x, center_y - y
 
 
def to_cartesian(pW, pH) -> tuple:
	global offset_x, offset_y
	center_x = (WIDTH // 2) + offset_x
	center_y = (HEIGHT // 2) + offset_y
	return (pW - center_x), -(pH - center_y)
 
 
pX, pY = 0, 0
color = (75, 125, 255)
 
 
# Some sample shape to understand the transformation
def draw_coordinates():
	pygame.draw.line(screen, color, to_pixels(0, 0), to_pixels(40, 0))
	pygame.draw.line(screen, color, to_pixels(0, 0), to_pixels(-40, 0))
	pygame.draw.line(screen, color, to_pixels(0, 0), to_pixels(0, 40))
	pygame.draw.line(screen, color, to_pixels(0, 0), to_pixels(0, -40))


color = (75, 125, 255)

mouse_held = False
exit = False
while not exit:
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.KEYDOWN:
			exit = True

	if pygame.mouse.get_pressed(3)[0]:
		mpos = pygame.mouse.get_pos()

		# mouse is just PRESSED down
		if not mouse_held:
			mouse_origin = mpos
			mouse_held = True
		
		# mouse is being HELD
		if mouse_held:
			offset_x = old_offset_x + mpos[0]-mouse_origin[0]
			offset_y = old_offset_y +mpos[1]-mouse_origin[1]

	# mouse is just RELEASED
	elif mouse_held:
		old_offset_x = offset_x
		old_offset_y = offset_y
		mouse_held = False

	screen.fill((0, 0, 0)) # Clear screen
	draw_coordinates()
	pygame.display.flip()
