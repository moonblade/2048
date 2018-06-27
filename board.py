#!/usr/bin/env python3
import random
from partialFormatter import fmt
from itertools import count, groupby, starmap
# import numpy

class Board():
	# size - size of side of square board
	# board - dictionary of cell -> value pairs
	# fourProbability - probability of a 4 showing up instead of 2
	def __init__(self, size=4, fourProbability=0.1):
		self.base = 2
		self.size = size
		self.board = [[None for x in range(self.size)] for y in range(self.size)]
		# self.board = dict((value,None) for value in [(x,y) for x in range(self.size) for y in range(self.size)])
		self.fourProbability=fourProbability

	def getEmptyCells(self):
		return [(x,y) for x in range(self.size) for y in range(self.size) if self.board[x][y] == None]

	def getEmptyCell(self):
		if (len(self.getEmptyCells())==0):
			return None
		return random.choice(self.getEmptyCells())

	def changeData(self, cell, number):
		if cell is None:
			return False
		else:
			self.board[cell[0]][cell[1]] = number
			return True

	# return 2 or 4 based on probability
	def getRandomData(self):
		chance = random.uniform(0, 1)
		if(chance <= self.fourProbability):
			return 4;
		else:
			return 2;

	def addRandomData(self):
		self.changeData(self.getEmptyCell(), self.getRandomData())

	def print(self):
		for x in range(self.size):
			print(''.join([fmt.format('{0:<10}', self.board[x][y]) for y in range(self.size)]))
		print()

	def flip(self):
		self.board = [self.board[x][::-1] for x in range(self.size)]

	def transpose(self):
		self.board = [[self.board[y][x] for y in range(self.size)] for x in range(self.size)]

	def moveDown(self):
		self.transpose()
		score = self.moveRight()
		self.transpose()
		return score
		
	def moveUp(self):
		self.transpose()
		score = self.moveLeft()
		self.transpose()
		return score

	def moveRight(self):
		self.flip()
		score = self.moveLeft()
		self.flip()
		return score

	def moveLeft(self):
		score = 0
		for rowIndex in range(self.size):
			row = self.board[rowIndex]
			r = []
			for n,x in starmap(lambda n, a: (n, sum(map(bool,a))), groupby(filter(bool, row))):
				r += ([n*self.base] * (x//self.base)) + ([n] * (x%self.base))
				score += n*self.base*(x//self.base)
			self.board[rowIndex] = r + ([None] * (self.size - len(r)))
		self.addRandomData()
		return score

b = Board(4)
b.addRandomData();

b.addRandomData();
b.addRandomData();
b.addRandomData();
b.addRandomData();
b.addRandomData();
b.addRandomData();
b.addRandomData();
b.addRandomData();
b.addRandomData();
b.addRandomData();
b.print()
b.flip()
print(b.moveLeft())
b.print()
print(b.moveRight())
b.print()
print(b.moveRight())
b.print()
print(b.moveUp())
b.print()
print(b.moveDown())
b.print()