import pygame
pygame.init()

<<<<<<< HEAD
win = pygame.display.set_mode((640, 480))
=======
win = pygame.display.set_mode((640.480))
>>>>>>> bd02c6bedd7e407db022f64643a793a4f3cca95b

pygame.display.set_caption("GameJam")

run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
<<<<<<< HEAD
            run = False

pygame.quit()
=======
            run=False

pygame.quit()            
>>>>>>> bd02c6bedd7e407db022f64643a793a4f3cca95b
