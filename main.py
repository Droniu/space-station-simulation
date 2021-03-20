import pygame as pog
import random as r
import threading
import time

class Astronaut(threading.Thread):
    def __init__(self, x=0, y=0, running=True):
        threading.Thread.__init__(self)
        self.x = x
        self.y = y
        self.running = running
        self.movementX = 0
        self.movementY = 0
    
    def run(self):
        while self.running:
            time.sleep(0.05)
            self.x += self.movementX
            self.y += self.movementY
            
            

def main():
    
    pog.init()

    screen = pog.display.set_mode([800, 450])

    entity = Astronaut(x=250, y=250)
    entity.start()

    running = True
    while running:

        for event in pog.event.get():
            if event.type == pog.QUIT:
                entity.running = False
                running = False
            if event.type == pog.MOUSEBUTTONUP:
                entity.movementX = r.randint(-3, 3)
                entity.movementY = r.randint(-3, 3)

        screen.fill((255, 40, 69))
        pog.draw.circle(screen, (0, 0, 255), (entity.x, entity.y), 25)
        

        pog.display.flip()

    pog.quit()

if __name__ == "__main__":
    main()