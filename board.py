#!/usr/bin/env python3
import random
from partialFormatter import fmt
class Board():
	# size - size of side of square board
	# board - dictionary of cell -> value pairs
	# fourProbability - probability of a 4 showing up instead of 2
	def __init__(self, size=4, fourProbability=0.1):
		self.size = size
		self.board = dict((value,None) for value in [(x,y) for x in range(self.size) for y in range(self.size)])
		self.fourProbability=fourProbability

	def getEmptyCells(self):
		return [x for x in self.board if self.board[x] == None]

	def getEmptyCell(self):
		if (len(self.getEmptyCells())==0):
			return None
		return random.choice(self.getEmptyCells())

	def addData(self, cell, number):
		if cell is None or self.board[cell] is not None:
			return False
		else:
			self.board[cell] = number
			return True

	# return 2 or 4 based on probability
	def getRandomData(self):
		num = random.randint(1, 100)
		if(num <= self.fourProbability*100):
			return 4;
		else:
			return 2;

	def addRandomData(self):
		self.addData(self.getEmptyCell(),self.getRandomData())

	def print(self):
		for x in range(self.size):
			print(''.join([fmt.format('{0:<10}', self.board[key]) for key in self.board if key[0]==x]))

b = Board(3)
# print(b.size)
# print(b.board)
# print(b.getEmptyCell())

b.addRandomData();
b.addRandomData();
b.addRandomData();
b.addRandomData();
b.addRandomData();
b.print()