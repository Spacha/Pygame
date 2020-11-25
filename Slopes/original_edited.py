import pygame
import sys

# PIL used ot load the bitmap into a numpy array
from PIL import Image
import numpy as np


pygame.init()
# make our screen for our game
window = pygame.display.set_mode((700,800))
# name our game
pygame.display.set_caption("Our Space Game")

class player:
    def __init__(self,x,y,height,width,color):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color

        # make our player jump
        self.isJump = False
        self.JumpCount = 10

        self.fall = 0


        self.rect = pygame.Rect(x,y,height,width)

                
    def draw(self):
        self.rect.topleft = (self.x,self.y)
        pygame.draw.rect(window,self.color,self.rect)

CLR_BLACK = ( 0 , 0 , 0 )
CLR_WHITE = (255,255,255)
CLR_BLUE  = ( 0 , 0 ,255)
playerman = player(200,200,10,10,CLR_BLUE)

class slope():
    # new_platforms = slope(ix*9.8, iy*50, 520,220,(23, 32, 42))
    def __init__(self,x,y,height,width,color):
        self.body_bmap = None

        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color  = color
        # self.image = pygame.image.load("hills1.png")
        # "hills_156x89.png"
        img_filename = "hills1.png"
        self.image = pygame.image.load(img_filename)

        self.rect = pygame.Rect(x,y,height,width)
        self.body_bmap = Image.open(img_filename)
        self.generate_ground()

    def draw(self):
        self.rect.topleft = (self.x,self.y)
        #pygame.draw.rect(window,self.color,self.rect)
        window.blit(self.image,self.rect)

    def generate_ground(self):
        if self.body_bmap is None:
            print("No bitmap loaded for ground!")
            return

        # MASK layer suggested
        '''
        the iamge as a numpy array:
        [
            (top-left)                            (top-left)
            [ [R,G,B,A] [R,G,B,A] [R,G,B,A] ... [R,G,B,A]  ]
            [ [R,G,B,A] [R,G,B,A] [R,G,B,A] ... [R,G,B,A]  ]
            [ [R,G,B,A] [R,G,B,A] [R,G,B,A] ... [R,G,B,A]  ]
                                 ...
            [ [R,G,B,A] [R,G,B,A] [R,G,B,A] ... [R,G,B,A]  ]
            (bottom-left)                     (bottom-right)
        ]

        So:
            dimension 0 = 4 (pixel values)
            dimension 1     (width in pixels)
            dimension 2     (height in pixels)

            a.shape[0] = height
            a.shape[1] = width
        '''

        # Generate
        # 1. Find the topmost black pixel from each column starting from left
        # 2. Save the pixel's y position to an array
        bitmap = np.array(self.body_bmap)
        # ground = np.zeros(len(bitmap))
        height, width = bitmap.shape[0:2]
        # print(width, height)

        def is_ground(px):
            return px > 0

        bitmap = np.apply_along_axis(is_ground, 2, bitmap)
        bitmap = np.any(bitmap, axis=2)
        '''
        a_img = np.array([
            [ [0,0], [0,0], [0,0], [0,0], [0,0], [0,1] ],
            [ [0,1], [0,0], [0,0], [0,0], [0,1], [0,0] ],
            [ [0,1], [0,1], [0,0], [0,1], [0,1], [0,0] ],
            [ [0,1], [0,1], [0,1], [0,0], [0,1], [0,0] ]
        ])
        # these convert the 3 dimensional (rows, columns, 4 pixel values)
        # array into 2 dimensional (rows, columns, is_ground) array
        a_img_bw = np.apply_along_axis(is_ground, 2, a_img)
        a_img_bw = np.any(a_img_bw, axis=2)
        print(a_img)
        print(a_img_bw)
        print(a_img_bw.T)
        '''
        '''
        print("a:")
        a = np.array([
            [ 0, 0, 0, 0, 0, 1 ],
            [ 1, 0, 0, 0, 1, 0 ],
            [ 1, 1, 0, 1, 1, 0 ],
            [ 1, 1, 1, 0, 1, 0 ]
        ])
        print("a.T:")
        print(a, a.T)
        '''

        # let's take a transpose so we can calculate the first ground bit of each vector
        # bitmapT = bitmap.T

        # height map will have [width] elements (one from each column)
        self.height_map = np.zeros(bitmap.shape[1], dtype=int)
        for x,col in enumerate(bitmap.T):
            for y,is_ground in enumerate(col):

                # first ground pixel found! Save the location to the 'height map'
                if is_ground:
                    self.height_map[x] = int(y)
                    break   # next column

        # now height map contains 
    
    def collided(self, y, x):
        '''

        '''
        x_idx = x - self.x

        # object is outside the slope, cannot collide
        if x_idx < 0:
            print("alle")
            return False
        if x_idx > len(self.height_map) - 1:
            print("yli")
            return False

        if y >= self.y+self.height_map[x_idx]:
            # print(y, self.y+self.height_map[x_idx])
            return True
        else:
            print(y, self.y+self.height_map[x_idx])

        return False
        #if y_ind <= self.height_map[x_ind]:




