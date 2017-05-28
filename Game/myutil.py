import os
import sys
import pygame

#OTHER ------
UP        = 'up'
DOWN      = 'down'
LEFT      = 'left'
RIGHT     = 'right'
CELL_SIZE = 32
#OTHER ------

#COLORS ------
#           R--  G--  B--
BLACK    = (  0,   0,   0)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (0,   255,   0)
BLUE     = (0,     0, 255)
PURPLE   = (255,   0, 255)
YELLOW   = (255, 255,   0)
AQUA     = (  0, 255, 255)
BROWN    = (165,  42,  42)
PINK     = (255, 192, 203)
COLORKEY = (244, 244, 244)
#COLORS ------

#FUNCTIONS ------
def cc(x, y):
		return (x * CELL_SIZE, y * CELL_SIZE)

def load_image(name, folder='', colorkey=None):
	fullname = os.path.join(folder, name)
	
	try:
		image = pygame.image.load(fullname).convert()
	except pygame.error as message:
		print('Cannot load image:', name)
		print(message)
		raise SystemExit
	
	if colorkey != None:
		#colorkey = image.get_at((0,0)) #get pixel in corner to use as colorkey?
		image.set_colorkey(colorkey, pygame.RLEACCEL)
		
	return image #, image.get_rect()
	
def load_sound(folder, name):
	class NoneSound:
		def play(self): pass
		
	if not pygame.mixer:
		return NoneSound()
		
	fullname = os.path.join(folder, name)
	
	try:
		sound = pygame.mixer.Sound(fullname)
	except pygame.error as message:
		print('Cannot load sound:', name)
		print(message)
		raise SystemExit
		
	return sound

def chop_image(image, sub_image_size=(CELL_SIZE, CELL_SIZE)):
	'''Chops a sprite into individual images.'''
	
	assert type(sub_image_size) is tuple and len(sub_image_size) == 2
	
	image_list = []
	index = 0 
	
	for x in range(0, image.get_width(), sub_image_size[0]):
		image_list.append([])
		for y in range(0, image.get_height(), sub_image_size[1]):
			image_list[index].append(image.subsurface(pygame.Rect((x, y), 
			                                             sub_image_size)))
		index += 1
		
	return image_list

def highlight_rect(surface, destination_rect, color, alpha_value):
	highlighter = pygame.Surface(destination_rect.size)
	highlighter.set_alpha(alpha_value)
	highlighter.fill(color)
	surface.blit(highlighter, destination_rect)
	return highlighter

def terminate():
	pygame.quit()
	sys.exit()

###CLASS FOR SPRITES SHIFTING	
class SpriteGroup(list):
	def __init__(self, *sprites):
		self.position = 0
		self.tick = 1
		self.extend(sprites)
		
	def reset_position(self):
		self.position = 0
	
	def check_position(self):
		if self.position >= len(self):
			self.reset_position()
	
	def get_next(self, count):
		"""Get next sprite in sprite group if
		it is time.
		"""
		
		self.check_position()
		if count % self.tick == 0:
			print(self.tick)
			sprite = self[self.position]
			self.position += 1
			return sprite
		self.tick += 1
		if self.tick == 1000:
			self.tick = 1
	
class Button(pygame.Rect):
	def __init__(self, location, size, image, highlighted_image, 
								                tag, action=None):
		super().__init__(location, size)
		self.image = image
		self.highlighted_image = highlighted_image
		self.tag = tag
		self.action = action 
		
	def draw(self, surface):
		surface.blit(self.image, self)
		
	def highlight(self, surface):
		surface.blit(self.highlighted_image, self)
	
	def moused_over(self):
		return self.collidepoint(pygame.mouse.get_pos())
	
	def clicked(self):
		#ADD CHOICE FOR MOUSE UP DOWN AND WHAT MOUSE BUTTON
		if (1 in pygame.mouse.get_pressed()
			and self.moused_over()):
				return True
				
		return False
				
class ButtonGroup(list):
	def __init__(self, tag, *buttons):
		self.tag = tag
		self.extend(buttons)
		
	def draw(self, surface):
		for button in self:
			button.draw(surface)
			
	def get_moused_over_button(self):
		return next((button 
			        for button 
			        in self 
			        if button.moused_over()), None)
			
	def highlight_button(self, surface, button_tag):
		next((button 
			 for button 
			 in self 
			 if button_tag == button.tag), 
			 None).highlight(surface)
			
	def get_clicked_button(self):
		return next((button 
				    for button 
			        in self 
			        if button.clicked()), 
			        None)
		
class Menu(list):
	def __init__(self, *buttongroups):
		self.extend(buttongroups)
		self.current_group = self[0].tag
		
	def draw(self, surface):
		next((buttongroup 
			 for buttongroup 
			 in self 
			 if self.current_group == buttongroup.tag), 
			 None).draw(surface)
			 
	def get_moused_over_button(self):
		return next((buttongroup 
			        for buttongroup 
			        in self
			        if self.current_group == buttongroup.tag), 
			        None).get_moused_over_button()
			 
	def highlight_button(self, surface, button_tag):
		next((buttongroup 
			 for buttongroup 
			 in self 
			 if self.current_group == buttongroup.tag), 
			 None).highlight_button(surface, button_tag)
		
	def get_clicked_button(self):
		return next((buttongroup 
			        for buttongroup 
			        in self 
			        if self.current_group == buttongroup.tag), 
			        None).get_clicked_button()
						   
		#return buttongroup.get_clicked_button()	
#FUNCTIONS ------