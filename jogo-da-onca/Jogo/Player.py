'''
This class implementes the player logic
'''
class Player:

	def __init__(self, piece):

		self.turns = 0
		self.piece = piece

	def selectPiece(self, grid, cell):
		return self.piece.isValid(grid, cell)

	def makeMove(self, grid, selected, cell):
		return self.piece.makeMove(grid, selected, cell)

	def getPieceType(self):

		from Dog import Dog
		from Jaguar import Jaguar

		if isinstance(self.piece, Dog):
			return "dog"
		return "jaguar"