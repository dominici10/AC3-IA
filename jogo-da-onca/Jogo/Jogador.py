class Jogador:

	def __init__(self, piece):

		self.turns = 0
		self.piece = piece

	def selectPiece(self, grid, cell):
		return self.piece.isValid(grid, cell)

	def makeMove(self, grid, selected, cell):
		return self.piece.makeMove(grid, selected, cell)

	def getPieceType(self):

		from Cachorro import Cachorro
		from Onca import Onca

		if isinstance(self.piece, Cachorro):
			return "cachorro"
		return "onça"