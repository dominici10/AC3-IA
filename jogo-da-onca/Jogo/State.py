'''
Defines a state in the minimax and alpha-beta algorithms.
It is represented by the grid and the series of moves made.
'''
class State:

	def __init__(self, grid, frm, to):

		import copy

		self.grid = copy.deepcopy(grid)
		self.frm = frm
		self.to = to

	def __str__(self): # for debugging
		ans = ""
		for i in range(len(self.grid)):
			ans += str(self.grid[i]) + "\n"
		ans += str(self.frm) + "\n"
		ans += str(self.to) + "\n"
		ans += "\n"
		return ans

	def getTo(self):
		return self.to

	def getGrid(self):
		return self.grid

	def getFrom(self):
		return self.frm