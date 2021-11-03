from Jogador import Jogador

class Inicio:

	def __init__(self, screen):

		self.screen = screen

		from Button import Button
		import constants

		self.player1Text = Button(screen, (constants.BUTTON_HEIGHT, constants.BUTTON_HEIGHT), "Jogador", outline=False)
		self.player2Text = Button(screen, (constants.SCREEN_HEIGHT - 3 * constants.BUTTON_HEIGHT, constants.BUTTON_HEIGHT), "IA", outline=False)

		self.player1 = None
		self.player2 = None

		self.player1AlgoButtons = [
			Button(screen, (self.player1Text.getBottomUp()[0], self.player1Text.getBottomUp()[1] + constants.BETWEEN_BUTTONS_Y_SPACE), "humano")
		]

		self.player1PiecesButtons = [
			Button(screen, (self.player1Text.getBottomUp()[0], self.player1Text.getBottomUp()[1] + 2 * constants.BETWEEN_BUTTONS_Y_SPACE), "Cachorros")
		]

		self.player2AlgoButtons = [
			Button(screen, (self.player2Text.getBottomUp()[0], self.player2Text.getBottomUp()[1] + constants.BETWEEN_BUTTONS_Y_SPACE), "IA")
		]

		self.player2PiecesButtons = [
			Button(screen, (self.player2Text.getBottomUp()[0], self.player2Text.getBottomUp()[1] + 2 * constants.BETWEEN_BUTTONS_Y_SPACE), "Onça")
		]

		left = self.player1PiecesButtons[0].getBottomUp()
		right = self.player2PiecesButtons[0].getBottomUp()

		left = (left[0] + constants.BUTTON_HEIGHT + (right[0] - left[0] - 2 * constants.BUTTON_HEIGHT) // 2, left[1] + constants.BUTTON_WIDTH)

		self.startButton = Button(screen, left, "Iniciar", outline = True)

	def drawState0(self):

		self.player1Text.draw()
		self.player2Text.draw()

		for button in self.player1AlgoButtons:
			button.draw()

		for button in self.player2AlgoButtons:
			button.draw()

		for button in self.player1PiecesButtons:
			button.draw()

		for button in self.player2PiecesButtons:
			button.draw()

		self.startButton.draw()

	def getPressed(self, clickCoords): 

		import constants

		for button in self.player1AlgoButtons:
			if button.pressed(clickCoords):
				button.setColor(constants.GREEN)
				text = button.getText()
    
				if text == "humano":
					self.player1AlgoButtons[0].setColor(constants.GREEN)
					self.player2AlgoButtons[0].setColor(constants.BLUE)
    


		for button in self.player1PiecesButtons:
			if button.pressed(clickCoords):
				button.setColor(constants.GREEN)
				text = button.getText()
    
				if text == "Cachorros":
						self.player1PiecesButtons[0].setColor(constants.GREEN)
						self.player2PiecesButtons[0].setColor(constants.BLUE)
					
			


		


	def pickUpParameters(self): # if the user pressed the start button get the parameters

		import constants
		from Jogador import Jogador
		from IA import IA

		player1Algo = ""
		player2Algo = ""

		if self.player1AlgoButtons[0].getColor() == constants.GREEN:
			player1Algo = "humano"

		if self.player2AlgoButtons[0].getColor() == constants.BLUE:
			player2Algo = "IA"

		from Cachorro import Cachorro
		from Onca import Onca

		if player1Algo != "" and player2Algo != "":
			if self.player1PiecesButtons[0].getColor() == constants.GREEN:

				if player1Algo == "humano":
					self.player1 = Jogador(Cachorro())
				elif player1Algo != "":
					self.player1 = IA(Cachorro(), player1Algo)

				if player2Algo == "humano":
					self.player2 = Jogador(Onca())
				elif player2Algo != "":
					self.player2 = IA(Onca(), player2Algo)

			elif self.player1PiecesButtons[1].getColor() == constants.GREEN:

				if player1Algo == "humano":
					self.player1 = Jogador(Onca())
				elif player1Algo != "":
					self.player1 = IA(Onca(), player1Algo)

				if player2Algo == "humano":
					self.player2 = Jogador(Cachorro())
				elif player2Algo != "":
					self.player2 = IA(Cachorro(), player2Algo)

	def runState0(self): 

		import pygame, constants

		for event in pygame.event.get():

			self.screen.fill(constants.WHITE)
			self.drawState0()

			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
				return ("exit", self.player1, self.player2)
			else:
				if event.type == pygame.MOUSEBUTTONDOWN:
					clickCoords = event.pos
					self.getPressed(clickCoords)
					if self.startButton.pressed(clickCoords):
						self.pickUpParameters()
						for button in self.player1AlgoButtons:
							button.setColor(constants.WHITE)

						for button in self.player2AlgoButtons:
							button.setColor(constants.VERDEX)

		pygame.display.flip()

		return ("tela inicial", self.player1, self.player2)


	def drawState1(self):

		import constants
		from IA import IA

		self.screen.fill(constants.WHITE)


		
		if isinstance(self.player2, IA):
			self.player2Text.draw()

			self.player2AlgoButtons[0].setText("Media")

			for button in self.player2AlgoButtons:
				button.draw()

			self.startButton.draw()

	def state1_checkPressed(self, clickCoords):

		import constants
		from IA import IA

		if isinstance(self.player2, IA):
			for button in self.player2AlgoButtons:
				if button.pressed(clickCoords):
					button.setColor(constants.BLUE)
					text = "Media"

					
					

	def setDifficulties(self):

		from IA import IA
		import constants

	

		if isinstance(self.player2, IA):

			if self.player2AlgoButtons[0].getColor() == constants.GREEN:
				self.player2.setDifficulty("easy")

	def runState1(self):

		import pygame, constants

		for event in pygame.event.get():

			self.screen.fill(constants.WHITE)
			self.drawState1()

			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
				return "sair", self.player1, self.player2
			else:
				if event.type == pygame.MOUSEBUTTONDOWN:
					clickCoords = event.pos
					self.state1_checkPressed(clickCoords)

					if self.startButton.pressed(clickCoords):
						self.setDifficulties()
						return "jogo", self.player1, self.player2


		pygame.display.flip()

		return "tela inicial", self.player1, self.player2

	def run(self):

		import pygame

		if self.player1 is None:
			return self.runState0()
		else:
			if isinstance(self.player1, Jogador) and isinstance(self.player2, Jogador):
				return "jogo", self.player1, self.player2
			return self.runState1()