from random import randint
from BaseAI_3 import BaseAI
from Helper import * 
import math
import time


class PlayerAI(BaseAI):

	def getMove(self, grid):
		"""
		returns an integer indicating the player's action.
		0:"Up", 1:"Down", 2:"Left", 3:"Right"
		"""
		#Start the clock to ensure a move does not exceed 0.2 seconds
		start = time.clock()

		highestValueMove = 0
		bestMove = None
		bestGrid = None

		moves = grid.getAvailableMoves()
		#print(type(grid))
		[childGrids, movesTochildGrids] = getChildGrids(grid, moves)




		for i in range(0,len(childGrids)):

			childGrid = childGrids[i]
			move = movesTochildGrids[i]

			#minimax will return a best achievable "Max" value for each child
			#value = Helper.minimax(childGrid, 0.2, True)
			#print("childGrid", childGrid)

			#value = minimax(childGrid, 4, True)
			#value = minimax2(childGrid, True,start)

			#value = alphaBeta(childGrid, -math.inf, math.inf, True, 3)
			#value = runAlphaBeta(childGrid, -math.inf, math.inf, True, start)


			"""
			Here we call alphabetaIDA on each immediate child node of the given
			 board. abIDA will return an overall "value" for each child based
			 on the heuristic. 
			Inside the function abIDA itself, we run alphabeta with a given time
			 limit (0.02). It will run using iterative deepening to not go too
			 deep down a single branch. Start at maxDepth 3 and increase from here.
			"""

			#childValue = alphaBetaIDA(childGrid, 0.2)
			startTime = time.clock()
			maxPlayerTurn = True
			alpha = -math.inf
			beta = math.inf
			maxDepth = 4
			maxScore = 0
			childValue = alphaBeta(childGrid, alpha, beta, maxPlayerTurn, maxDepth, startTime)





			if childValue > highestValueMove:

				highestValueMove = childValue
				bestMove = move
				bestGrid = childGrid

		return bestMove


















		#print(moves)
		#return moves[randint(0, len(moves) - 1)] if moves else None






	#def minimax


	#def heuristic