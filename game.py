from board import Board
from move import Move
import getch
class Game():
	def __init__(self):
		self.board = Board()
		self.score = 0

	def makeMove(self, move):
		score, valid=self.board.move(move)
		if (valid):
			self.score+=score
			self.board.addRandomData()
			self.print()
			print(self.score)

	def move(self):
		char = getch.getch()
		if char == 'q':
			return True
		elif char == 'd':
			self.makeMove(Move.RIGHT)
		elif char == 'a':
			self.makeMove(Move.LEFT)
		elif char == 'w':
			self.makeMove(Move.UP)
		elif char == 's':
			self.makeMove(Move.DOWN)

	def print(self):
		self.board.print()

	def isGameOver(self):
		return self.board.noMoreMoves()

if __name__ == '__main__':
	g = Game()
	g.print()
	while not g.isGameOver():
		if(g.move()):
			break
