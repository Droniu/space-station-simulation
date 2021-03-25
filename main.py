import sys
import pygame
import random as r
import threading
import time
from math import sqrt

# todo - enemy class, medbay, weapons

# 550 - arena start from left
# 100 - arena start from top

class Spritesheet(object):
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

class Astronaut(threading.Thread, pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, running=True):
        threading.Thread.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.sprite_catalog = {
            "idle_empty": Spritesheet('sprites/pngs/fighter_idle_empty.png').images_at(
                ((0, 0, 63, 63),(64, 0, 128,63),(0, 64, 63, 128),(64, 64, 128, 128)), colorkey=(0, 0, 0)),
            "idle_weapon": Spritesheet('sprites/pngs/fighter_idle_weapon.png').images_at(
                ((0, 0, 63, 63),(64, 0, 128,63),(0, 64, 63, 128),(64, 64, 128, 128)), colorkey=(0, 0, 0)),
            "idle_shooting": Spritesheet('sprites/pngs/fighter_idle_shooting.png').images_at(
                ((0, 0, 63, 63),(64, 0, 128,63),(0, 64, 63, 128),(64, 64, 128, 128)), colorkey=(0, 0, 0)),
            "walking_empty": Spritesheet('sprites/pngs/fighter_walking_empty.png').images_at(
                ((0, 0, 63, 63),(64, 0, 128,63),(0, 64, 63, 128),(64, 64, 128, 128)), colorkey=(0, 0, 0)),
            "walking_weapon": Spritesheet('sprites/pngs/fighter_walking_weapon.png').images_at(
                ((0, 0, 63, 63),(64, 0, 128,63),(0, 64, 63, 128),(64, 64, 128, 128)), colorkey=(0, 0, 0)),
            "walking_shooting": Spritesheet('sprites/pngs/fighter_walking_shooting.png').images_at(
                ((0, 0, 63, 63),(64, 0, 128,63),(0, 64, 63, 128),(64, 64, 128, 128)), colorkey=(0, 0, 0)),
            "dying": Spritesheet('sprites/pngs/fighter_dying.png').images_at(
                ((0, 0, 63, 63),(64, 0, 128,63),(0, 64, 63, 128),(64, 64, 128, 128)), colorkey=(0, 0, 0))
        }
        self.spritesheet = self.sprite_catalog["walking_shooting"]
        self.current_sprite = 0
        self.is_animating = True
        self.image = self.spritesheet[self.current_sprite] 
        
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.running = running
        self.movementX = 0
        self.movementY = 0
        
        self.healthpoints = 100
        self.speed = 3
        self.weapon = None
        self.ammo = 0
        self.kit = False
        
    def update(self):
        if self.is_animating == True:
            self.current_sprite += 0.085
            
            if self.current_sprite >= len(self.spritesheet):
                self.current_sprite = 0
            self.image = self.spritesheet[int(self.current_sprite)]
    
    def animate(self):
        self.is_animating = True
    
    def run(self):
        while self.running:
            time.sleep(0.05)
            if self.healthpoints <= 0:
                self.die(self)
            
            self.rect.left += self.movementX
            self.rect.top -= self.movementY

            if self.ammo>0:
                pass
            else:
                pass
                #self.go_armory()
            
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
        
        
                
class Enemy(threading.Thread, pygame.sprite.Sprite):
    def __init__(self, x=1080, y=350, atype="Phantom"):
        threading.Thread.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/pngs/enemy.png")
        self.rect = self.image.get_rect()
        self.rect.bottomleft = [x, y]
        self.movementX = 0
        self.movementY = 0
        self.running = True
        
        if atype == "Phantom":
            self.healthpoints = 100
            self.speed = 3
        elif atype == "Stalker":
            self.healthpoints = 75
            self.speed = 5
        elif atype == "Nightmare":
            self.healthpoints = 500
            self.speed = 1
    
    def run(self):
        while self.running:
            time.sleep(0.05)
            self.rect.left += self.movementX
            self.rect.top -= self.movementY
            
            if self.healthpoints <= 0:
                self.die()
            
        
    def die(self):
        self.running = False
    
    def find_victim(self, astronauts):
        shortest = 1500
        chosen = None
        for n in astronauts:
            dist = sqrt( (self.rect.left - n.rect.left)**2 + (self.rect.top - n.rect.top)**2 )
            if dist<shortest:
                dist=shortest
                chosen = n
        self.hunt(chosen)
    
    def hunt(self, victim):
        if victim.rect.left < self.rect.left:
            self.movementX = -self.speed
        else:
            self.movementX = self.speed
        
        if victim.rect.top < self.rect.top:
            self.movementY = self.speed
        else:
            self.movementY = -self.speed
        
                
            
        
        
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
            

class Game(threading.Thread):
    def __init__(self, astronauts, enemy):
        threading.Thread.__init__(self)
        self.astronauts = astronauts
        self.enemy = enemy
        self.running = True
    
    def run(self):
        while self.running:
            time.sleep(0.1)
            self.enemy.find_victim(self.astronauts)
            
                
        
            

def main():
    
    pygame.init()

    screen = pygame.display.set_mode([1280, 720])

    entities = pygame.sprite.Group()
    enemy = Enemy()
    
    for i in range(0, 5):
        x = r.randrange(550, 1280)
        y = r.randrange(100, 720)
        entity = Astronaut(x, y)
        entities.add(entity)
        
    for n in entities:
        n.start()
    enemy.start()
        
    game = Game(entities, enemy)
    game.start()

    bg = Background("sprites/map.png", [0,0])
    
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for n in entities:
                    n.running = False
                running = False
                enemy.running = False
                game.running = False
                pygame.quit()
                sys.exit()

        screen.fill([32, 32, 32])
        screen.blit(bg.image, bg.rect)
        
        entities.draw(screen)
        entities.update()
        
        screen.blit(enemy.image, enemy.rect)

        pygame.display.flip()



if __name__ == "__main__":
    main()