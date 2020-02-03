import pygame
pygame.init()

win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("GameJam")
bg = pygame.image.load('background.png')
avion = pygame.image.load('aviontest.png')
bgX = 0
bgX2 = bg.get_width()
clock = pygame.time.Clock()
run = True
x = 50
y = 50
width = 40
height = 60
vel = 2
speedscrolling=500

def redrawGameWindow():
    #win.blit(bg, (0,0))
    #win.blit(testco, (270,625)) #coordonnées du milieu de chaque tuyeau = (x+225,625)
    win.blit(bg,(bgX,0))
    win.blit(bg,(bgX2,0))
    win.blit(avion,(x,y))
    pygame.display.update()

while run:
    clock.tick(speedscrolling)
    bgX -= 1.4
    bgX2 -= 1.4

    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    keys=pygame.key.get_pressed()

    if keys[pygame.K_z]:
        y -= vel
    if keys[pygame.K_s]:
        y += vel


    redrawGameWindow()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
