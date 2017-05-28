import pygame
from pygame.locals import *
import myutil
import os

#BASE CLASS FOR GAME OBJECTS ------
class Bounder(pygame.Rect):
	'''Class to keep track of Rects surrounding 
	   objects for collision detection.
	'''

	def __init__(self, location, size):
		super().__init__(location, size)
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
	
	def set_collisions(self, index_name, objects, dummy):
		'''Get all things that collide with bounder Rects
		   as a dictionary. Collisions must be emptied
		   after game loop.
		'''
	
		items = (self,        'self',
				 self.t_rect, 'top',
		         self.b_rect, 'bottom', 
			     self.l_rect, 'left', 
                 self.r_rect, 'right')
		
		self.collisions.update({index_name : {}})
		self.collisions[index_name].update({'all' : []})
		
		for i in range(0, len(items), 2):
			collide_index = items[i].collidelist(objects)
			if collide_index != -1:
				self.collisions[index_name].update({items[i+1] : objects[collide_index]})
			else:
				self.collisions[index_name].update({items[i+1] : dummy})
			self.collisions[index_name]['all'].append(self.collisions[index_name][items[i+1]])
	
	def set_bottom_collisions(self, index_name, objects, dummy):
		'''Set collisions just for bottom Rect of Bounder.'''
	
		collide_index = self.b_rect.collidelist(objects)
		
		self.collisions.update({index_name : {}})
		
		if collide_index != -1:
			self.collisions[index_name].update({'bottom' : objects[collide_index]})
		else:
			self.collisions[index_name].update({'bottom' : dummy})
	
	#GET ALL THE TAGS OF ALL OBJECTS THAT COLLIDE WITH THE BOUNDER
	###CHANGE TO YIELD
	def get_all_collision_tags(self, index_name):
		return {object.tag for object in self.collisions[index_name]['all']}
#BASE CLASS FOR GAME OBJECTS ------

class Thing(Bounder):
	'''Class for game objects like ladders, 
	   floors, keys, etc...
	'''

	def __init__(self, location, size, tag,
	             image, is_blocker,
				 clickable, can_fall, grounded=True, down_momentum=None):
		super().__init__(location, size)
		self.tag = tag
		self.image = image
		self.is_blocker = is_blocker
		self.clickable = clickable
		self.can_fall = can_fall
		self.grounded = grounded
		self.down_momentum = down_momentum
		
	def __str__(self):
		return 'Thing, {0}, location: {1}, {2}'.format(self.tag, self.x, self.y)
		
	def draw(self, surface):
		surface.blit(self.image, self)
		
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
				
class Player(Bounder):
	'''Class for player.'''

	def __init__(self, location, size, 
	             direction, grounded,
	             laddered, down_momentum,
				 images, image_dict,
				 key_count=0, 
				 has_hammer=False, 
				 has_shield=False):
		super().__init__(location, size)
		self.direction = direction
		self.grounded = grounded
		self.laddered = laddered 
		self.down_momentum = down_momentum
		self.images = images
		self.image_collection = image_dict
		self.key_count = key_count
		self.has_hammer = has_hammer
		self.has_shield = has_shield
	
	def get_current_sprite(self):
		pass
	
	def draw(self, surface):
		if not self.laddered:
			if self.grounded:
				if self.direction == myutil.LEFT:
					###FIX
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

	def move(self, direction, move_amount):
		assert direction in {myutil.UP, myutil.DOWN, myutil.LEFT, myutil.RIGHT}
	
		if direction == myutil.UP:
			self.move_ip(0, -move_amount)
		elif direction == myutil.DOWN:
			self.move_ip(0, move_amount)
		elif direction == myutil.LEFT:
			self.move_ip(-move_amount, 0)
		elif direction == myutil.RIGHT:
			self.move_ip(move_amount, 0)

