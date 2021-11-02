'''
Class created for building the homescreen which is made of multiple buttons.
Each button should have a size, text and background color in case the user checks the option.
'''
class Button:

	def __init__(self, screen, bottomUp, text, outline = True):

		import constants, pygame

		self.screen = screen
		self.bottomUp = bottomUp
		self.text = text
		self.font = "arial"
		self.fontDimension = 16
		self.height = constants.BUTTON_HEIGHT
		self.width = constants.BUTTON_WIDTH
		self.rectangle = pygame.Rect(self.bottomUp[0], self.bottomUp[1], self.height, self.width)
		self.renderedText = pygame.font.SysFont(self.font, self.fontDimension).render(self.text, True, constants.BLACK)
		self.textRectangle = self.renderedText.get_rect(center = self.rectangle.center)
		self.outline = outline
		self.color = constants.WHITE


	def getBottomUp(self):
		return self.bottomUp

	def getText(self):
		return self.text

	def setText(self, text):

		import constants, pygame

		self.text = text
		self.renderedText = pygame.font.SysFont(self.font, self.fontDimension).render(self.text, True, constants.BLACK)
		self.textRectangle = self.renderedText.get_rect(center = self.rectangle.center)

	def pressed(self, clickCoords):
		x, y = clickCoords
		return self.bottomUp[0] <= x <= self.bottomUp[0] + self.height and self.bottomUp[1] <= y <= self.bottomUp[1] + self.width

	def setColor(self, color):
		self.color = color

	def getColor(self):
		return self.color

	def draw(self): # draw the button

		import pygame, constants

		if self.outline:
			pygame.draw.rect(self.screen, constants.BLACK, self.rectangle)
			overRect = pygame.Rect(self.bottomUp[0] + 2, self.bottomUp[1] + 2, self.height - 4, self.width - 4)
			pygame.draw.rect(self.screen, self.color, overRect)
		else:
			pygame.draw.rect(self.screen, self.color, self.rectangle)
		self.screen.blit(self.renderedText, self.textRectangle)