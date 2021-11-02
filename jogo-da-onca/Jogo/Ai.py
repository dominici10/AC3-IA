class Ai:

	def __init__(self, piece, algorithm, difficulty = "easy", heuristic = 1):

		self.turns = 0
		self.piece = piece
		self.algorithm = algorithm
		self.difficulty = difficulty
		self.heuristic = heuristic - 1

		self.eval = [self.eval1, self.eval2]

		self.generatedNodes = 0


	def selectPiece(self, grid, cell):
		return self.piece.isValid(grid, cell)

	
	def makeMove(self, grid):

		self.generatedNodes = 0

		from State import State

		# set the depth of the game tree
		if self.difficulty == "easy":
			depth = 3
		

		if self.algorithm == "IA":
			state, score = self.minimax(State(grid, None, None), self.piece, depth, max)

		return state, score, self.generatedNodes

	def minimax(self, state, piece, depth, f): # minimax algorithm

		self.generatedNodes += 1

		if depth == 0:
			return state, self.eval[self.heuristic](state, piece, f)

		nextStates = piece.genMoves(state.getGrid())

		from Jaguar import Jaguar
		from Dog import Dog
		import copy

		nextPiece = Jaguar() if isinstance(piece, Dog) else Dog()
		bestScore, nextF = (float('-inf'), min) if f == max else (float('inf'), max)
		bestState = None

		for nextState in nextStates:

			_, aux = self.minimax(nextState[-1], nextPiece, depth - 1, nextF)
			a = f(aux, bestScore)

			if a != bestScore:
				bestScore = a
				bestState = copy.deepcopy(nextState)

		return bestState, bestScore

	def setDifficulty(self, difficulty):
		self.difficulty = difficulty

	def setHeuristic(self, heuristic):
		self.heuristic = heuristic - 1

	def getPieceType(self):

		from Dog import Dog
		from Jaguar import Jaguar

		if isinstance(self.piece, Dog):
			return "Cachorro"
		else:
			return "Onça"

	
	def eval1(self, state, piece, f): 

		grid = state.getGrid()

		dogsCnt = 0
		for i in range(len(grid)):
			for j in range(len(grid[0])):
				if grid[i][j] == 'd':
					dogsCnt += 1

		from Jaguar import Jaguar

		if isinstance(piece, Jaguar):
			if f == max:
				return 14 - dogsCnt
			else:
				return dogsCnt
		else:
			if f == max:
				return dogsCnt
			else:
				return 14 - dogsCnt


	
	def eval2(self, state, piece, f): # no of dogs around jaguar

		grid = state.getGrid()

		for i in range(len(grid)):
			for j in range(len(grid[0])):
				if grid[i][j] == 'j':
					jaguar = (i, j)

		from Utilities import Utilities

		node = Utilities.cellToNode(grid, jaguar)

		import constants

		dogsCnt = 0
		for nextNode in constants.ADJACENCY_LIST[node]:
			nextCell = Utilities.nodeToCell(grid, nextNode)

			i, j = nextCell
			if grid[i][j] == 'd':
				dogsCnt += 1

		from Jaguar import Jaguar

		if isinstance(piece, Jaguar):
			if f == max:
				return len(constants.ADJACENCY_LIST[node]) - dogsCnt
			else:
				return dogsCnt
		else:
			if f == max:
				return dogsCnt
			else:
				return len(constants.ADJACENCY_LIST[node]) - dogsCnt