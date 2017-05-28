###FIX PROBLEM WHEN A THING IS OUT OF BOUNDS GAME CRASHES
###FIX USE OF ALL COLLISIONS FOR LOCKS
import master
from master import Player
from master import Thing
import myutil
from myutil import cc
import sys
import pygame
from pygame.locals import *
	
def main():
	pygame.init()
	
	pygame.display.set_caption('Super Bro Dog')
	
	#CONSTANTS ------
	#              wid  hei
	SCREENSIZE  = (640, 480)
	DISPLAYSURF = pygame.display.set_mode(SCREENSIZE)
	FPS         = 60
	FPSCLOCK    = pygame.time.Clock()
	SQUARESIZE  = (32, 32)
	#CONSTANTS ------
	
	#IMAGE LOAD ------
	sheet         = myutil.load_image('sheet.png', 'world1', myutil.COLORKEY)
	images        = myutil.chop_image(sheet, SQUARESIZE)
	floorimg      = myutil.load_image('floor.png', 'world1', myutil.COLORKEY)
	keyimg        = myutil.load_image('key.png', 'world1', myutil.COLORKEY)
	lockimg       = myutil.load_image('lock.png', 'world1')
	rockimg       = images[2][2]
	wallimg       = myutil.load_image('wall.png', 'world1',)
	backgroundimg = myutil.load_image('background.png', 'world1')
	ladderimg     = myutil.load_image('ladder.png', 'world1', myutil.COLORKEY)
	breakableimg  = myutil.load_image('breakable.png', 'world1', myutil.COLORKEY)
	winimg        = myutil.load_image('win.png', 'world1', myutil.COLORKEY)
	
	playerimgs = {'left'      : images[2][0],
				  'right'     : images[0][1],
				  'jumpleft'  : images[0][0],
				  'jumpright' : images[1][0],
				  'laddered'  : images[1][0]}
	#IMAGE LOAD ------
	
	#PHYSICS ------
	start_momentum = -5.4
	max_down       = 5.4
	max_up         = -5.4
	jump_change    = .2
	move_amount    = 2
	#PHYSICS ------
	
	#OTHER ------
	level_just_loaded = True
	dirty_rects       = []
	level             = 1
	#OTHER ------
	
	#GAME OBJECTS ------
	ladders  = []
	floors   = []	
	items    = []
	blockers = []
	all      = []
	clicked  = [] #TRACK CLICKED THINGS FOR UPDATE
	#GAME OBJECTS ------
	
	def load_level(file):
		x, y  = 0, 0
		
		with open(file) as f:
			while True:
				char = f.read(1)
				
				if not char:
					break
				elif char == '.':
					pass
				elif char == '_':
					floors.append(Thing(cc(x, y), SQUARESIZE, 'floor', floorimg, False, False, False))
				elif char == '#':
					ladders.append(Thing(cc(x, y), SQUARESIZE, 'ladder', ladderimg, False, False, False))
				elif char == '|':
					blockers.append(Thing(cc(x, y), SQUARESIZE, 'wall', wallimg, True, False, False))
				elif char == 'b':
					blockers.append(Thing(cc(x, y), SQUARESIZE, 'breakable', breakableimg, True, True, False))
				elif char == 'k':
					items.append(Thing(cc(x, y), SQUARESIZE, 'key', keyimg, False, False, True, -5.4))
				elif char == 'l':
					blockers.append(Thing(cc(x, y), SQUARESIZE, 'lock', lockimg, True, False, False))
				elif char == 'w':
					items.append(Thing(cc(x, y), SQUARESIZE, 'win', winimg, False, False, True, True, -5.4))
				elif char == 's':
					start = cc(x, y)
		
				if x == 20:
					x, y = 0, y + 1
				elif char == '/':
					x, y = -1, 0 #FIX -1
				else:
					x += 1
		
		#all.extend(ladders + floors + items + blockers)
		
		return start
	
	start_location = load_level('world1\level{0}.txt'.format(level))
	
	player = Player(start_location,
	                SQUARESIZE,
				    myutil.RIGHT,
					True,
					False,
					start_momentum,
				    playerimgs)

	DISPLAYSURF.blit(backgroundimg, (0, 0))
	
	#DUMMY OBJECT FOR COLLISIONS -----
	dum_thing = Thing((-50, -50), SQUARESIZE, None, None, None, None, None)
	#DUMMY OBJECT FOR COLLISIONS -----
	blah = 3
	while True:
		pygame.event.pump()
		
		#GET COLLISIONS ------
		player.set_collisions('items', items, dum_thing)
		player.set_collisions('ladders', ladders, dum_thing)
		player.set_collisions('floors', floors, dum_thing)
		player.set_collisions('blockers', blockers, dum_thing)
		
		if blah == 3:
			print('before remove:', player.collisions['blockers']['left'])
			
			player.collisions['blockers']['left'] = dum_thing
			
			print('after remove:', player.collisions['blockers']['left'])
			
			print(player.collisions['blockers']['all'])
			blah += 1
		
		for item in items:
			if item.can_fall:
				item.set_collisions('floors', floors, dum_thing)
				item.set_collisions('blockers', blockers, dum_thing)
		#GET COLLISIONS ------
		
		dirty_rects.extend(clicked)
		
		#WHEN ON LADDER AND TOUCHING FLOOR BECOME GROUNDED
		if(player.laddered
		   and player.collisions['floors']['bottom'].tag == 'floor'
		   and player.collisions['floors']['bottom'] != player.collisions['floors']['self']):
				player.grounded = True
				player.laddered = False
				player.down_momentum = start_momentum
				DISPLAYSURF.blit(backgroundimg.subsurface(player), player)
				dirty_rects.append(Rect((player.x, player.y), player.size))
		
		#KEYBOARD ------
		keyboard = pygame.key.get_pressed()
			
		if keyboard[K_UP]:
			if (player.collisions['ladders']['self'].tag == 'ladder' 
			    and not player.collisions['blockers']['top'].is_blocker):
					if not player.laddered:
						player.laddered = True
						player.grounded = False
					player.direction = myutil.UP
					player.update_p_rect_y()
					DISPLAYSURF.blit(backgroundimg.subsurface(player), player)
					dirty_rects.append(Rect((player.x, player.y), player.size))
					player.move(myutil.UP, move_amount)
					player.update_tblr_rects()
			
		if keyboard[K_DOWN]:
			if ((player.collisions['ladders']['bottom'].tag == 'ladder' 
			    or player.laddered)
				and not player.collisions['blockers']['bottom'].is_blocker):
					if not player.laddered:
						player.laddered = True
						player.grounded = False
					player.direction = myutil.DOWN
					player.update_p_rect_y()
					DISPLAYSURF.blit(backgroundimg.subsurface(player), player)
					dirty_rects.append(Rect((player.x, player.y), player.size))
					player.move(myutil.DOWN, move_amount)
					player.update_tblr_rects()
		
		if keyboard[K_LEFT]:
			player.direction = myutil.LEFT
			player.update_p_rect_x()
			DISPLAYSURF.blit(backgroundimg.subsurface(player), player)
			dirty_rects.append(Rect((player.x, player.y), player.size))
			if (player.left != SCREENSIZE[0] - SCREENSIZE[0]
			    and not player.collisions['blockers']['left'].is_blocker):
					player.move(myutil.LEFT, move_amount)
					player.update_tblr_rects()
			
		if keyboard[K_RIGHT]:
			player.direction = myutil.RIGHT
			player.update_p_rect_x()
			DISPLAYSURF.blit(backgroundimg.subsurface(player), player)
			dirty_rects.append(Rect((player.x, player.y), player.size))
			if (player.right != SCREENSIZE[0] 
			    and not player.collisions['blockers']['right'].is_blocker):
					player.move(myutil.RIGHT, move_amount)
					player.update_tblr_rects()
			
		if keyboard[K_SPACE]:
			if (player.grounded 
			    and not player.laddered
			    and not player.collisions['blockers']['top'].is_blocker):
					player.grounded = False
			
		if keyboard[K_ESCAPE]:
			myutil.terminate()
		#KEYBOARD ------
	
		if player.collisions['items']['self'].tag == 'key':
			player.key_count += 1
			items.remove(player.collisions['items']['self'])
			DISPLAYSURF.blit(backgroundimg.subsurface(player.collisions['items']['self']), player.collisions['items']['self'])
			dirty_rects.append(Rect((player.collisions['items']['self'].x, player.collisions['items']['self'].y), 
			                                                     player.collisions['items']['self'].size))
		elif (player.key_count > 0
			  and 'lock' in player.get_all_collision_tags('blockers')):
				player.key_count -= 1
				for thing in player.collisions['blockers']['all']:
					if thing.tag == 'lock':
						blockers.remove(thing)
						DISPLAYSURF.blit(backgroundimg.subsurface(thing), thing) 
						dirty_rects.append(Rect((thing.x, thing.y), thing.size))
				###WORKS BUT COLLISIONS STILL IN REGULAR NON ALL LISTS PROBLEM?
				#if player.collisions['blockers']['left'].tag == 'lock': 
				#	blockers.remove(player.collisions['blockers']['left'])
				#	DISPLAYSURF.blit(backgroundimg.subsurface(player.collisions['blockers']['left']), 
				#											    player.collisions['blockers']['left'])
				#	dirty_rects.append(Rect((player.collisions['blockers']['left'].x, 
			    #                             player.collisions['blockers']['left'].y), 
			    #                             player.collisions['blockers']['left'].size))
				#elif player.collisions['blockers']['right'].tag == 'lock':
				#	blockers.remove(player.collisions['blockers']['right'])
				#	DISPLAYSURF.blit(backgroundimg.subsurface(player.collisions['blockers']['right']), 
				#	                                            player.collisions['blockers']['right'])
				#	dirty_rects.append(Rect((player.collisions['blockers']['right'].x, 
				#	                         player.collisions['blockers']['right'].y), 
			    #                            player.collisions['blockers']['right'].size))
				#elif player.collisions['blockers']['top'].tag == 'lock':
				#	blockers.remove(player.collisions['blockers']['top'])
				#	DISPLAYSURF.blit(backgroundimg.subsurface(player.collisions['blockers']['top']), 
				#	                                            player.collisions['blockers']['top'])
				#	dirty_rects.append(Rect((player.collisions['blockers']['top'].x, 
				#	                         player.collisions['blockers']['top'].y), 
			    #                            player.collisions['blockers']['top'].size))
				#elif player.collisions['blockers']['bottom'].tag == 'lock':
				#	blockers.remove(player.collisions['blockers']['bottom'])
				#	DISPLAYSURF.blit(backgroundimg.subsurface(player.collisions['blockers']['bottom']), 
				#	                                            player.collisions['blockers']['bottom'])
				#	dirty_rects.append(Rect((player.collisions['blockers']['bottom'].x, 
				#	                         player.collisions['blockers']['bottom'].y), 
			    #                            player.collisions['blockers']['bottom'].size))
				
		#PREVENT ODD LADDER POSITIONS
		if player.laddered and player.y%2 != 0:
			player.update_p_rect_y()
			DISPLAYSURF.blit(backgroundimg.subsurface(player), player)
			dirty_rects.append(Rect((player.x, player.y), player.size))
			player.y -= 1
			player.update_tblr_rects()
			
		#FALL WHEN EXITING A LADDER
		if (player.collisions['ladders']['self'].tag != 'ladder' 
		    and player.laddered):
				player.laddered = False
				if not player.grounded:
					player.down_momentum = 0
		
		#FALL WHEN WALKING OVER A HOLE
		if (player.collisions['floors']['bottom'].tag == None
			and not player.collisions['blockers']['bottom'].is_blocker
			and player.down_momentum == start_momentum):
				player.grounded      = False
				player.down_momentum = 0
		
		#ITEMS FALL WHEN NOT ON ANYTHING ------
		for item in items:
			if item.can_fall:
				if (item.collisions['floors']['bottom'].tag == None
					and not item.collisions['blockers']['bottom'].is_blocker
					and item.down_momentum == start_momentum):
						item.grounded      = False
						item.down_momentum = 0
						
				if (item.down_momentum != max_down 
					and not item.grounded):
						item.down_momentum += jump_change
						
				if not item.grounded:
					item.update_p_rect_y()
					DISPLAYSURF.blit(backgroundimg.subsurface(item), item)
					dirty_rects.append(Rect((item.x, item.y), item.size))
					item.move(myutil.DOWN, item.down_momentum)
					item.update_tblr_rects()
					
				item.set_collisions('floors', floors, dum_thing)
				item.set_collisions('blockers', blockers, dum_thing)
					
				if (item.collisions['floors']['self'].tag == 'floor'
					and item.p_rect.bottom <= item.collisions['floors']['self'].top
					and item.down_momentum > 0
					and item.p_rect.left <= item.collisions['floors']['self'].right
					and item.p_rect.right >= item.collisions['floors']['self'].left):
						item.grounded      = True
						item.down_momentum = start_momentum
						DISPLAYSURF.blit(backgroundimg.subsurface(item), item)
						dirty_rects.append(Rect((item.x, item.y), item.size))
						item.top = item.collisions['floors']['self'].top - SQUARESIZE[0]
						player.update_tblr_rects()
				elif (item.collisions['blockers']['self'].is_blocker
					  and item.p_rect.bottom <= item.collisions['blockers']['self'].top
					  and item.down_momentum > 0
					  and item.p_rect.left <= item.collisions['blockers']['self'].right
					  and item.p_rect.right >= item.collisions['blockers']['self'].left):
						item.grounded      = True
						item.down_momentum = start_momentum
						DISPLAYSURF.blit(backgroundimg.subsurface(item), item)
						dirty_rects.append(Rect((item.x, item.y), item.size))
						item.top = item.collisions['blockers']['self'].top - SQUARESIZE[0]
						item.update_tblr_rects()
		#ITEMS FALL WHEN NOT ON ANYTHING ------

		#CHANGE DOWN MEMENTUM OF PLAYER WHEN JUMPING/FALLING
		if (player.down_momentum != max_down 
		    and not player.grounded
			and not player.laddered):
				player.down_momentum += jump_change
				
		#FALL OR ASCEND BASED ON CURRENT DOWN MOMENTUM
		if not player.grounded and not player.laddered:
			player.update_p_rect_y()
			DISPLAYSURF.blit(backgroundimg.subsurface(player), player)
			dirty_rects.append(Rect((player.x, player.y), player.size))
			player.move(myutil.DOWN, player.down_momentum)
			player.update_tblr_rects()
		
		###FOR SMOOTH LANDING BETTER WAY???
		player.set_collisions('floors', floors, dum_thing)
		player.set_collisions('blockers', blockers, dum_thing)
		
		#LAND ON FLOOR OR BLOCKER WITHOUT GOING THROUGH IT
		if (player.collisions['floors']['self'].tag == 'floor'
			and player.p_rect.bottom <= player.collisions['floors']['self'].top
			and player.down_momentum > 0
			and player.p_rect.left <= player.collisions['floors']['self'].right
			and player.p_rect.right >= player.collisions['floors']['self'].left):
				player.grounded       = True
				player.down_momentum  = start_momentum
				DISPLAYSURF.blit(backgroundimg.subsurface(player), player)
				dirty_rects.append(Rect((player.x, player.y), player.size))
				player.top = player.collisions['floors']['self'].top - SQUARESIZE[0]
				player.update_tblr_rects()
		elif (player.collisions['blockers']['self'].is_blocker
			  and player.p_rect.bottom <= player.collisions['blockers']['self'].top
			  and player.down_momentum > 0
			  and player.p_rect.left <= player.collisions['blockers']['self'].right
			  and player.p_rect.right >= player.collisions['blockers']['self'].left):
				player.grounded       = True
				player.down_momentum  = start_momentum
				DISPLAYSURF.blit(backgroundimg.subsurface(player), player)
				dirty_rects.append(Rect((player.x, player.y), player.size))
				player.top = player.collisions['blockers']['self'].top - SQUARESIZE[0]
				player.update_tblr_rects()
				
		#PREVENT PLAYER FROM JUMPING THROUGH BLOCKERS
		if (player.collisions['blockers']['self'].is_blocker
			  and player.p_rect.top >= player.collisions['blockers']['self'].bottom
			  and player.down_momentum <= 0
			  and player.p_rect.left <= player.collisions['blockers']['self'].right
			  and player.p_rect.right >= player.collisions['blockers']['self'].left):
				player.down_momentum  = 0
				DISPLAYSURF.blit(backgroundimg.subsurface(player), player)
				dirty_rects.append(Rect((player.x, player.y), player.size))
				player.bottom = player.collisions['blockers']['self'].bottom + SQUARESIZE[0]
				player.update_tblr_rects()
		
		#NEXT LEVEL WHEN BONE AQUIRED ------	
		if player.collisions['items']['self'].tag == 'win':
			level_just_loaded = True
			level += 1
			items.remove(player.collisions['items']['self'])
			DISPLAYSURF.blit(backgroundimg.subsurface(player.collisions['items']['self']), 
					                                            player.collisions['items']['self'])
			dirty_rects.append(Rect((player.collisions['items']['self'].x, 
					                 player.collisions['items']['self'].y), 
			                         player.collisions['items']['self'].size))
		#NEXT LEVEL WHEN BONE AQUIRED ------	
		
		#DRAW ------
		for floor in floors:
			floor.draw(DISPLAYSURF)	
		for ladder in ladders:
			ladder.draw(DISPLAYSURF)
		for item in items:
			item.draw(DISPLAYSURF)
		for blocker in blockers:
			if blocker.tag != 'breakable':
				blocker.draw(DISPLAYSURF)
		
		#HIGHLIGHT CLICKABLE THINGS
		###ADD WAY THAT MORE THAN JUST BREAKABLE CAN BE CLICKED
		#for blocker in blockers:
			if blocker.tag == 'breakable': ###PROBLEM HERE
				dirty_rects.append(Rect((blocker.x, blocker.y), blocker.size))
				blocker.draw(DISPLAYSURF)
				if blocker.collidepoint(pygame.mouse.get_pos()):
					if True in pygame.mouse.get_pressed():
						blockers.remove(blocker)
						clicked.append(blocker)
						DISPLAYSURF.blit(backgroundimg.subsurface(blocker), blocker)
						dirty_rects.append(Rect((blocker.x, blocker.y), blocker.size))
					else:
						#myutil.highlight_rect(DISPLAYSURF, blocker, myutil.BLUE, alpha_value = 155)
						dirty_rects.append(Rect((blocker.x, blocker.y), blocker.size))
			
		player.draw(DISPLAYSURF)
		#DRAW ------
		
		#UPKEEP ------
	#	player.update_tblr_rects() ###SHOULD BE ENABLED???

		dirty_rects.append(Rect((player.x, player.y), player.size))
		
		player.collisions = {}
		for item in items:
			if item.can_fall:
				item.collisions = {}
				dirty_rects.append(Rect((item.x, item.y), item.size))
		
		#NEXT LEVEL ------
		if level_just_loaded and level == 1:
			level_just_loaded = False
			pygame.display.update()
		elif level_just_loaded and level > 1:
				items, ladders, floors, blockers = [], [], [], []
				player.x, player.y = start_location = load_level('world1\level{0}.txt'.format(level))
				level_just_loaded = False
				pygame.display.update()
		#NEXT LEVEL ------
		
		pygame.display.update(dirty_rects)
		
		dirty_rects = []
		
		FPSCLOCK.tick(FPS)
		#UPKEEP ------
		
if __name__ == '__main__':
	main()