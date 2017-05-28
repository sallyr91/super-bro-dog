import pygame
from pygame.locals import *
import myutil

#BASE CLASS FOR GAME OBJECTS ------
class Bounder(pygame.Rect):
	def __init__(self, location, size, tag=None):
		super().__init__(location, size)
		self.tag = tag
		self.p_rect = Rect(location, size) #PREVIOUS RECT
		self.t_rect = Rect((location[0], location[1] -1), (size[0], 1))
		self.b_rect = Rect((location[0], location[1] + size[0]), (size[0], 1))
		self.l_rect = Rect((location[0]-1, location[1]), (1, size[1]))
		self.r_rect = Rect((location[0]+size[0], location[1]), (1, size[1]))
		self.collisions = {}
		
	def update_p_rect_y(self):
		self.p_rect.y = self.y
		
	def update_p_rect_x(self):
		self.p_rect.x = self.x
		
	def update_tblr_rects(self):
		self.t_rect.x = self.x
		self.t_rect.y = self.y - 1
		
		self.b_rect.x = self.x
		self.b_rect.y = self.y + self.size[0]
		
		self.l_rect.x = self.x - 1
		self.l_rect.y = self.y
		
		self.r_rect.x = self.x + self.size[0]
		self.r_rect.y = self.y
		
	def set_collisions(self, rect_size, index_name, objects):	###REMEMBER TO EMPTY COLLISIONS collisions = {} 	
		items = (self,        'self',
				 self.t_rect, 'top',
		         self.b_rect, 'bottom', 
			     self.l_rect, 'left', 
                 self.r_rect, 'right')
		
		for i in range(0, len(items), 2):
			collide_index = items[i].collidelist(objects)
			if collide_index != -1:
				self.collisions[index_name] = {items[i+1], objects[collide_index]}
			else:
				self.collisions[index_name] = {items[i+1], Bounder((-50, -50), rect_size, '')}
	
	def set_bottom_collisions(self, rect_size, index_name, objects):	     
		collide_index = self.b_rect.collidelist(objects)
		
		if collide_index != -1:
			self.collisions[index_name] = {'bottom', objects[collide_index]}
		else:
			self.collisions[index_name] = {'bottom', Bounder((-50, -50), rect_size, '')}
#BASE CLASS FOR GAME OBJECTS ------

class Thing(Bounder):
	def __init__(self, location, size, tag,
	             image, is_blocker,
				 clickable, can_fall, down_momentum=None):
		super().__init__(location, size, tag)
		self.image         = image
		self.is_blocker    = is_blocker
		self.clickable     = clickable
		self.can_fall      = can_fall
		self.down_momentum = down_momentum
		
	def draw(self, screen):
		screen.blit(self.image, self)
				
class Player(Bounder):
	def __init__(self, location, size, direction, grounded,
	             laddered, down_momentum,
				 images, key_count=0, shilded=False):
		super().__init__(location, size, tag=None)
		self.direction     = direction
		self.grounded      = grounded      #is player on floor
		self.laddered      = laddered      #is player on ladder
		self.down_momentum = down_momentum #for jumping/falling
		self.images        = images		   
		self.key_count     = key_count	   #how many keys does the player have
		self.shilded       = shilded       #does the player have a shield
											  
	def draw(self, surface):
		if not self.laddered:
			if self.grounded:
				if self.direction == myutil.LEFT:
					surface.blit(self.images['left'], self)
				elif self.direction == myutil.RIGHT:
					surface.blit(self.images['right'], self)
				else: 
					surface.blit(self.images['laddered'], self)
			else:
				if self.direction == myutil.LEFT:
					surface.blit(self.images['jumpleft'], self)
				elif self.direction == myutil.RIGHT:
					surface.blit(self.images['jumpright'], self)
				elif self.direction == myutil.UP:
					surface.blit(self.images['laddered'], self)
				else: 
					surface.blit(self.images['laddered'], self)
		else:
			surface.blit(self.images['laddered'], self)
		
	def get_collisions(self, objects, rect_size):
		collided_with = {}
		
		items = (self,        'player',
				 self.t_rect, 'top',
		         self.b_rect, 'bottom', 
			     self.l_rect, 'left', 
                 self.r_rect, 'right')
		
		for i in range(0, len(items), 2):
			collide_index = items[i].collidelist(objects)
			if collide_index != -1:
				yield items[i+1], objects[collide_index]
			else:
				yield items[i+1], Thing((-50, -50), rect_size, None, None, None, None, None)

	def move(self, direction, move_amount):
		if direction == myutil.UP:
			self.move_ip(0, -move_amount)
		elif direction == myutil.DOWN:
			self.move_ip(0, move_amount)
		elif direction == myutil.LEFT:
			self.move_ip(-move_amount, 0)
		elif direction == myutil.RIGHT:
			self.move_ip(move_amount, 0)
		else:
			print('direction must be up, down, left, or right')
			raise SystemExit