slopes = []

platformGroup = pygame.sprite.Group

'''                                                                                    
level = [
"                                                                  ",
"                                                                  ",
"                                                                  ",
"                                                                  ",
"                                                                  ",
"                                                                  ",
"                                                                  ",
"   c                                                              "
]

for iy, row in enumerate(level):
    for ix, col in enumerate(row):
        if col == "c":
            new_platforms = slope(ix*9.8, iy*50, 520,220,(23, 32, 42))
            slopes.append(new_platforms)
'''
ground = slope(0, 300, 520, 220, (23, 32, 42))
slopes.append(ground)

# our game fps
fps = 40
clock = pygame.time.Clock()


def redraw(on_ground):
    if on_ground:
        window.fill((170,170,170))
    else:
        window.fill(CLR_BLACK)

    playerman.draw()

    for slope in slopes:
        slope.draw()

# init
on_ground = False

# our game main loop
runninggame = True
while runninggame:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.quit:
            runninggame = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                runninggame = False



    keys = pygame.key.get_pressed()
    for slope in slopes:
        if playerman.rect.colliderect(slope.rect):
            playerman.x += 7

    collide = False
    if not playerman.isJump:                    
        playerman.y += playerman.fall
        playerman.fall += 1
        playerman.isJump = False
        collide = False

        # collisions
        '''
        for slope in slopes:
            if playerman.rect.colliderect(slope.rect):
                collide = True
                playerman.isJump = False
                playerman.y = slope.rect.top - playerman.height + 1
                if playerman.rect.right > slope.rect.left and playerman.rect.left < slope.rect.left - playerman.width:
                    playerman.x = slope.rect.left - playerman.width
                if playerman.rect.left < slope.rect.right and playerman.rect.right > slope.rect.right + playerman.width:
                    playerman.x = slope.rect.right
            '''

        # !!!
        if ground.collided(playerman.rect.bottom, playerman.rect.centerx):
            print("Collision!")
            on_ground = True
        else:
            on_ground = False


        if playerman.rect.bottom >= 890:
            collide = True
            playerman.isJump = False
            playerman.JumpCount = 10
            playerman.y = 890 - playerman.height

        if collide:
            if keys[pygame.K_SPACE]:
                playerman.isJump = True
                        
            playerman.fall = 0

    else:
        if playerman.JumpCount > 0:
            playerman.y -= (playerman.JumpCount*abs(playerman.JumpCount)) * 0.3
            playerman.JumpCount -= 1
        else:
            playerman.JumpCount = 10
            playerman.isJump = False

    redraw(on_ground)
    pygame.display.update()

pygame.quit()
sys.exit()
