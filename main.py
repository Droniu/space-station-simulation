import pygame
import random as r
import threading
import time

# todo - enemy class, medbay, weapons

class Astronaut(threading.Thread, pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, running=True):
        threading.Thread.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/fighter_simple.gif")
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.running = running
        self.movementX = 0
        self.movementY = 0
    
    def run(self):
        while self.running:
            time.sleep(0.05)
            self.rect.left += self.movementX
            self.rect.top -= self.movementY
            
class Enemy():
    def __init__(self, x=0, y=0, alive=True):
        pass

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
            
            

def main():
    
    pygame.init()

    screen = pygame.display.set_mode([1280, 720])

    entity = Astronaut(x=250, y=250)
    entity.start()

    bg = Background("sprites/map_draft.png", [0,0])
    
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                entity.running = False
                running = False
            """if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    entity.movementX -= 19
                if event.key == pygame.K_RIGHT:
                    entity.movementX += 19
                if event.key == pygame.K_UP:
                    entity.movementY += 19
                if event.key == pygame.K_DOWN:
                    entity.movementY -= 19
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or pygame.K_DOWN:
                    entity.movementY = 0
                if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                    entity.movementX = 0
            """
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT]:
            entity.movementX -= 1

        if keys_pressed[pygame.K_RIGHT]:
            entity.movementX += 1

        if keys_pressed[pygame.K_UP]:
            entity.movementY += 1

        if keys_pressed[pygame.K_DOWN]:
            entity.movementY     -= 1


        screen.fill([32, 32, 32])
        screen.blit(bg.image, bg.rect)
        screen.blit(entity.image, entity.rect)
        

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()