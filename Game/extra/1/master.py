import pygame
from pygame.locals import *
import myutil

class Thing(pygame.Rect):
	def __init__(self, location, size, 
	            image, tag, is_blocker):
		super().__init__(location, size)
		self.image      = image
		self.tag        = tag #what kind of object is it?
		self.is_blocker = is_blocker #can it block player movement?
		#self.clickable  = clickable
		#self.can_fall   = can_fall
		#self.draw_order = draw_order
		
	def draw(self, screen):
		screen.blit(self.image, self)
				
class Player(pygame.Rect):
	def __init__(self, location, size, direction, grounded,
	             laddered, down_momentum,
				 images, key_count=0, shilded=False):
		super().__init__(location, size)
		self.direction     = direction
		self.grounded      = grounded      #is player on floor
		self.laddered      = laddered      #is player on ladder
		self.down_momentum = down_momentum #for jumping/falling
		self.images        = images		   
		self.key_count     = key_count	   #how many keys does the player have
		self.shilded       = shilded       #does the player have a shield
		self.previous_rect = Rect(location, size) #for updating screen
		self.next_rect     = Rect(location, size)
		self.t_rect = Rect((location[0], location[1] -1), (size[0], 1))
		self.b_rect = Rect((location[0], #rect for colliding with floor objects
		                    location[1] + size[0]), 
								       (size[0], 1))
		self.l_rect = Rect((location[0]-1, location[1]), #rects for colliding with left/right
		                                    (1, size[1]))
		self.r_rect = Rect((location[0]+size[0], location[1]), 
		                                          (1, size[1]))
											  
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

	def update_previous_y(self):
		self.previous_rect.y = self.y
		
	def update_previous_x(self):
		self.previous_rect.x = self.x
	
    ###PROBLEM MOVING MAKES NEXT RECT SAME AS PLAYER IMPLEMENT MOVEMENT PHYSICS FOR LEFT RIGHT	
	def update_next(self, move_amount=None):
		if self.grounded or self.laddered:
			if self.direction == myutil.UP:
				self.next_rect.x   = self.x
				self.next_rect.top = self.top - move_amount
			elif self.direction == myutil.DOWN:
				self.next_rect.x = self.x
				self.next_rect.bottom = self.bottom + move_amount
			elif self.direction == myutil.LEFT:
				self.next_rect.left = self.left - move_amount
				self.next_rect.y = self.y
			elif self.direction == myutil.RIGHT:
				self.next_rect.right = self.right + move_amount
				self.next_rect.y = self.y
		else:
			if self.down_momentum < 0:
				self.next_rect.top = self.top + self.down_momentum
				self.next_rect.x = self.x
			else:
				self.next_rect.bottom = self.bottom + self.down_momentum
				self.next_rect.x = self.x
	
	def update_rects(self):
		self.t_rect.x = self.x
		self.t_rect.y = self.y - 1
		
		self.b_rect.x = self.x
		self.b_rect.y = self.y + self.size[0]
		
		self.l_rect.x = self.x - 1
		self.l_rect.y = self.y
		
		self.r_rect.x = self.x + self.size[0]
		self.r_rect.y = self.y
		
	def get_collisions(self, objects, squaresize):
		collided_with = {}
		
		items = (self,        'player',
				 self.t_rect, 'top',
		         self.b_rect, 'base', 
			     self.l_rect, 'left', 
                 self.r_rect, 'right')
		
		for i in range(0, len(items), 2):
			collide_index = items[i].collidelist(objects)
			if collide_index != -1:
				yield items[i+1], objects[collide_index]
			else:
				yield items[i+1], Thing((-50, -50), squaresize, None, None, None)

	def move(self, direction, move_amount):
		self.update_rects()
	
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