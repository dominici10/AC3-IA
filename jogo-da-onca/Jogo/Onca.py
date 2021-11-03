class Onca:

	def __init__(self):
		import constants, copy
		self.adjacencyList = copy.deepcopy(constants.ADJACENCY_LIST)

	def isValid(self, grid, cell):
		i, j = cell
		if i == None or j == None:
			return False
		return grid[i][j] == 'j'

	def makeMove(self, grid, selected, cell):

		from Utilities import Utilities

		node = Utilities.cellToNode(grid, selected)
		nextNode = Utilities.cellToNode(grid, cell)

		if nextNode in self.adjacencyList[node] and grid[cell[0]][cell[1]] is None:
			grid[selected[0]][selected[1]], grid[cell[0]][cell[1]] = grid[cell[0]][cell[1]], grid[selected[0]][selected[1]]
			return 0

		if nextNode:

			dr = Utilities.sign(selected[0] - cell[0])
			dc = Utilities.sign(selected[1] - cell[1])

			intermediateCell = (cell[0] + dr, cell[1] + dc)
			intermediateNode = Utilities.cellToNode(grid, intermediateCell)

			i1, j1 = selected
			i2, j2 = intermediateCell
			i3, j3 = cell

			if grid[i2][j2] == 'd' and grid[i3][j3] is None and intermediateNode in self.adjacencyList[node] and nextNode in self.adjacencyList[intermediateNode]:
				grid[i1][j1], grid[i3][j3] = grid[i3][j3], grid[i1][j1]
				grid[i2][j2] = None

			return 1

		return 0

	def genJumps(self, grid, cell):

		from Utilities import Utilities
		from Estado import Estado
		import copy

		i, j = cell

		jumps = []
		node = Utilities.cellToNode(grid, cell)

		di = [-2, -2, -2, 0, 0, 2, 2, 2]
		dj = [-2, 0, 2, -2, 2, -2, 0, 2]

		for dir in range(len(di)):
			newi = i + di[dir]
			newj = j + dj[dir]

			if Utilities.inGrid(grid, (newi, newj)):
				if grid[newi][newj] is None:
					inti = i + Utilities.sign(di[dir])
					intj = j + Utilities.sign(dj[dir])

					if grid[inti][intj] == 'd':
						newNode = Utilities.cellToNode(grid, (newi, newj))
						intNode = Utilities.cellToNode(grid, (inti, intj))

						if newNode in self.adjacencyList[intNode] and intNode in self.adjacencyList[node]:
							newGrid = copy.deepcopy(grid)
							newGrid[i][j], newGrid[newi][newj] = newGrid[newi][newj], newGrid[i][j]
							newGrid[inti][intj] = None
							jumps.append([Estado(newGrid, (i, j), (newi, newj))])

		return jumps

	def genAdjMoves(self, grid, cell):

		from Utilities import Utilities
		from Estado import Estado
		import copy
		# print(cell)
		i, j = cell

		node = Utilities.cellToNode(grid, (i, j))

		states = []
		for nextNode in self.adjacencyList[node]:
			k, l = Utilities.nodeToCell(grid, nextNode)
			if grid[k][l] == None:
				newGrid = copy.deepcopy(grid)
				newGrid[i][j], newGrid[k][l] = newGrid[k][l], newGrid[i][j]
				states.append([Estado(newGrid, (i, j), (k, l))])

		return states

	
	def genMoves(self, grid):

		for i in range(len(grid)):
			for j in range(len(grid[0])):
				if self.isValid(grid, (i, j)):
					onca = (i, j)

		i, j = onca

		from Utilities import Utilities
		from Estado import Estado
		import copy

		node = Utilities.cellToNode(grid, (i, j))

		states = self.genAdjMoves(grid, onca)
		toRelax = self.genJumps(grid, onca)

		while len(toRelax):
			lStates = toRelax.pop()
			state = lStates[-1]

			cell = state.getTo()
			grid = copy.deepcopy(state.getGrid())
			for adj in self.genAdjMoves(grid, cell):
				states.append(lStates + adj)

			for jump in self.genJumps(grid, cell):
				toRelax.append(lStates + jump)

		return states