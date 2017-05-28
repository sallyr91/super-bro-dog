import pygame
import sys
from pygame.locals import *

def terminate():
	pygame.quit()
	sys.exit()

def main():
	pygame.init()
	
	pygame.display.set_caption('game')
	
	#CONSTANTS ------
	#              wid  hei
	SCREENSIZE = (640, 480)
	DISPLAYSURF = pygame.display.set_mode(SCREENSIZE)
	FPS = 30
	FPSCLOCK = pygame.time.Clock()
	#CONSTANTS ------
	
	#COLORS ------
	BLACK = (0, 0, 0)
	#COLORS ------
	
	while True:
		#DRAW ------
		DISPLAYSURF.fill(BLACK)
		#DRAW ------
		
		#EVENT ------
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
		#EVENT ------
		
		#UPKEEP ------
		pygame.display.update()
		FPSCLOCK.tick(FPS)
		#UPKEEP ------
		
if __name__ == '__main__':
	main()