class Level():
	'''Class for individual levels and their contents.'''

	def __init__(self, tag, folder, file, images):
		self.ladders = []
		self.floors = []	
		self.items = []
		self.blockers = []
		self.tag = tag
		self.start = self.load_level(folder, file, images)
		
	def load_level(self, folder, filename, images):
		x, y  = 0, 0
		
		fullname = os.path.join(folder, filename)
		
		with open(fullname) as f:
			while True:
				char = f.read(1)
				
				if not char:
					break
				elif char == '.':
					pass
				elif char == '_':
					self.floors.append(Thing(myutil.cc(x, y), (myutil.CELL_SIZE, myutil.CELL_SIZE), 'floor', 
					                   images['floor'], False, False, False))
				elif char == '#':
					self.ladders.append(Thing(myutil.cc(x, y), (myutil.CELL_SIZE, myutil.CELL_SIZE), 'ladder', 
					                    images['ladder'], False, False, False))
				elif char == '|':
					self.blockers.append(Thing(myutil.cc(x, y), (myutil.CELL_SIZE, myutil.CELL_SIZE), 'wall', 
					                     images['wall'], True, False, False))
				elif char == 'b':
					self.blockers.append(Thing(myutil.cc(x, y), (myutil.CELL_SIZE, myutil.CELL_SIZE), 'breakable', 
					                     images['breakable'], True, True, False))
				elif char == 'k':
					self.items.append(Thing(myutil.cc(x, y), (myutil.CELL_SIZE, myutil.CELL_SIZE), 'key', 
					                  images['key'], False, False, True, True, 
									  -5.4))
				elif char == 'l':
					self.blockers.append(Thing(myutil.cc(x, y), (myutil.CELL_SIZE, myutil.CELL_SIZE), 'lock', 
					                     images['lock'], True, False, False))
				elif char == 'h':
					self.items.append(Thing(myutil.cc(x, y), (myutil.CELL_SIZE, myutil.CELL_SIZE), 'hammer', 
					                  images['hammer'], False, False, True, True,
									  -5.4))
				elif char == '*':
					self.blockers.append(Thing(myutil.cc(x, y), (myutil.CELL_SIZE, myutil.CELL_SIZE), 'hammerable', 
					                     images['hammerable'], True, True, 
										 False))
				elif char == 'w':
					self.items.append(Thing(myutil.cc(x, y), (myutil.CELL_SIZE, myutil.CELL_SIZE), 'win', 
					                  images['win'], False, False, True, True, 
									  -5.4))
				elif char == 's':
					start = myutil.cc(x, y)
		
				if x == 20:
					x, y = 0, y + 1
				elif char == '/':
					x, y = -1, 0 #FIX -1
				else:
					x += 1

		return start
		
	def draw(self, surface, images, dirty_rects, player):
		for floor in self.floors:
			floor.draw(surface)	
		for ladder in self.ladders:
			ladder.draw(surface)
		for item in self.items:
			item.draw(surface)
		for blocker in self.blockers:
			#HIGHLIGHT CLICKABLE THINGS ------
			if blocker.tag in {'breakable', 'hammerable'}:
				dirty_rects.append(Rect((blocker.x, blocker.y), blocker.size))
				blocker.draw(surface)
				if blocker.collidepoint(pygame.mouse.get_pos()):
					if True in pygame.mouse.get_pressed():
						if blocker.tag == 'hammerable' and not player.has_hammer:
							pass
						else:
							self.blockers.remove(blocker)
							#clicked.append(blocker)
							surface.blit(images['background'].subsurface(blocker), blocker)
					else:
						if blocker.tag == 'breakable':
							myutil.highlight_rect(surface, blocker, myutil.BLUE, alpha_value = 155)
						elif blocker.tag == 'hammerable' and player.has_hammer:
							myutil.highlight_rect(surface, blocker, myutil.BLUE, alpha_value = 155)
						else:
							myutil.highlight_rect(surface, blocker, myutil.RED, alpha_value = 155)
				else:
					surface.blit(images['background'].subsurface(blocker), blocker)
					#DRAW ITEM BEHIND TRANSPARENT BLOCKER
					item = next((item for item in self.items if (item.x, item.y) == (blocker.x, blocker.y)), None)
					if item:
						item.draw(surface)
					blocker.draw(surface)
			#HIGHLIGHT CLICKABLE THINGS ------
			else:
				blocker.draw(surface)