import sys
import pygame
import random as r
import threading
import time
from math import sqrt

# todo - enemy class, medbay, weapons

# 550 - arena start from left
# 100 - arena start from top

# constants - armory x, y, same for medbay
# movement into specific places
# sleep for a while
# change state variables (e.g. ammo, hp).

# what happens next? where does the character go?


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
	def __init__(self, x=0, y=0, lockObjects=[], enemies=None, id=-1):
		threading.Thread.__init__(self)
		pygame.sprite.Sprite.__init__(self)
		self.sprite_catalog = {
			"idle_empty": Spritesheet('sprites/pngs/fighter_idle_empty.png').images_at(
				((0, 0, 63, 63),(64, 0, 128,63),(0, 64, 63, 128),(64, 64, 128, 128)), colorkey=(0, 0, 0)),
			"idle_weapon": Spritesheet('sprites/pngs/fighter_idle_weapon.png').images_at(
				((0, 0, 63, 63),(64, 0, 128,63),(0, 64, 63, 128),(64, 64, 128, 128)), colorkey=(0, 0, 0)),
			"idle_shooting": Spritesheet('sprites/pngs/fighter_idle_shooting.png').images_at(
				((0, 0, 79, 63),(80, 0, 160,63),(0, 64, 79, 128),(80, 64, 160, 128)), colorkey=(0, 0, 0)),
			"walking_empty": Spritesheet('sprites/pngs/fighter_walking_empty.png').images_at(
				((0, 0, 63, 63),(64, 0, 128,63),(0, 64, 63, 128),(64, 64, 128, 128)), colorkey=(0, 0, 0)),
			"walking_weapon": Spritesheet('sprites/pngs/fighter_walking_weapon.png').images_at(
				((0, 0, 63, 63),(64, 0, 128,63),(0, 64, 63, 128),(64, 64, 128, 128)), colorkey=(0, 0, 0)),
			"walking_shooting": Spritesheet('sprites/pngs/fighter_walking_shooting.png').images_at(
				((0, 0, 79, 63),(80, 0, 160,63),(0, 64, 79, 128),(80, 64, 160, 128)), colorkey=(0, 0, 0)),
			"dying": Spritesheet('sprites/pngs/fighter_dying.png').images_at(
				((0, 0, 63, 63),(64, 0, 128,63),(0, 64, 63, 128),(64, 64, 128, 128)), colorkey=(0, 0, 0))
		}
		self.spritesheet = self.sprite_catalog["idle_weapon"]
		self.current_sprite = 0
		self.is_animating = True
		self.image = self.spritesheet[self.current_sprite] 
		
		self.id = id
		
		self.rect = self.image.get_rect()
		self.rect.topleft = [x, y]
		self.running = True
		self.movementX = 0
		self.movementY = 0
		
		self.lockObjects = lockObjects
		self.enemies = enemies
		
		self.healthpoints = 100
		self.speed = 3
		self.weapon = True
		self.ammo = 30	
		self.medkit = False
		
		self.underAttack = False
		self.isHit = False
		
		self.goingToCenter = False
		self.goingToMedBay = False
		self.goingToWeaponry = False
		
		self.isInMedBay = False
		self.isInWeaponry = False
		#print(" === Astronaut "+str(id)+" created ===")
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
			if self.goingToCenter: 
				if self.rect.top > 225 and self.rect.top < 275 and self.rect.left > 725 and self.rect.left < 775:
					self.goingToCenter = False
				else:
					if self.rect.top < 250: 
						self.rect.top += self.speed
					if self.rect.top > 250:
						self.rect.top -= self.speed
					if self.rect.left < 750:
						self.rect.left += self.speed
					if self.rect.left > 750:
						self.rect.left -= self.speed
			#elif goingToWeaponry:
			else:
				self.rect.left += self.movementX
				self.rect.top -= self.movementY
			if self.rect.top < 0: 
				self.goingToCenter = True
			if self.rect.top > 560:
				self.goingToCenter = True
			if self.rect.left < 560 and not self.goingToMedBay and not self.goingToWeaponry and not self.isInMedBay:
				self.goingToCenter = True
			if self.rect.left > 1000:
				self.goingToCenter = True
			
			if self.movementX != 0 or self.movementY != 0 or self.goingToCenter or self.goingToMedBay or self.goingToWeaponry:
				if self.weapon:
					self.spritesheet = self.sprite_catalog["walking_weapon"]
				else:
					self.spritesheet = self.sprite_catalog["walking_empty"]
			# collision detection with alien
			for n in self.enemies:
				if self.rect.colliderect(n.rect):
					self.isHit = True
					break
				else:
					self.isHit = False

			if self.healthpoints <= 0:
				self.die()
				
			if self.isHit:
				if (self.weapon and (self.ammo > 0)):
					self.attackEscape()
				else:
					self.escape()
			else:
				if not self.goingToMedBay and not self.goingToWeaponry and not self.isInMedBay:
					if not self.underAttack and self.weapon and (self.ammo > 0):
						self.attack(self.enemies)
					elif not self.underAttack:
						self.stay()
					else:
						self.escape()
					if self.healthpoints < 50:
						if self.medkit == True:
							self.medkit = False
							self.healthpoints = 100	
						else:
							if self.weapon:
								if not self.lockObjects[1].locked():
									self.goArmory(1,True)
								elif not self.lockObjects[2].locked():
									self.goArmory(2,True)
								else:
									self.escape()
							else:
								if not self.lockObjects[0].locked():
									self.goMedbay()
								else: 
									self.escape()
								
					else:
						if (self.weapon and (self.ammo > 0)):
							if not self.enemies:
								self.stay()
							else:
								self.attack(self.enemies)
						else:
							if not self.lockObjects[1].locked():
								self.goArmory(1)
							elif not self.lockObjects[2].locked():
								self.goArmory(2)
							else:
								self.escape()
			

			
	def stay(self):
		#print(" === Astronaut "+str(self.id)+" stays ===")
		self.movementX = 0
		self.movementY = 0
		if self.weapon == True: 
			self.spritesheet = self.sprite_catalog["idle_weapon"]
		else:
			self.spritesheet = self.sprite_catalog["idle_empty"]
	def goArmory(self,slot,leaveWeapon=False):
		self.goingToWeaponry = True
		self.lockObjects[slot].acquire()
		while self.goingToWeaponry:
			if self.weapon:
				self.spritesheet = self.sprite_catalog["walking_weapon"]
			else:
				self.spritesheet = self.sprite_catalog["walking_empty"]
			if self.healthpoints == 0:
				self.die()
				return
			time.sleep(0.05)
			if self.rect.top > 125 and self.rect.top < 175 and self.rect.left > 225 and self.rect.left < 275:
				self.goingToWeaponry = False
				self.isInWeaponry = True
			else:
				if self.rect.top < 150: 
					self.rect.top += self.speed
				if self.rect.top > 150:
					self.rect.top -= self.speed
				if self.rect.left < 250:
					self.rect.left += self.speed
				if self.rect.left > 250:
					self.rect.left -= self.speed
		self.stay()
		time.sleep(5.0)
		self.goingToCenter = True
		if leaveWeapon:
			self.weapon = False
		else:
			self.weapon = True
		self.ammo = 30
		self.lockObjects[slot].release()
		while self.goingToCenter: 
			time.sleep(0.05)
			if self.weapon:
				self.spritesheet = self.sprite_catalog["walking_weapon"]
			else:
				self.spritesheet = self.sprite_catalog["walking_empty"]
			if self.healthpoints == 0:
				self.die()
				return
			if self.rect.left > 560:
				self.goingToCenter = False
			else:
				self.rect.left += self.speed
		self.isInWeaponry = False
	def goMedbay(self): # medbay coordinates - 550, 500
		self.goingToMedBay = True
		#self.goArmory(slot,True)
		self.lockObjects[0].acquire()
		while self.goingToMedBay:
			if self.weapon:
				self.spritesheet = self.sprite_catalog["walking_weapon"]
			else:
				self.spritesheet = self.sprite_catalog["walking_empty"]
			if self.healthpoints == 0:
				self.die()
				return
			time.sleep(0.05)
			if self.rect.top > 325 and self.rect.top < 375 and self.rect.left > 225 and self.rect.left < 275:
				self.goingToMedBay = False
				self.isInMedBay = True
			else:
				if self.rect.top < 350: 
					self.rect.top += self.speed
				if self.rect.top > 350:
					self.rect.top -= self.speed
				if self.rect.left < 250:
					self.rect.left += self.speed
				if self.rect.left > 250:
					self.rect.left -= self.speed
		self.stay()
		time.sleep(5.0)
		
		self.goingToCenter = True
		self.medkit = True
		self.healthpoints = 100
		self.lockObjects[0].release()
		while self.goingToCenter: 
			time.sleep(0.05)
			if self.weapon:
				self.spritesheet = self.sprite_catalog["walking_weapon"]
			else:
				self.spritesheet = self.sprite_catalog["walking_empty"]
			if self.healthpoints == 0:
				self.die()
				return
			if self.rect.left > 560:
				self.goingToCenter = False
			else:
				self.rect.left += self.speed
		self.isInMedBay = False
		
	def findNearest(self, group):
		shortest = -1
		chosen = None
		for n in group:
			dist = sqrt( (self.rect.centerx - n.rect.centerx)**2 + (self.rect.centery - n.rect.centery)**2 )
			if shortest == -1:
				shortest=dist
				chosen = n
			if dist<shortest:
				shortest=dist
				chosen = n
		return chosen
	
	def attackEscape(self):
		print(" === Astronaut "+str(self.id)+" is attackescape; ammo is "+str(self.ammo))
		chosen = self.findNearest(self.enemies)
		if (chosen is not None):   
			self.speed=2
			if chosen.rect.centerx < self.rect.centerx:
				self.movementX = self.speed
			if chosen.rect.centerx >= self.rect.centerx:
				self.movementX = -self.speed
				
			if chosen.rect.centerx < self.rect.centerx:
				self.movementY = -self.speed
			if chosen.rect.centerx >= self.rect.centerx:
				self.movementY = self.speed
			
			#print(" === Astronaut "+str(self.id)+" escapes and attacks Enemy "+str(chosen.id)+" ===")
			chosen.healthpoints -= 10
			self.ammo -= 1
			self.spritesheet = self.sprite_catalog["walking_shooting"]
			self.speed=3
			

	def attack(self, attackers):
		print(" === Astronaut "+str(self.id)+" is attack; ammo is "+str(self.ammo))
		#self.stay()
		chosen = self.findNearest(self.enemies)
		if (chosen is not None):
			#print(" === Astronaut "+str(self.id)+" attacks Enemy "+str(chosen.id)+" ===")
			chosen.healthpoints -= 10
			self.ammo -= 1
			self.spritesheet = self.sprite_catalog["idle_shooting"]
			time.sleep(0.8)
		
	def escape(self):
		#print(" === Astronaut "+str(self.id)+" is escaping ===")
		chosen = self.findNearest(self.enemies)
		if (chosen is not None):   
			self.speed=4
			if chosen.rect.centerx < self.rect.centerx:
				self.movementX = self.speed
			if chosen.rect.centerx >= self.rect.centerx:
				self.movementX = -self.speed
				
			if chosen.rect.centerx < self.rect.centerx:
				self.movementY = -self.speed
			if chosen.rect.centerx >= self.rect.centerx:
				self.movementY = self.speed
		self.speed=3
		if self.weapon:
			self.spritesheet = self.sprite_catalog["walking_weapon"]
		else:
			self.spritesheet = self.sprite_catalog["walking_empty"]
	def die(self):
		#print(" === Astronaut "+str(self.id)+" died ===")
		self.stay()
		self.spritesheet = self.sprite_catalog["dying"]
		time.sleep(0.85)
		self.running = False
				
