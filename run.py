import sys
import pygame
import random as r
import threading
from logic import *

def main():
    
    pygame.init()

    screen = pygame.display.set_mode([1280, 720])
    pygame.display.set_caption('Space Station Simulation')

    astronauts = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    lockObjects = []
    # 0 - medbay, 1 - armory, 2 - armory
    for i in range(0, 3):
        lockObjects.append(threading.Lock())
    
    for i in range(0, 3):
        enemies.add(Enemy(i))
    
    for i in range(0, 8):
        x = r.randrange(550, 1180)
        y = r.randrange(100, 620)
        astronauts.add(Astronaut(x, y, lockObjects, enemies, i))
    #print("=== GAME STARTS ===")    

        
    for n in astronauts:
        n.start()
    for n in enemies:
        n.start()
        
    game = Game(astronauts, enemies)
    game.start()

    bg = Background("sprites/map.png", [0,0])
    
    wall = Background("sprites/wall.png", [0,0])
    
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for n in astronauts:
                    n.running = False
                for n in enemies:
                    n.running = False
                running = False
                game.running = False
                pygame.quit()
                sys.exit()

        screen.fill([32, 32, 32])
        screen.blit(bg.image, bg.rect)
        
        astronauts.draw(screen)
        astronauts.update()
        
        enemies.draw(screen)
        enemies.update()
        
        screen.blit(wall.image, wall.rect)

        pygame.display.flip()
        
if __name__ == "__main__":
    main()