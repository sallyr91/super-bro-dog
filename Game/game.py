###FIX PROBLEM WHEN A THING IS OUT OF BOUNDS GAME CRASHES
###FIX USE OF ALL COLLISIONS FOR LOCKS
###ADD LEVEL AND PERHAPS WORLD OBJECT TO CONTAIN THING LISTS
###IF YOU FALL OFF LADDER AND HOLD DOWN ARROW IMAGE DOES NOT CHANGE WHEN HITTING GROUND
import master
from master import Player
from master import Thing
from master import Level
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
	DISPLAYSURF = pygame.display.set_mode(SCREENSIZE)#FULLSCREEN)
	FPS         = 60
	FPSCLOCK    = pygame.time.Clock()
	SQUARESIZE  = (32, 32)
	#CONSTANTS ------
	
	#CHARACTER IMAGES ------
	character_sheet_image = myutil.load_image('character-sheet.png', 
											  'general-images', myutil.COLORKEY)
	character_images = myutil.chop_image(character_sheet_image, SQUARESIZE)
	playerimgs = {'left'      : character_images[0][1],
				  'right'     : character_images[1][1],
				  'jumpleft'  : character_images[0][0],
				  'jumpright' : character_images[1][0],
				  'laddered'  : character_images[0][0]}
	#CHARACTER IMAGES ------
	
	#INVENTORY IMAGES ------
	inventory_sheet_image = myutil.load_image('inventory-sheet.png', 
											  'general-images', myutil.COLORKEY)
	inventory_images = myutil.chop_image(inventory_sheet_image, SQUARESIZE)
	key_icon_image = inventory_images[0][0]
	hammer_outline_image = inventory_images[1][0]
	hammer_icon_image = inventory_images[2][0]
	#INVENTORY IMAGES ------
	
	#ITEM IMAGES ------
	item_sheet_image = myutil.load_image('item-sheet.png', 
									     'general-images', 
										 myutil.COLORKEY)
	item_images = myutil.chop_image(item_sheet_image, SQUARESIZE)
	key_image = item_images[0][0]
	hammer_image = item_images[1][0]
	win_image = item_images[2][0]
	#ITEM IMAGES ------
	
	#WORLD1 IMAGES ------
	world1_sheet_image = myutil.load_image('world1-sheet.png', 
										   'world1', myutil.COLORKEY)
	world1_images = myutil.chop_image(world1_sheet_image, SQUARESIZE)
	floor_image = world1_images[0][0]
	ladder_image = world1_images[1][0]
	wall_image = world1_images[2][0]
	breakable_image = world1_images[0][1]
	hammerable_image = world1_images[1][1]
	lock_image = world1_images[2][1]
	background_image = myutil.load_image('world1-background.png', 'world1')
	world1_images = {
					 'floor' : floor_image,
					 'ladder' : ladder_image,
					 'wall' : wall_image,
					 'breakable' : breakable_image,
					 'hammerable' : hammerable_image,
					 'lock' : lock_image,
					 'key' : key_image,
					 'hammer' : hammer_image,
					 'win' : win_image,
					 'background' : background_image
					}
	#WORLD1 IMAGES ------
	
	#----#
	#MENU#
	#----#
	global at_menu
	at_menu = True
	def change_menu_status():
		global at_menu
		at_menu = not at_menu
		
	menu_margin = 8
	menu_start_image = myutil.load_image('menu-start.png', 'general-images')
	menu_start_highlighted_image = myutil.load_image('menu-start-highlighted.png', 'general-images')
	menu_logo_image = myutil.load_image('menu-logo.png', 'general-images')
	menu_quit_image = myutil.load_image('menu-quit.png', 'general-images')
	menu_quit_highlighted_image = myutil.load_image('menu-quit-highlighted.png', 'general-images')
	logo_button = myutil.Button((menu_margin, menu_margin), 
								 (menu_logo_image.get_width(), 
								 menu_logo_image.get_height()), 
								 menu_logo_image, 
								 menu_logo_image, 
								 'logo')
	start_button = myutil.Button((menu_margin, logo_button.bottom+menu_margin), 
								 (menu_start_image.get_width(), 
								 menu_start_image.get_height()), 
								 menu_start_image, 
								 menu_start_highlighted_image, 
								 'start',
								 change_menu_status)
	quit_button = myutil.Button((menu_margin, start_button.bottom+menu_margin), 
								 (menu_quit_image.get_width(), 
								 menu_quit_image.get_height()), 
								 menu_quit_image, 
								 menu_quit_highlighted_image, 
								 'quit',
								 myutil.terminate)
	menu_buttons = myutil.ButtonGroup('group1', logo_button, 
									  start_button, quit_button)
	menu = myutil.Menu(menu_buttons)
	
	#PHYSICS ------
	start_momentum = -5.4
	max_down = 5.4
	max_up = -5.4
	jump_change = .2
	move_amount = 2
	#PHYSICS ------
	
	#OTHER ------
	worlds = [[Level('w1-l1', 'world1', 'level1.txt', world1_images),
			   Level('w1-l2', 'world1', 'level2.txt', world1_images),
			   Level('w1-l3', 'world1', 'level3.txt', world1_images),
			   Level('w1-l4', 'world1', 'level4.txt', world1_images),
			   Level('w1-l5', 'world1', 'level5.txt', world1_images)]]
	current_level = 0
	current_world = 0
	level_just_loaded = True
	dirty_rects = []
	#OTHER ------
	
	#INVENTORY LOCATIONS ------
	key_icon_location = cc(0, 14)
	hammer_icon_location = cc(1, 14)
	#INVENTORY LOCATIONS ------
	
	start_location = worlds[current_world][current_level].start
	
	player = Player(start_location,
	                SQUARESIZE,
				    myutil.RIGHT,
					True,
					False,
					start_momentum,
				    playerimgs,
					myutil.SpriteGroup(ladder_image, breakable_image, hammer_image))
	
	#-----------------------------#
	#DUMMY OBJECT FOR NO COLLISION#
	#-----------------------------#
	dum_thing = Thing((-50, -50), SQUARESIZE, None, None, None, None, None)
	
	#---------#
	#GAME LOOP#
	#---------#
	while True:
		pygame.event.pump()
		
		keyboard = pygame.key.get_pressed()
		
		if at_menu:
			DISPLAYSURF.fill(myutil.BLACK)
			menu.draw(DISPLAYSURF)
			button = menu.get_moused_over_button()
			if button:
				menu.highlight_button(DISPLAYSURF, button.tag)
			clicked_button = menu.get_clicked_button()
			if clicked_button:
				clicked_button.action()
				if not at_menu:
					DISPLAYSURF.blit(background_image, (0, 0))
			
		if not at_menu:
			#------------------------------#
			#GET PLAYER AND ITEM COLLISIONS#
			#------------------------------#
			player.set_collisions('items', 
								  worlds[current_world][current_level].items,
								  dum_thing)
			player.set_collisions('ladders', 
								  worlds[current_world][current_level].ladders,
								  dum_thing)
			player.set_collisions('floors', 
							      worlds[current_world][current_level].floors,
								  dum_thing)
			player.set_collisions('blockers', 
								  worlds[current_world][current_level].blockers,
								  dum_thing)
			
			for item in worlds[current_world][current_level].items:
				if item.can_fall:
					item.set_collisions('floors', 
									    worlds[current_world][current_level].floors,
										dum_thing)
					item.set_collisions('blockers', 
										worlds[current_world][current_level].blockers,
										dum_thing)

			#-------------------------------------------------#
			#WHEN ON LADDER AND TOUCHING FLOOR BECOME GROUNDED#
			#-------------------------------------------------#
			if(player.laddered
			   and player.collisions['floors']['bottom'].tag == 'floor'
			   and player.collisions['floors']['bottom'] != player.collisions['floors']['self']):
					player.grounded = True
					player.laddered = False
					player.down_momentum = start_momentum
					DISPLAYSURF.blit(background_image.subsurface(player), player)
					dirty_rects.append(Rect((player.x, player.y), player.size))
			
			#--------------#
			#KEYBOARD INPUT#
			#--------------#
			if keyboard[K_UP]:
				if (player.collisions['ladders']['self'].tag == 'ladder' 
					and not player.collisions['blockers']['top'].is_blocker):
						if not player.laddered:
							player.laddered = True
							player.grounded = False
						player.direction = myutil.UP
						player.update_p_rect_y()
						DISPLAYSURF.blit(background_image.subsurface(player), player)
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
						DISPLAYSURF.blit(background_image.subsurface(player), player)
						dirty_rects.append(Rect((player.x, player.y), player.size))
						player.move(myutil.DOWN, move_amount)
						player.update_tblr_rects()
			
			if keyboard[K_LEFT]:
				player.direction = myutil.LEFT
				player.update_p_rect_x()
				DISPLAYSURF.blit(background_image.subsurface(player), player)
				dirty_rects.append(Rect((player.x, player.y), player.size))
				if (player.left != SCREENSIZE[0] - SCREENSIZE[0]
					and not player.collisions['blockers']['left'].is_blocker):
						player.move(myutil.LEFT, move_amount)
						player.update_tblr_rects()
				
			if keyboard[K_RIGHT]:
				player.direction = myutil.RIGHT
				player.update_p_rect_x()
				DISPLAYSURF.blit(background_image.subsurface(player), player)
				dirty_rects.append(Rect((player.x, player.y), player.size))
				if (player.right != SCREENSIZE[0] 
					and not player.collisions['blockers']['right'].is_blocker):
						player.move(myutil.RIGHT, move_amount)
						player.update_tblr_rects()
				
			if keyboard[K_SPACE]:
				if (player.grounded 
					and not player.laddered
					and not player.collisions['blockers']['top'].is_blocker
					and not player.top == SCREENSIZE[1] - SCREENSIZE[1]):
						player.grounded = False
				
			if keyboard[K_ESCAPE]:
				myutil.terminate()
			
			#-------------#
			#AQUIRE HAMMER#
			#-------------#
			if player.collisions['items']['self'].tag == 'hammer':
				player.has_hammer = True
				worlds[current_world][current_level].items.remove(player.collisions['items']['self'])
				DISPLAYSURF.blit(background_image.subsurface(player.collisions['items']['self']), player.collisions['items']['self'])
				dirty_rects.append(Rect((player.collisions['items']['self'].x, player.collisions['items']['self'].y), 
																	 player.collisions['items']['self'].size))
				DISPLAYSURF.blit(background_image.subsurface(Rect(hammer_icon_location, SQUARESIZE)), hammer_icon_location)
				dirty_rects.append(Rect(SQUARESIZE, hammer_icon_location))
			
			#-------------------------------------------#
			#AQUIRE KEY OR REMOVE LOCK IF YOU HAVE A KEY#
			#-------------------------------------------#
			if player.collisions['items']['self'].tag == 'key':
				player.key_count += 1
				worlds[current_world][current_level].items.remove(player.collisions['items']['self'])
				DISPLAYSURF.blit(background_image.subsurface(player.collisions['items']['self']), player.collisions['items']['self'])
				dirty_rects.append(Rect((player.collisions['items']['self'].x, player.collisions['items']['self'].y), 
																	 player.collisions['items']['self'].size))
			elif (player.key_count > 0
				  and 'lock' in player.get_all_collision_tags('blockers')):
					player.key_count -= 1
					for thing in player.collisions['blockers']['all']:
						if thing.tag == 'lock':
							worlds[current_world][current_level].blockers.remove(thing)
							DISPLAYSURF.blit(background_image.subsurface(thing), thing) 
							dirty_rects.append(Rect((thing.x, thing.y), thing.size))
					###WORKS BUT COLLISIONS STILL IN REGULAR NON ALL LISTS PROBLEM?
			
			#-----------------------------------#
			#PREVENT PLAYER ODD LADDER POSITIONS#
			#-----------------------------------#
			if player.laddered and player.y%2 != 0:
				player.update_p_rect_y()
				DISPLAYSURF.blit(background_image.subsurface(player), player)
				dirty_rects.append(Rect((player.x, player.y), player.size))
				player.y -= 1
				player.update_tblr_rects()
			
			#--------------------------#
			#FALL WHEN EXITING A LADDER#
			#--------------------------#
			if (player.collisions['ladders']['self'].tag != 'ladder' 
				and player.laddered):
					player.laddered = False
					if not player.grounded:
						player.down_momentum = 0
			
			#------------------------------------#
			#HAVE ITEMS FALL WHEN NOT ON ANYTHING#
			#------------------------------------#
			for item in worlds[current_world][current_level].items:
				if item.can_fall:
					if (item.collisions['floors']['bottom'].tag == None
						and not item.collisions['blockers']['bottom'].is_blocker
						and item.collisions['blockers']['self'].tag == None
						and item.down_momentum == start_momentum):
							item.grounded      = False
							item.down_momentum = 0
							
					if (item.down_momentum != max_down 
						and not item.grounded):
							item.down_momentum += jump_change
							
					if not item.grounded:
						item.update_p_rect_y()
						DISPLAYSURF.blit(background_image.subsurface(item), item)
						dirty_rects.append(Rect((item.x, item.y), item.size))
						item.move(myutil.DOWN, item.down_momentum)
						item.update_tblr_rects()
						
					item.set_collisions('floors', worlds[current_world][current_level].floors, dum_thing)
					item.set_collisions('blockers', worlds[current_world][current_level].blockers, dum_thing)
						
					if (item.collisions['floors']['self'].tag == 'floor'
						and item.p_rect.bottom <= item.collisions['floors']['self'].top
						and item.down_momentum > 0
						and item.p_rect.left <= item.collisions['floors']['self'].right
						and item.p_rect.right >= item.collisions['floors']['self'].left):
							item.grounded      = True
							item.down_momentum = start_momentum
							DISPLAYSURF.blit(background_image.subsurface(item), item)
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
							DISPLAYSURF.blit(background_image.subsurface(item), item)
							dirty_rects.append(Rect((item.x, item.y), item.size))
							item.top = item.collisions['blockers']['self'].top - SQUARESIZE[0]
							item.update_tblr_rects()

			#------------------------------------------------------#
			#CHANGE DOWN MEMENTUM OF PLAYER WHEN JUMPING OR FALLING#
			#------------------------------------------------------#
			if (player.down_momentum != max_down 
				and not player.grounded
				and not player.laddered):
					player.down_momentum += jump_change
			#------------------------------------------------------#
			
			#---------------------------------------------#
			#FALL OR ASCEND BASED ON CURRENT DOWN MOMENTUM#
			#---------------------------------------------#
			if not player.grounded and not player.laddered:
				player.update_p_rect_y()
				DISPLAYSURF.blit(background_image.subsurface(player), player)
				dirty_rects.append(Rect((player.x, player.y), player.size))
				player.move(myutil.DOWN, player.down_momentum)
				player.update_tblr_rects()
			#---------------------------------------------#
			
			###FOR SMOOTH LANDING BETTER WAY???
			###!!!!!!!!!!!!WATCH PLACEMENT OF CODE BEFORE AND AFTER THIS!
			player.set_collisions('floors', worlds[current_world][current_level].floors, dum_thing)
			player.set_collisions('blockers', worlds[current_world][current_level].blockers, dum_thing)
			
			#-----------------------------#
			#FALL WHEN WALKING OVER A HOLE#
			#-----------------------------#
			if (player.collisions['floors']['bottom'].tag == None
				and not player.collisions['blockers']['bottom'].is_blocker
				and player.down_momentum == start_momentum):
					player.grounded      = False
					player.down_momentum = 0
					player.update_p_rect_y() ###IS THIS A GOOD IDEA TO FALL OVER A HOLE????
					DISPLAYSURF.blit(background_image.subsurface(player), player)
					dirty_rects.append(Rect((player.x, player.y), player.size))
					player.move(myutil.DOWN, move_amount/2)
					player.update_tblr_rects()
			#-----------------------------#
			
			#---------------------------------------------------#
			#LAND ON FLOOR OR BLOCKER WITHOUT FALLING THROUGH IT#
			#---------------------------------------------------#
			if (player.down_momentum > 0
				and player.collisions['floors']['bottom'].tag == 'floor'
				and player.p_rect.bottom <= player.collisions['floors']['bottom'].top
				and player.p_rect.left <= player.collisions['floors']['bottom'].right
				and player.p_rect.right >= player.collisions['floors']['bottom'].left):
					player.grounded      = True
					player.down_momentum = start_momentum
					DISPLAYSURF.blit(background_image.subsurface(player), player)
					dirty_rects.append(Rect((player.x, player.y), player.size))
					player.top = player.collisions['floors']['bottom'].top - SQUARESIZE[0]
					player.update_tblr_rects()
			elif (player.collisions['blockers']['bottom'].is_blocker
				  and player.p_rect.bottom <= player.collisions['blockers']['bottom'].top
				  and player.down_momentum > 0
				  and player.p_rect.left <= player.collisions['blockers']['bottom'].right
				  and player.p_rect.right >= player.collisions['blockers']['bottom'].left):
					player.grounded      = True
					player.down_momentum = start_momentum
					DISPLAYSURF.blit(background_image.subsurface(player), player)
					dirty_rects.append(Rect((player.x, player.y), player.size))
					player.top = player.collisions['blockers']['bottom'].top - SQUARESIZE[0]
					player.update_tblr_rects()
			#---------------------------------------------------#
			
			#-------------------------------------------------#
			#PREVENT PLAYER FROM JUMPING THROUGH TOP OF SCREEN#
			#-------------------------------------------------#
			if player.top < SCREENSIZE[1] - SCREENSIZE[1]:
				player.down_momentum = 0
				DISPLAYSURF.blit(background_image.subsurface(Rect((player.x, 0), player.size)), 
															Rect((player.x, 0), player.size))
				dirty_rects.append(Rect((player.x, player.y), player.size)) ###POSSIBLE PROBLEM HERE
				player.top = 0
				player.update_tblr_rects()
				###P RECT PROBLEM?
			
			#----------------------------------------------------#
			#PREVENT PLAYER FROM FALLING THROUGH BOTTOM OF SCREEN#
			#----------------------------------------------------#
			if player.bottom > SCREENSIZE[1]:
				player.down_momentum = start_momentum
				player.grounded = True
				DISPLAYSURF.blit(background_image.subsurface(Rect((player.x, SCREENSIZE[1]-player.size[1]), 
																							player.size)), 
														  Rect((player.x, SCREENSIZE[1]-player.size[1]), player.size))
				dirty_rects.append(Rect((player.x, player.y), player.size)) ###POSSIBLE PROBLEM HERE
				player.x, player.y = start_location
				player.update_tblr_rects()
				player.update_p_rect_x()
				player.update_p_rect_y()
			
			#--------------------------------------------#
			#PREVENT PLAYER FROM JUMPING THROUGH BLOCKERS#
			#--------------------------------------------#
			if (player.collisions['blockers']['self'].is_blocker
				and player.p_rect.top >= player.collisions['blockers']['self'].bottom
				and player.down_momentum <= 0
				and player.p_rect.left <= player.collisions['blockers']['self'].right
				and player.p_rect.right >= player.collisions['blockers']['self'].left):
					player.down_momentum = 0
					DISPLAYSURF.blit(background_image.subsurface(player), player)
					dirty_rects.append(Rect((player.x, player.y), player.size))
					player.bottom = player.collisions['blockers']['self'].bottom + SQUARESIZE[0]
					player.update_tblr_rects()
			#--------------------------------------------#
			
			#-------------------------------------#
			#GO TO NEXT LEVEL WHEN BONE IS AQUIRED#
			#-------------------------------------#
			if player.collisions['items']['self'].tag == 'win':
				level_just_loaded = True
				current_level += 1
				DISPLAYSURF.blit(background_image.subsurface(player.collisions['items']['self']), 
																	player.collisions['items']['self'])
				dirty_rects.append(Rect((player.collisions['items']['self'].x, 
										 player.collisions['items']['self'].y), 
										 player.collisions['items']['self'].size))
				player.has_hammer = False
				#ADD RESET METHOD TO PLAYER
										 
			#DRAW THINGS ------
			worlds[current_world][current_level].draw(DISPLAYSURF, world1_images, dirty_rects, player)
			#DRAW THINGS ------
			
			#DRAW INVENTORY -----
			DISPLAYSURF.blit(key_icon_image, key_icon_location)
			
			if not player.has_hammer:
				DISPLAYSURF.blit(hammer_outline_image, hammer_icon_location)
			else:
				DISPLAYSURF.blit(hammer_icon_image, hammer_icon_location)
			#DRAW INVENTORY -----
			
			player.draw(DISPLAYSURF)
			dirty_rects.append(Rect((player.x, player.y), player.size))
			
			player.collisions = {}
			for item in worlds[current_world][current_level].items:
				if item.can_fall:
					item.collisions = {}
					dirty_rects.append(Rect((item.x, item.y), item.size))
			
			#NEXT LEVEL ------
			if level_just_loaded and current_level == 0:
				level_just_loaded = False
				pygame.display.update()
			elif level_just_loaded and current_level > 0:
				###BETTER WAY INSTEAD OF REDRAWING???
				DISPLAYSURF.blit(background_image, (0, 0))
				player.x, player.y = start_location = worlds[current_world][current_level].start
				player.update_tblr_rects()
				worlds[current_world][current_level].draw(DISPLAYSURF, world1_images, dirty_rects, player)
				DISPLAYSURF.blit(key_icon_image, key_icon_location)
				if not player.has_hammer:
					DISPLAYSURF.blit(hammer_outline_image, hammer_icon_location)
				else:
					DISPLAYSURF.blit(hammer_icon_image, hammer_icon_location)
				level_just_loaded = False
				pygame.display.update()
			#NEXT LEVEL ------
		
		if not at_menu:
			pygame.display.update(dirty_rects)
		else:
			pygame.display.update()
			
		dirty_rects = []
		
		FPSCLOCK.tick(FPS)
		
if __name__ == '__main__':
	main()