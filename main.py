import sys
import pygame
import random as r
import threading
import time

# todo - enemy class, medbay, weapons

# 550 - arena start from left
# 100 - arena start from top


class Astronaut(threading.Thread, pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, running=True):
        threading.Thread.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        for i in range(1, 4):
            self.sprites.append(pygame.image.load("sprites/fighter/simple/" + str(i) + ".png"))
        self.current_sprite = 0
        self.is_animating = True
        self.image = self.sprites[self.current_sprite]    
        
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.running = running
        self.movementX = 0
        self.movementY = 0
        
        self.healthpoints = 100
        self.weapon = None
        self.ammo = 0
        self.kit = False
        
    def update(self):
        if self.is_animating == True:
            self.current_sprite += 0.085
            
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]
    
    def animate(self):
        self.is_animating = True
    
    def run(self):
        while self.running:
            time.sleep(0.05)
            if self.healthpoints == 0:
                self.die(self)
            self.rect.left += self.movementX
            self.rect.top -= self.movementY
            if self.ammo>0:
                pass
            else:
                self.go_armory()
            
    def stay(self):
        self.movementX = 0
        self.movementY = 0
    def attack(self, Enemy):
        pass
    def escape(self): 
        pass
    def go_armory(self):
        pass
    def go_medbay(self):
        pass
    def die(self):
        
        self.running = False
                
class Enemy():
    def __init__(self, x=0, y=0, type="Phantom"):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/fighter_simple.gif")
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.movementX = 0
        self.movementY = 0
        
        self.healthpoints = 100

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
            
            

def main():
    
    pygame.init()

    screen = pygame.display.set_mode([1280, 720])

    entities = pygame.sprite.Group()
    
    for i in range(0, 5):
        x = r.randrange(550, 1280)
        y = r.randrange(100, 720)
        entity = Astronaut(x, y)
        entities.add(entity)
        
    for n in entities:
        n.start()
    
    
    entities.add(entity)

    bg = Background("sprites/map_draft.png", [0,0])
    
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for n in entities:
                    n.running = False
                running = False
                pygame.quit()
                sys.exit()
                


        screen.fill([32, 32, 32])
        screen.blit(bg.image, bg.rect)
        entities.draw(screen)
        entities.update()

        pygame.display.flip()



if __name__ == "__main__":
    main()