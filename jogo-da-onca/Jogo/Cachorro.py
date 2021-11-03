class Cachorro:

	def __init__(self):
		import constants, copy
		self.adjacencyList = copy.deepcopy(constants.ADJACENCY_LIST)

	def isValid(self, grid, cell):
		i, j = cell
		if i == None or j == None:
			return False
		return grid[i][j] == 'd'

	def makeMove(self, grid, selected, cell): # check if move is valid

		from Utilities import Utilities

		node = Utilities.cellToNode(grid, selected)
		nextNode = Utilities.cellToNode(grid, cell)

		if nextNode in self.adjacencyList[node] and grid[cell[0]][cell[1]] is None:
			grid[selected[0]][selected[1]], grid[cell[0]][cell[1]] = grid[cell[0]][cell[1]], grid[selected[0]][selected[1]]
			return 0

		return 1

	
	def genMoves(self, grid):

		from Utilities import Utilities
		from Estado import Estado
		import copy

		states = []

		for i in range(len(grid)):
			for j in range(len(grid[0])):
				if self.isValid(grid, (i, j)):
					node = Utilities.cellToNode(grid, (i, j))

					for nextNode in self.adjacencyList[node]:
						k, l = Utilities.nodeToCell(grid, nextNode)
						if grid[k][l] == None:
							newGrid = copy.deepcopy(grid)
							newGrid[i][j], newGrid[k][l] = newGrid[k][l], newGrid[i][j]
							states.append([Estado(newGrid, (i, j), (k, l))])

		return states