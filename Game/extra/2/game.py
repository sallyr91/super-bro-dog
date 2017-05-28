#PROBLEM NO IMAGE FOR DIRECTION == UP and LADDERED
#HAVE TWO DIFFERENT VARIABLES FOR UP/DOWN LEFT/RIGHT?
#keyboard: you cant hold right up and jump, or down left and jump
#dog images still not drawing correctly
#dog jitters when landing fix with list representing map get adjacent rects and update
#jump boots, bouncy pads, jet pack???
#IF YOU LAND ON BLOCK AND LOCK WITH KEY BLOCK DISAPPEARS!!!!!!!!!!!!!!GAME BRAKING
#DONT LET DOG JUMP THROUGH BLOCKERS
#JUMP IS POSSIBLE FIRST FRAME IN MID AIR!!!! FIXXXXXXXXXXXXXXXXXXXX GAME BREAKING
#FIX breakables, items not showing behind breakables
#PERHAPS MAKE JUST CLICKED LIST THAT GET RECT COPY OF JUST CLICKED ADDED FOR UPDATE?
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
	breakableimg  = myutil.load_image('ladder.png', 'world1', myutil.COLORKEY)
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
	collided_with     = {}
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
					items.append(Thing(cc(x, y), SQUARESIZE, 'win', winimg, False, False, True, -5.4))
				elif char == 's':
					start = cc(x, y)
		
				if x == 20:
					x, y = 0, y + 1
				elif char == '/':
					x, y = -1, 0 #FIX -1
				else:
					x += 1
		
		all.extend(ladders + floors + items + blockers)
		
		return start
	
	start_location = load_level('world1\level1.txt')
	
	player = Player(start_location,
	                    SQUARESIZE,
					  myutil.RIGHT,
					          True,
					         False,
					start_momentum,
				    	 playerimgs)

	DISPLAYSURF.blit(backgroundimg, (0, 0))
	
	while True:
		###EVENT ------
		pygame.event.pump()
		
		#GET WHAT THE PLAYER TOUCHES ------
		player.set_collisions(SQUARESIZE, 'items', items)
		player.set_collisions(SQUARESIZE, 'ladders', ladders)
		player.set_collisions(SQUARESIZE, 'floors', floors)
		player.set_collisions(SQUARESIZE, 'blockers', blocker)
		
		collided_with['items']    = dict(player.get_collisions(items,    SQUARESIZE))
		collided_with['ladders']  = dict(player.get_collisions(ladders,  SQUARESIZE))
		collided_with['floors']   = dict(player.get_collisions(floors,   SQUARESIZE))
		collided_with['blockers'] = dict(player.get_collisions(blockers, SQUARESIZE))
		#GET WHAT THE PLAYER TOUCHES ------
		
		dirty_rects.extend(clicked)
		
		#WHEN ON LADDER AND TOUCHING FLOOR BECOME GROUNDED
		if(player.laddered
		   and collided_with['floors']['bottom'].tag == 'floor'
		   and collided_with['floors']['bottom'] != collided_with['floors']['player']):
				player.grounded = True
				player.laddered = False
				player.down_momentum = start_momentum
				DISPLAYSURF.blit(backgroundimg.subsurface(player), player)
				dirty_rects.append(Rect((player.x, player.y), player.size))
		
		#KEYBOARD ------
		keyboard = pygame.key.get_pressed()
			
		if keyboard[K_UP]:
			if (collided_with['ladders']['player'].tag == 'ladder' 
			    and not collided_with['blockers']['top'].is_blocker):
					if not player.laddered:
						player.laddered = True
						player.grounded = False
					player.direction = myutil.UP
					player.update_p_rect_y()
					DISPLAYSURF.blit(backgroundimg.subsurface(player), player)
					dirty_rects.append(Rect((player.x, player.y), player.size))
					player.update_tblr_rects()
					player.move(myutil.UP, move_amount)
			
		if keyboard[K_DOWN]:
			if ((collided_with['ladders']['bottom'].tag == 'ladder' 
			    or player.laddered)
				and not collided_with['blockers']['bottom'].is_blocker):
					if not player.laddered:
						player.laddered = True
						player.grounded = False
					player.direction = myutil.DOWN
					player.update_p_rect_y()
					DISPLAYSURF.blit(backgroundimg.subsurface(player), player)
					dirty_rects.append(Rect((player.x, player.y), player.size))
					player.update_tblr_rects()
					player.move(myutil.DOWN, move_amount)
		
		if keyboard[K_LEFT]:
			player.direction = myutil.LEFT
			player.update_p_rect_x()
			DISPLAYSURF.blit(backgroundimg.subsurface(player), player)
			dirty_rects.append(Rect((player.x, player.y), player.size))
			if (player.left != SCREENSIZE[0] - SCREENSIZE[0]
			    and not collided_with['blockers']['left'].is_blocker):
					player.move(myutil.LEFT, move_amount)
					player.update_tblr_rects()
			
		if keyboard[K_RIGHT]:
			player.direction = myutil.RIGHT
			player.update_p_rect_x()
			DISPLAYSURF.blit(backgroundimg.subsurface(player), player)
			dirty_rects.append(Rect((player.x, player.y), player.size))
			if (player.right != SCREENSIZE[0] 
			    and not collided_with['blockers']['right'].is_blocker):
					player.move(myutil.RIGHT, move_amount)
					player.update_tblr_rects()
			
		if keyboard[K_SPACE]:
			if (player.grounded 
			    and not player.laddered
			    and not collided_with['blockers']['top'].is_blocker):
					player.grounded = False
			
		if keyboard[K_ESCAPE]:
			myutil.terminate()
		#KEYBOARD ------
		
		if collided_with['items']['player'].tag == 'win':
			level += 1
	
		if collided_with['items']['player'].tag == 'key':
			player.key_count += 1
			items.remove(collided_with['items']['player'])
			DISPLAYSURF.blit(backgroundimg.subsurface(collided_with['items']['player']), collided_with['items']['player'])
			dirty_rects.append(Rect((collided_with['items']['player'].x, collided_with['items']['player'].y), 
			                                                     collided_with['items']['player'].size))
		elif (player.key_count > 0 ### !!! SIMPLIFY???
			  and (collided_with['blockers']['left'].tag == 'lock' 
			  or collided_with['blockers']['right'].tag == 'lock'
			  or collided_with['blockers']['top'].tag == 'lock'
			  or collided_with['blockers']['bottom'].tag == 'lock')):
				player.key_count -= 1
				if collided_with['blockers']['left'].tag == 'lock': 
					blockers.remove(collided_with['blockers']['left'])
					DISPLAYSURF.blit(backgroundimg.subsurface(collided_with['blockers']['left']), 
															    collided_with['blockers']['left'])
					dirty_rects.append(Rect((collided_with['blockers']['left'].x, 
			                                 collided_with['blockers']['left'].y), 
			                                 collided_with['blockers']['left'].size))
				elif collided_with['blockers']['right'].tag == 'lock':
					blockers.remove(collided_with['blockers']['right'])
					DISPLAYSURF.blit(backgroundimg.subsurface(collided_with['blockers']['right']), 
					                                            collided_with['blockers']['right'])
					dirty_rects.append(Rect((collided_with['blockers']['right'].x, 
					                         collided_with['blockers']['right'].y), 
			                                 collided_with['blockers']['right'].size))
				elif collided_with['blockers']['top'].tag == 'lock':
					blockers.remove(collided_with['blockers']['top'])
					DISPLAYSURF.blit(backgroundimg.subsurface(collided_with['blockers']['top']), 
					                                            collided_with['blockers']['top'])
					dirty_rects.append(Rect((collided_with['blockers']['top'].x, 
					                         collided_with['blockers']['top'].y), 
			                                 collided_with['blockers']['top'].size))
				elif collided_with['blockers']['bottom'].tag == 'lock':
					blockers.remove(collided_with['blockers']['bottom'])
					DISPLAYSURF.blit(backgroundimg.subsurface(collided_with['blockers']['bottom']), 
					                                            collided_with['blockers']['bottom'])
					dirty_rects.append(Rect((collided_with['blockers']['bottom'].x, 
					                         collided_with['blockers']['bottom'].y), 
			                                 collided_with['blockers']['bottom'].size))
				
		#PREVENT ODD LADDER POSITIONS
		if player.laddered and player.y%2 != 0:
			player.update_p_rect_y()
			DISPLAYSURF.blit(backgroundimg.subsurface(player), player)
			dirty_rects.append(Rect((player.x, player.y), player.size))
			player.y -= 1
			player.update_tblr_rects()
			
		#FALL WHEN EXITING A LADDER
		if (collided_with['ladders']['player'].tag != 'ladder' 
		    and player.laddered):
				player.laddered = False
				if not player.grounded:
					player.down_momentum = 0
		
		#FALL WHEN WALKING OVER A HOLE
		if (collided_with['floors']['bottom'].tag == None
			and not collided_with['blockers']['bottom'].is_blocker
			and player.down_momentum == start_momentum):
				player.grounded      = False
				player.down_momentum = 0 
		
		#CHANGE DOWN MEMENTUM WHEN JUMPING
		if (player.down_momentum != max_down 
		    and not player.grounded
			and not player.laddered):
				player.down_momentum += jump_change
			
		#FALL OR ASCEND bottomD ON CURRENT DOWN MOMENTUM
		if not player.grounded and not player.laddered:
			player.update_p_rect_y()
			DISPLAYSURF.blit(backgroundimg.subsurface(player), player)
			dirty_rects.append(Rect((player.x, player.y), player.size))
			player.move(myutil.DOWN, player.down_momentum)
			player.update_tblr_rects()
		
		###FOR SMOOTH LANDING BETTER WAY???
		collided_with['floors']   = dict(player.get_collisions(floors,   SQUARESIZE))
		collided_with['blockers'] = dict(player.get_collisions(blockers, SQUARESIZE))
		
		#LAND ON FLOOR OR BLOCKER WITHOUT GOING THROUGH IT
		if (collided_with['floors']['player'].tag == 'floor'
			and player.p_rect.bottom <= collided_with['floors']['player'].top
			and player.down_momentum > 0
			and player.p_rect.left <= collided_with['floors']['player'].right
			and player.p_rect.right >= collided_with['floors']['player'].left):
				player.grounded       = True
				player.down_momentum  = start_momentum
				DISPLAYSURF.blit(backgroundimg.subsurface(player), player)
				dirty_rects.append(Rect((player.x, player.y), player.size))
				player.top = collided_with['floors']['player'].top - SQUARESIZE[0]
		elif (collided_with['blockers']['player'].is_blocker
			  and player.p_rect.bottom <= collided_with['blockers']['player'].top
			  and player.down_momentum > 0
			  and player.p_rect.left <= collided_with['blockers']['player'].right
			  and player.p_rect.right >= collided_with['blockers']['player'].left):
				player.grounded       = True
				player.down_momentum  = start_momentum
				DISPLAYSURF.blit(backgroundimg.subsurface(player), player)
				dirty_rects.append(Rect((player.x, player.y), player.size))
				player.top = collided_with['blockers']['player'].top - SQUARESIZE[0]
				player.update_tblr_rects()
				
		#PREVENT PLAYER FROM JUMPING THROUGH BLOCKERS
		if (collided_with['blockers']['player'].is_blocker
			  and player.p_rect.top >= collided_with['blockers']['player'].bottom
			  and player.down_momentum <= 0
			  and player.p_rect.left <= collided_with['blockers']['player'].right
			  and player.p_rect.right >= collided_with['blockers']['player'].left):
				player.down_momentum  = 0
				DISPLAYSURF.blit(backgroundimg.subsurface(player), player)
				dirty_rects.append(Rect((player.x, player.y), player.size))
				player.bottom = collided_with['blockers']['player'].bottom + SQUARESIZE[0]
				player.update_tblr_rects()
		###EVENT ------
		
		#DRAW ------
		for ladder in ladders:
			ladder.draw(DISPLAYSURF)
		for item in items:
			item.draw(DISPLAYSURF)
		for floor in floors:
			floor.draw(DISPLAYSURF)	
		for blocker in blockers:
			if blocker.tag != 'breakable':
				blocker.draw(DISPLAYSURF)
		
		#HIGHLIGHT CLICKABLE THINGS
		###ADD WAY THAT MORE THAN JUST BREAKABLE CAN BE CLICKED
		for blocker in blockers:
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
						myutil.highlight_rect(DISPLAYSURF, blocker, myutil.BLUE, alpha_value = 155)
						dirty_rects.append(Rect((blocker.x, blocker.y), blocker.size))
			
		player.draw(DISPLAYSURF)
		#DRAW ------
		
		#UPKEEP ------
	#	player.update_tblr_rects() ###SHOULD BE ENABLED???

		dirty_rects.append(Rect((player.x, player.y), player.size))
		
		if level_just_loaded:
			pygame.display.update()
			level_just_loaded = False
		
		pygame.display.update(dirty_rects)
		
		dirty_rects = []
		
		FPSCLOCK.tick(FPS)
		#UPKEEP ------
		
if __name__ == '__main__':
	main()