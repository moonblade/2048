from board import Board
from move import Move
import curses
class Game():
	def __init__(self):
		self.screen = curses.initscr()
		# curses.noecho()
		# curses.cbreak()
		self.screen.keypad(True)
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
		char = self.screen.getch()
		if char == ord('q'):
			return True
		elif char == curses.KEY_RIGHT:
			self.makeMove(Move.RIGHT)
		elif char == curses.KEY_LEFT:
			self.makeMove(Move.LEFT)
		elif char == curses.KEY_UP:
			self.makeMove(Move.UP)
		elif char == curses.KEY_DOWN:
			self.makeMove(Move.DOWN)

	def print(self):
		self.board.print()

	def isGameOver(self):
		return False

	def __del__(self):
		curses.nocbreak(); 
		self.screen.keypad(0); 
		curses.echo()
		curses.endwin()
		
if __name__ == '__main__':
	g = Game()
	while not g.isGameOver():
		if(g.move()):
			break
	