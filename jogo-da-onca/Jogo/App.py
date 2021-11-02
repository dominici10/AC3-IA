from Homescreen import Homescreen


class App:

	def __init__(self):

		import pygame
		import constants

		pygame.init()
		self.screen = pygame.display.set_mode([constants.SCREEN_HEIGHT, constants.SCREEN_WIDTH])
		pygame.display.set_caption("Andrei Blahovici Adugo")

		self.running = True

	def run(self): # defines the flow of the app: homescreen -> game -> exit

		from Game import Game

		mode = "homescreen"
		homescreen = Homescreen(self.screen)
		while self.running:

			if mode == "homescreen":
				mode, player1, player2 = homescreen.run()
				if mode != "homescreen":
					game = Game(self.screen, player1, player2)
			elif mode == "game":
				mode, player1, player2 = game.run()
				if mode != "game":
					homescreen = Homescreen(self.screen)
			else:
				self.running = False
			