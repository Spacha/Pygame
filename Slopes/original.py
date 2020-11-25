import pygame
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

white = (255,255,255)
playerman = player(200,200,10,10,white)







class slope():
    def __init__(self,x,y,height,width,color):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color  = color
        self.image = pygame.image.load("hills1.png")
        self.rect = pygame.Rect(x,y,height,width)
    def draw(self):
        self.rect.topleft = (self.x,self.y)
        pygame.draw.rect(window,self.color,self.rect)
        window.blit(self.image,self.rect)




slopes = []

platformGroup = pygame.sprite.Group

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
        
        


# our game fps
fps = 40
clock = pygame.time.Clock()


def redraw():
    window.fill((0,0,0))
    playerman.draw()

    for slope in slopes:
        slope.draw()


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
        for slope in slopes:
            if playerman.rect.colliderect(slope.rect):
                collide = True
                playerman.isJump = False
                playerman.y = slope.rect.top - playerman.height + 1
                if playerman.rect.right > slope.rect.left and playerman.rect.left < slope.rect.left - playerman.width:
                    playerman.x = slope.rect.left - playerman.width
                if playerman.rect.left < slope.rect.right and playerman.rect.right > slope.rect.right + playerman.width:
                    playerman.x = slope.rect.right


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


    

    

            

    redraw()
    pygame.display.update()

pygame.quit()
