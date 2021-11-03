from Inicio import Inicio


class App:

	def __init__(self):

		import pygame
		import constants

		pygame.init()
		self.screen = pygame.display.set_mode([constants.SCREEN_HEIGHT, constants.SCREEN_WIDTH])
		pygame.display.set_caption("Andrei Blahovici Adugo")

		self.running = True

	def run(self): 

		from Jogo import Jogo

		mode = "tela inicial"
		homescreen = Inicio(self.screen)
		while self.running:

			if mode == "tela inicial":
				mode, player1, player2 = homescreen.run()
				if mode != "tela inicial":
					game = Jogo(self.screen, player1, player2)
			elif mode == "jogo":
				mode, player1, player2 = game.run()
				if mode != "jogo":
					homescreen = Inicio(self.screen)
			else:
				self.running = False
			