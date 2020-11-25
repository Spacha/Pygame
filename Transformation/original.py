import pygame
 
WIDTH = 1024
HEIGHT = 768
x_offset = 0
y_offset = 0
x_offset_prev = 0
y_offset_prev = 0
 
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.set_alpha(None)
 
def to_pixels(x, y):
    center_x = (WIDTH / 2) + x_offset
    center_y = (HEIGHT / 2) + y_offset
    return center_x + x, center_y - y
 
 
def to_cartesian(pW, pH) -> tuple:
    center_x = (WIDTH / 2) + x_offset
    center_y = (HEIGHT / 2) + y_offset
    return (pW - center_x), -(pH - center_y)
 
 
pX, pY = 0, 0
color = (75, 125, 255)
 
 
# Some sample shape to understand the transformation
def draw_coordinates():
    pygame.draw.line(screen, color, to_pixels(0, 0), to_pixels(40, 0))
    pygame.draw.line(screen, color, to_pixels(0, 0), to_pixels(-40, 0))
    pygame.draw.line(screen, color, to_pixels(0, 0), to_pixels(0, 40))
    pygame.draw.line(screen, color, to_pixels(0, 0), to_pixels(0, -40))
 
 
pos = [0, 0]
 
while 1:
    event = pygame.event.get()
    posX, posY = to_cartesian(*pygame.mouse.get_pos())
    if pygame.mouse.get_pressed(3)[0]:
        # Translate X
        translate = pos[0] - (pos[0] - posX)
        x_offset += translate
        # Translate Y
        translate = pos[1] - (pos[1] - posY)
        y_offset -= translate
 
    pos = [posX, posY]
    screen.fill((0, 0, 0)) # Clear screen
    nX, nY = to_pixels(pX, pY)
    draw_coordinates()
    pygame.display.flip()