class Enemy(threading.Thread, pygame.sprite.Sprite):
	def __init__(self, id=-1, x=1080, y=350, atype="Phantom"):
		threading.Thread.__init__(self)
		pygame.sprite.Sprite.__init__(self)
		self.isHunting = False
		self.chosenAstronaut = None
		self.astronauts = None
		self.id = id
		self.sprite_catalog = {
			"phantom_idle": Spritesheet('sprites/pngs/phantom_idle.png').images_at(
				((0, 0, 63, 63),(64, 0, 128,63),(0, 64, 63, 128),(64, 64, 128, 128)), colorkey=(0, 0, 0)),
			"phantom_walking": Spritesheet('sprites/pngs/phantom_walking.png').images_at(
				((0, 0, 68, 63),(69, 0, 138, 63),(0, 64, 68, 128),(69, 64, 138, 128)), colorkey=(0, 0, 0)),
			"phantom_attack": Spritesheet('sprites/pngs/phantom_attack.png').images_at(
				((0, 0, 63, 63),(64, 0, 128,63),(0, 64, 63, 128),(64, 64, 128, 128)), colorkey=(0, 0, 0))
		}
		
		self.spritesheet = self.sprite_catalog["phantom_idle"]
		self.current_sprite = 0
		self.is_animating = True
		self.image = self.spritesheet[self.current_sprite]
		
		self.rect = self.image.get_rect()
		self.rect.bottomleft = [x, y]
		self.movementX = 0
		self.movementY = 0
		self.running = True
		
		if atype == "Phantom":
			self.healthpoints = 100
			self.speed = 3
			self.attackPower = 20
			self.sprite_catalog = {
				"phantom_idle": Spritesheet('sprites/pngs/phantom_idle.png').images_at(
					((0, 0, 63, 63),(64, 0, 128,63),(0, 64, 63, 128),(64, 64, 128, 128)), colorkey=(0, 0, 0)),
				"phantom_walking": Spritesheet('sprites/pngs/phantom_walking.png').images_at(
					((0, 0, 68, 63),(69, 0, 138, 63),(0, 64, 68, 128),(69, 64, 138, 128)), colorkey=(0, 0, 0)),
				"phantom_attack": Spritesheet('sprites/pngs/phantom_attack.png').images_at(
					((0, 0, 63, 63),(64, 0, 128,63),(0, 64, 63, 128),(64, 64, 128, 128)), colorkey=(0, 0, 0))
			}
			
		elif atype == "Stalker":
			self.healthpoints = 75
			self.speed = 5
			self.attackPower = 7
		elif atype == "Nightmare":
			self.healthpoints = 500
			self.speed = 1
			self.attackPower = 20
			
		#print(" === Enemy "+str(id)+" created ===")
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
			self.rect.left += self.movementX
			self.rect.top -= self.movementY
			if self.rect.top < 0: 
				self.rect.top = 0
			if self.rect.top > 560:
				self.rect.top = 560
			if self.rect.left < 560:
				self.rect.left = 560
			if self.rect.left > 1000:
				self.rect.left = 1000
				
			if self.movementX != 0 or self.movementY != 0:
				self.spritesheet = self.sprite_catalog["phantom_walking"]
			
			if self.healthpoints <= 0:
				self.die()
			if not self.isHunting:
				self.find_victim(self.astronauts)
				self.isHunting = True;
			else:
				if self.rect.colliderect(self.chosenAstronaut.rect):
					self.attack(self.chosenAstronaut)
					time.sleep(0.5)
				else:
					self.hunt(self.chosenAstronaut);
	def die(self):
		#print(" === Enemy "+str(self.id)+" died ===")
		if not (self.chosenAstronaut is None):
			self.chosenAstronaut.underAttack = False;
		self.running = False
	
	def find_victim(self, astronauts):
		#print(" === Enemy "+str(self.id)+" searches for victim ===")
		shortest = -1
		chosen = None
		for n in astronauts:
			if not n.underAttack and not n.isInMedBay and not n.isInWeaponry:
				dist = sqrt( (self.rect.centerx - n.rect.centerx)**2 + (self.rect.centery - n.rect.centery)**2 )
				if shortest == -1:
					shortest=dist
					chosen = n
				if dist<shortest:
					shortest=dist
					chosen = n
				
		if chosen is None:
			shortest = -1
			for n in astronauts:
				if not n.isInMedBay and not n.isInWeaponry:
					dist = sqrt( (self.rect.centerx - n.rect.centerx)**2 + (self.rect.centery - n.rect.centery)**2 )
					if shortest == -1:
						shortest=dist
						chosen = n
					if dist<shortest:
						shortest=dist
						chosen = n
		if chosen is None:
			shortest = -1
			for n in astronauts:
				dist = sqrt( (self.rect.centerx - n.rect.centerx)**2 + (self.rect.centery - n.rect.centery)**2 )
				if shortest == -1:
					shortest=dist
					chosen = n
				if dist<shortest:
					shortest=dist
					chosen = n
		self.hunt(chosen)
		self.chosenAstronaut = chosen
		chosen.underAttack = True;
		#print(" === Enemy "+str(self.id)+" is hunting Astronaut "+str(chosen.id)+" ===")
		
	def hunt(self, victim):
		if victim.rect.left + 10 > self.rect.left and victim.rect.left - 10 < self.rect.left:
			self.movementX = 0
		elif victim.rect.left < self.rect.left:
			self.movementX = -self.speed
		elif victim.rect.left > self.rect.left:
			self.movementX = self.speed
		else:
			self.movementX = 0
		
		if victim.rect.top + 10 > self.rect.top and victim.rect.top - 10 < self.rect.top:
			self.movementY = 0
		elif victim.rect.top < self.rect.top:
			self.movementY = self.speed
		elif victim.rect.top > self.rect.top:
			self.movementY = -self.speed
		else:
			self.movementY = 0
		
		if victim.isInMedBay or victim.isInWeaponry:
			self.chosenAstronaut = None
			self.isHunting = False
			
	def updateAstronauts(self, astronauts):
		self.astronauts = astronauts
	
	def attack(self, victim):
		#print(" === Enemy "+str(self.id)+" attacks Astronaut "+str(victim.id)+"===")
		self.movementX = 0
		self.movementY = 0
		self.spritesheet = self.sprite_catalog["phantom_attack"]
		if victim.healthpoints - self.attackPower <= 0:
			self.chosenAstronaut = None
			self.isHunting = False	
		victim.healthpoints -= self.attackPower
		
class Background(pygame.sprite.Sprite):
	def __init__(self, image_file, location):
		pygame.sprite.Sprite.__init__(self) 
		self.image = pygame.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location
			

class Game(threading.Thread):
	def __init__(self, astronauts, enemies):
		threading.Thread.__init__(self)
		self.astronauts = astronauts
		self.enemies = enemies
		self.astronautsMaxId = 8
		self.enemiesMaxId = 3
		for n in self.enemies:
			n.updateAstronauts(self.astronauts)
		self.running = True
	
	def run(self):
		while self.running:
			time.sleep(0.1)
			if len(self.enemies) < 3:
				newEnemy = Enemy(self.enemiesMaxId)
				newEnemy.start()
				self.enemies.add(newEnemy)
				self.enemiesMaxId+=1
			for n in self.enemies:
				n.updateAstronauts(self.astronauts)
				if not n.running:
					self.enemies.remove(n)
			for n in self.astronauts:
				if not n.running:
					self.astronauts.remove(n)
			
				
		
			

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

		pygame.display.flip()



if __name__ == "__main__":
	main()
