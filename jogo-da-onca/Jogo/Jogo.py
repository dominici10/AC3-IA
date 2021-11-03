from pygame.constants import KEYDOWN

class Jogo:

	def __init__(self, screen, player1, player2):

		import copy, constants
		from Jogador import Jogador
		from Onca import Onca
		from Cachorro import Cachorro
		from IA import IA
		import time

		self.screen = screen
		self.screen.fill(constants.WHITE)

		self.grid = copy.deepcopy(constants.DEFAULT_GRID)
		self.adjacencyList = copy.deepcopy(constants.ADJACENCY_LIST)
		self.selected = (None, None)

		if isinstance(player1, IA) and isinstance(player2, IA): 
			player2.setHeuristic(2)

		if player1.getPieceType() == "cachorro": 
			player1, player2 = player2, player1

		self.players = [player1, player2]
		self.turn = 0
		self.animation = []
		self.moveTimes = [[], []]
		self.playerStartTime = None
		self.totalMoves = [0, 0]
		self.generatedNodes = [[], []]

		if isinstance(self.players[self.turn], Jogador):
			self.playerStartTime = time.time()

		self.mapCoordinates()

		for i in range(len(self.grid)): # print initial grid
			print(self.grid[i])

		print("Turno da Onça")

	# map grid cells to on screen coordinates
	def mapCoordinates(self):

		import constants

		self.onScreenCoordinates = []

		row = [(constants.SCREEN_HEIGHT // 5, constants.SCREEN_WIDTH // 15)]
		for i in range(1, len(self.grid[0])):
			row.append((row[i - 1][0] + constants.SQUARE_LENGTH, row[i - 1][1]))

		self.onScreenCoordinates.append(row)

		for i in range(1, len(self.grid)):
			for j in range(len(self.grid[i])):
				if j == 0:
					row = [(row[0][0], row[0][1] + constants.SQUARE_LENGTH)]
				else:
					row.append((row[j - 1][0] + constants.SQUARE_LENGTH, row[j - 1][1]))
				if j == len(self.grid[i]) - 1:
					self.onScreenCoordinates.append(row)


	# draws the grid with respect to the selected piece
	def drawGrid(self):

		import pygame, constants
		from Utilities import Utilities
		import constants

		self.screen.fill(constants.WHITE)

		# draw segments
		for node in range(len(self.grid) * len(self.grid[0])):
			for nextNode in self.adjacencyList[node]:
				i1, j1 = Utilities.nodeToCell(self.grid, node)
				i2, j2 = Utilities.nodeToCell(self.grid, nextNode)

				x = self.onScreenCoordinates[i1][j1]
				y = self.onScreenCoordinates[i2][j2]

				pygame.draw.line(self.screen, constants.BLACK, x, y, constants.SQUARE_SIDE_WIDTH)

		for node in range(len(self.grid) * len(self.grid[0])): # draw pieces

			i, j = Utilities.nodeToCell(self.grid, node)

			if self.grid[i][j] == 'j':

				center = self.onScreenCoordinates[i][j]
				radius = constants.CIRCLE_RADIUS

				if self.selected == (i, j):
					pygame.draw.circle(self.screen, constants.RED, center, radius)
				pygame.draw.circle(self.screen, constants.BLACK, center, radius - 2)


			elif self.grid[i][j] == 'd':

				center = self.onScreenCoordinates[i][j]
				radius = constants.CIRCLE_RADIUS

				if self.selected == (i, j):
					pygame.draw.circle(self.screen, constants.RED, center, radius)
				pygame.draw.circle(self.screen, constants.CACHORRO, center, radius - 2)

		pygame.display.flip()

	
	def drawEndGrid(self):

		import pygame, constants
		from Utilities import Utilities
		import constants

		self.screen.fill(constants.WHITE)

		for i in range(len(self.grid)):
			for j in range(len(self.grid[0])):
				if self.grid[i][j] == 'j':
					jaguar = (i, j)

		# draw segments
		for node in range(len(self.grid) * len(self.grid[0])):
			for nextNode in self.adjacencyList[node]:
				i1, j1 = Utilities.nodeToCell(self.grid, node)
				i2, j2 = Utilities.nodeToCell(self.grid, nextNode)

				x = self.onScreenCoordinates[i1][j1]
				y = self.onScreenCoordinates[i2][j2]

				pygame.draw.line(self.screen, constants.BLACK, x, y, constants.SQUARE_SIDE_WIDTH)

		for node in range(len(self.grid) * len(self.grid[0])): # draw pieces

			i, j = Utilities.nodeToCell(self.grid, node)

			if self.grid[i][j] == 'j':

				center = self.onScreenCoordinates[i][j]
				radius = constants.CIRCLE_RADIUS

				pygame.draw.circle(self.screen, constants.BLACK, center, radius - 2)


			elif self.grid[i][j] == 'd':

				center = self.onScreenCoordinates[i][j]
				radius = constants.CIRCLE_RADIUS

				dogNode = Utilities.cellToNode(self.grid, (i, j))
				jaguarNode = Utilities.cellToNode(self.grid, jaguar)


				if dogNode in constants.ADJACENCY_LIST[jaguarNode]:
					pygame.draw.circle(self.screen, constants.RED, center, radius)
				pygame.draw.circle(self.screen, constants.GRAY, center, radius - 2)

		pygame.display.flip()

	
	def run(self):

		import pygame, constants
		from IA import IA
		from Utilities import Utilities
		from Jogador import Jogador
		import time
		import copy
		import statistics

		for event in pygame.event.get():

			self.drawGrid()

			endGame = Utilities.endGame(self.grid)

			if endGame is not None: # if someone won print all the required stuff
				print("Total move player 0: ", self.totalMoves[0])
				print("Total move player 1: ", self.totalMoves[1])
				if isinstance(self.players[0], IA):

					if len(self.moveTimes[0]):
						print("Player 0 times:")
						print("Max time: ", max(self.moveTimes[0]))
						print("Min time: ", min(self.moveTimes[0]))
						print("Mean time: ", statistics.mean(self.moveTimes[0]))
						print("Median: ", statistics.median(self.moveTimes[0]))
					else:
						print("Player 0 made no moves")

					if len(self.generatedNodes[0]):
						print("Player 0 nodes:")
						print("Max nodes:", max(self.generatedNodes[0]))
						print("Min nodes:", min(self.generatedNodes[0]))
						print("Mean nodes:", statistics.mean(self.generatedNodes[0]))
						print("Median:", statistics.median(self.generatedNodes[0]))
					else:
						print("Player 1 made no moves")

				if isinstance(self.players[1], IA):

					if len(self.moveTimes[1]):
						print("Player 1 times:")
						print("Max time: ", max(self.moveTimes[1]))
						print("Min time: ", min(self.moveTimes[1]))
						print("Mean time: ", statistics.mean(self.moveTimes[1]))
						print("Median: ", statistics.median(self.moveTimes[1]))
					else:
						print("Player 1 made no moves")

					if len(self.generatedNodes[1]):
						print("Player 1 nodes:")
						print("Max nodes:", max(self.generatedNodes[1]))
						print("Min nodes:", min(self.generatedNodes[1]))
						print("Mean nodes:", statistics.mean(self.generatedNodes[1]))
						print("Median:", statistics.median(self.generatedNodes[1]))
					else:
						print("Player 1 made no moves")

				print(endGame)

				if endGame[0] == 'D':
					self.drawEndGrid()
				else:
					for i in range(len(self.grid)):
						for j in range(len(self.grid[0])):
							if self.grid[i][j] == 'j':
								jaguar = (i, j)
					self.selected = jaguar
					self.drawGrid()

				time.sleep(2)

				return "sair", self.players[0], self.players[1]

			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:

				if isinstance(self.players[0], IA):

					if len(self.generatedNodes[0]):
						print("Nós do jogador 0:")
						print("Max Nós:", max(self.generatedNodes[0]))
						print("Min Nós:", min(self.generatedNodes[0]))
						print("Mean Nós:", statistics.mean(self.generatedNodes[0]))
						print("Median:", statistics.median(self.generatedNodes[0]))
					else:
						print("O jogador 1 não fez nenhum movimento")

				if isinstance(self.players[1], IA):

					if len(self.generatedNodes[1]):
						print("Player 1 Nós:")
						print("Max Nós:", max(self.generatedNodes[1]))
						print("Min Nós:", min(self.generatedNodes[1]))
						print("Mean Nós:", statistics.mean(self.generatedNodes[1]))
						print("Median:", statistics.median(self.generatedNodes[1]))
					else:
						print("O jogador 1 não fez nenhum movimento")

				print("Total de movimentos do jogador 0: ", self.totalMoves[0])
				print("Total de movimentos do jogador 1: ", self.totalMoves[1])


				return "sair", self.players[0], self.players[1]

			if isinstance(self.players[self.turn], IA):

				start = time.time()
				states, score, genNodes = self.players[self.turn].makeMove(self.grid)
				end = time.time()

				self.generatedNodes[self.turn].append(genNodes)

				for state in states:

					frm = state.getFrom()
					self.selected = frm

					self.drawGrid()
					time.sleep(1.5)
					self.grid = state.getGrid()

					self.drawGrid()

				print("Estimativa de movimento do jogador ", self.turn, ": ", score)
				print("Número de nós gerados: ", genNodes)

				self.moveTimes[self.turn].append(end - start)
				print("Jogador " + str(self.turn) + " fez um movimento " + str(end - start))

				self.turn ^= 1
				self.totalMoves[self.turn] += 1

				if isinstance(self.players[self.turn], Jogador):
					self.playerStartTime = time.time()

				if self.turn == 0:
					print("Turno da Onça")
				else:
					print("Turno do Cachorro")

				self.selected = (None, None)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				clickCoords = event.pos

				row, col = Utilities.clickCoordsToCell(self.onScreenCoordinates, self.grid, clickCoords)

				selected = self.players[self.turn].selectPiece(self.grid, (row, col))
				if selected:
					self.selected = (row, col)
				else: # actual move
					if row is not None and col is not None and self.selected != (None, None):
						leftTurns = self.players[self.turn].makeMove(self.grid, self.selected, (row, col))

						if leftTurns == 0:

							end = time.time()
							self.moveTimes[self.turn].append(end - self.playerStartTime)

							print("Jogador " + str(self.turn) + " fez um movimento " + str(end - self.playerStartTime))

							self.turn ^= 1
							self.totalMoves[self.turn] += 1

							if isinstance(self.players[self.turn], Jogador):
								self.playerStartTime = time.time()

							if self.turn == 0:
								print("Turno da Onça")
							else:
								print("Turno do Cachorro")



		return "jogo", self.players[0], self.players[1]