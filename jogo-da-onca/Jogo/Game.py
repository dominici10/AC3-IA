from pygame.constants import KEYDOWN

'''
This class takes care of the game mechanics.
'''
class Game:

	def __init__(self, screen, player1, player2):

		import copy, constants
		from Player import Player
		from Jaguar import Jaguar
		from Dog import Dog
		from Ai import Ai
		import time

		self.screen = screen
		self.screen.fill(constants.WHITE)

		self.grid = copy.deepcopy(constants.DEFAULT_GRID)
		self.adjacencyList = copy.deepcopy(constants.ADJACENCY_LIST)
		self.selected = (None, None)

		if isinstance(player1, Ai) and isinstance(player2, Ai): # if I have to Ai's set the other one's heuristic to 2
			player2.setHeuristic(2)

		if player1.getPieceType() == "dog": # make sure jaguar makes the first move
			player1, player2 = player2, player1

		self.players = [player1, player2]
		self.turn = 0
		self.animation = []
		self.moveTimes = [[], []]
		self.playerStartTime = None
		self.totalMoves = [0, 0]
		self.generatedNodes = [[], []]

		if isinstance(self.players[self.turn], Player):
			self.playerStartTime = time.time()

		self.mapCoordinates()

		for i in range(len(self.grid)): # print initial grid
			print(self.grid[i])

		print("Jaguar's turn")

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
				pygame.draw.circle(self.screen, constants.GRAY, center, radius - 2)

		pygame.display.flip()

	# in case dogs won, draw a red circle around the ones that surround the jaguar
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

	# game logic
	def run(self):

		import pygame, constants
		from Ai import Ai
		from Utilities import Utilities
		from Player import Player
		import time
		import copy
		import statistics

		for event in pygame.event.get():

			self.drawGrid()

			endGame = Utilities.endGame(self.grid)

			if endGame is not None: # if someone won print all the required stuff
				print("Total move player 0: ", self.totalMoves[0])
				print("Total move player 1: ", self.totalMoves[1])
				if isinstance(self.players[0], Ai):

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

				if isinstance(self.players[1], Ai):

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

				return "exit", self.players[0], self.players[1]

			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]: # if the user quits the app print the required stuff

				if isinstance(self.players[0], Ai):

					if len(self.generatedNodes[0]):
						print("Player 0 nodes:")
						print("Max nodes:", max(self.generatedNodes[0]))
						print("Min nodes:", min(self.generatedNodes[0]))
						print("Mean nodes:", statistics.mean(self.generatedNodes[0]))
						print("Median:", statistics.median(self.generatedNodes[0]))
					else:
						print("Player 1 made no moves")

				if isinstance(self.players[1], Ai):

					if len(self.generatedNodes[1]):
						print("Player 1 nodes:")
						print("Max nodes:", max(self.generatedNodes[1]))
						print("Min nodes:", min(self.generatedNodes[1]))
						print("Mean nodes:", statistics.mean(self.generatedNodes[1]))
						print("Median:", statistics.median(self.generatedNodes[1]))
					else:
						print("Player 1 made no moves")

				print("Total move player 0: ", self.totalMoves[0])
				print("Total move player 1: ", self.totalMoves[1])


				return "exit", self.players[0], self.players[1]

			if isinstance(self.players[self.turn], Ai):

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

				print("Player move estimation ", self.turn, ": ", score)
				print("Number of generated nodes: ", genNodes)

				self.moveTimes[self.turn].append(end - start)
				print("Player " + str(self.turn) + " made a move in " + str(end - start))

				self.turn ^= 1
				self.totalMoves[self.turn] += 1

				if isinstance(self.players[self.turn], Player):
					self.playerStartTime = time.time()

				if self.turn == 0:
					print("Jaguar's turn")
				else:
					print("Dogs' turn")

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

							print("Player " + str(self.turn) + " made a move in " + str(end - self.playerStartTime))

							self.turn ^= 1
							self.totalMoves[self.turn] += 1

							if isinstance(self.players[self.turn], Player):
								self.playerStartTime = time.time()

							if self.turn == 0:
								print("Jaguar's turn")
							else:
								print("Dogs' turn")



		return "game", self.players[0], self.players[1]