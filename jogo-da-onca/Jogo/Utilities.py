class Utilities:

	@staticmethod
	def clickedOn(onScreenCoordinates, grid, cell, clickCoords):

		i, j = cell
		cellX, cellY = onScreenCoordinates[i][j]
		x, y = clickCoords

		import math, constants

		radius = math.sqrt((cellX - x) * (cellX - x) + (cellY - y) * (cellY - y))
		radius = round(radius, 5)

		if grid[i][j] is None:
			if radius <= constants.SQUARE_SIDE_WIDTH:
				return True
			return False
		elif radius <= constants.CIRCLE_RADIUS:
			return True
		return False

	@staticmethod
	def clickCoordsToCell(onScreenCoordinates, grid, clickCoords):
		row, col = None, None
		for i in range(len(grid)):
			for j in range(len(grid[0])):
				if Utilities.clickedOn(onScreenCoordinates, grid, (i, j), clickCoords):
					row = i
					col = j
					break
		return row, col

	@staticmethod
	def cellToNode(grid, cell):
		i, j = cell
		return i * len(grid[0]) + j

	@staticmethod
	def nodeToCell(grid, node):
		i = node // len(grid[0])
		j = node % len(grid[0])

		return (i, j)

	@staticmethod
	def sign(x):
		if x == 0:
			return 0
		if x < 0:
			return -1
		return 1

	@staticmethod
	def endGame(grid):

		cntDogs = 0
		for i in range(len(grid)):
			for j in range(len(grid[0])):
				if grid[i][j] == 'd':
					cntDogs += 1
				elif grid[i][j] == 'j':
					cougarPos = (i, j)

		if cntDogs < 10:
			return "Vitória Onça"

		import constants

		blockCnt = 0
		for nextNode in constants.ADJACENCY_LIST[Utilities.cellToNode(grid, cougarPos)]:
			i, j = Utilities.nodeToCell(grid, nextNode)
			if grid[i][j] == 'd':
				blockCnt += 1

		if blockCnt == len(constants.ADJACENCY_LIST[Utilities.cellToNode(grid, cougarPos)]):
			return "Vitória Cachorro"

		return None

	@staticmethod
	def inGrid(grid, cell):
		i, j = cell
		return 0 <= i < len(grid) and 0 <= j < len(grid[0])
