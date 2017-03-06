#from Grid_3 import getAvailableCells 
import math
import time





def getChildGrids(grid, availableMoves):

	#The child grids and the corresponding move that led to it in lists[]
	grids = []
	moves = []

	for aMove in availableMoves:

		gridCopy = grid.clone()

		#Returns True if properly moved & effects the grid itself (shallow)
		wasMoved = gridCopy.move(aMove)

		grids.append(gridCopy)

		moves.append(aMove)


	return grids, moves






def heuristicMerges(grid):
	"""Count the number of merges: how many more available cells."""
	availableCells = grid.getAvailableCells()

	numOfAvailableCells = len(availableCells)

	return numOfAvailableCells


def heuristicGradientValues(grid):
	"""Assign weights to the top left 2x2. """


	maxValue = grid.getMaxTile() 


	gradientScore = 0

	#gradientScore = (grid.map[0][0] * 4) + (grid.map[1][0] * 2) + (grid.map[0][1] * 2) + (grid.map[1][1] * 1)
	if grid.map[0][0] == maxValue:
		gradientScore +=10
	if grid.map[0][0] in [0,2,4,8] or grid.map[3][0] in [0,2,4,8] or grid.map[0][3] in [0,2,4,8] or grid.map[3][3] in [0,2,4,8]:
		gradientScore -=5

	#print(gradientScore)
	return gradientScore



	# #Check if largest tile is in a edge-edge corner
	# if(grid.map[0][0] == maxValue or grid.map[3][0] == maxValue or 
	# 	grid.map[0][3] == maxValue or grid.map[3][3] == maxValue):

	# 	gradientScore += 30
	
	# #Decrease score if a sub-max tile is in a corner
	# if( (grid.map[0][0] != 0 and grid.map[0][0]!= maxValue) or
	# 	(grid.map[3][0] != 0 and grid.map[3][0]!= maxValue) or
	# 	(grid.map[0][3] != 0 and grid.map[0][3]!= maxValue) or
	# 	(grid.map[3][3] != 0 and grid.map[3][3]!= maxValue)):

	# 	gradientScore -= 5


	#return gradientScore









def heuristicClusterLikeTiles(grid):
	"""Incentivize clustering titles of similar value. 
	Tiles differ by a factor of 2.

	Sweep over the board adding value for tiles adjacent to like-valued tiles.
	Return a total score of how clustered they are.

	"""

	clusterScore = 0

	#Iterate over every tile. Only check right and down adjacent tiles. Anything more is unneccesary.
	for i in range(0, len(grid.map)):
		for j in range(0, len(grid.map)):

			if i+1 < len(grid.map):
				if grid.map[i][j] !=0:
					if grid.map[i][j] * 2 == grid.map[i+1][j] or grid.map[i][j] / 2 == grid.map[i+1][j]:
						clusterScore += 2

			if j+1 < len(grid.map):
				if grid.map[i][j] !=0:
					if grid.map[i][j] * 2 == grid.map[i][j+1] or grid.map[i][j] / 2 == grid.map[i][j+1]:
						clusterScore += 2



			#Does this potentially help? To also take into account diagonal tiles?

	return clusterScore






def higherNumberedTiles(grid):

	totalTileValue = 0

	for i in range(0,len(grid.map)):
		for j in range(0, len(grid.map)):

			totalTileValue += grid.map[i][j]


	availableCells = grid.getAvailableCells()
	numAvailableCells = len(availableCells)
	totalCells = 16
	fullCells = totalCells - numAvailableCells

	print(totalTileValue / fullCells)
	return totalTileValue / fullCells




	





def totalHeuristic(grid):
	# print("mergesVal: "+str(heuristicMerges(grid)*4) + "\n" +
	# "gradientVal: " + str(heuristicGradientValues(grid)) + "\n" +
	# "maxTileVal: " + str(math.log(grid.getMaxTile())*4) + "\n" +
	# "clusterVal: " + str(heuristicClusterLikeTiles(grid))+"\n"
	# )

	"""Cluster like tiles seems to perform poorly"""

	# print("Total hVal: " + heuristicMerges(grid)*4
	# + heuristicGradientValues(grid)
	# + math.log(grid.getMaxTile())
	# + heuristicClusterLikeTiles(grid))

	# maxValue = grid.getMaxTile() 

	# if(grid.map[0][0] == maxValue):
	# 	maxValue = 100

	# return maxValue


	#return heuristicMerges(grid)*4 + heuristicGradientValues(grid) + math.log(grid.getMaxTile())*4 + heuristicClusterLikeTiles(grid)
	#return heuristicMerges(grid)
	#return grid.getMaxTile()
	#return higherNumberedTiles(grid)

	print("heuristicMerges: ",heuristicMerges(grid), ". heuristicGradientValues: ",heuristicGradientValues(grid))
	return heuristicMerges(grid) + heuristicGradientValues(grid)




	

#def minimax(grid, timeLimit, maxPlayerTurn):

def minimax(currentGrid, depth, maxPlayerTurn):
	'''
	Return: value(int) for a given child. Indicating success value by looking 
	into the "future" outcomes of moves.
	'''

	#if depth = 0 or node is a terminal node: return heuristic value of node?
	#print("in minimax: ", currentGrid)
	#print("IN MINIMAX: type of current grid:   ", type(currentGrid))

	print(currentGrid.map, " At depth: ", depth)
	print()

	if depth == 0:
		#return heuristic1(currentGrid) + heuristic2(currentGrid)*3
		return totalHeuristic(currentGrid)

	availableMoves = currentGrid.getAvailableMoves()

	if maxPlayerTurn:
		bestValue = -math.inf

		[childGrids, movesTochildGrids] = getChildGrids(currentGrid, availableMoves)

		for child in childGrids:
			#print("in first recurse: ", child)

			value = minimax(child, depth - 1, False)
			bestValue = max(value, bestValue)

		return bestValue

	else:

		bestValue = math.inf

		[childGrids, movesTochildGrids] = getChildGrids(currentGrid, availableMoves)

		for child in childGrids:
			value = minimax(child, depth - 1, True)
			bestValue = min(value, bestValue)

		return bestValue

def minimax2(currentGrid, maxPlayerTurn, startTime):
	'''
	Return: value(int) for a given child. Indicating success value by looking 
	into the "future" outcomes of moves.
	'''

	#if depth = 0 or node is a terminal node: return heuristic value of node?
	#print("in minimax: ", currentGrid)
	#print("IN MINIMAX: type of current grid:   ", type(currentGrid))
	if time.clock() - startTime > 0.2 or len(currentGrid.getAvailableMoves()) == 0:
		return heuristic1(currentGrid) + heuristic2(currentGrid)*3

	availableMoves = currentGrid.getAvailableMoves()

	if maxPlayerTurn:
		bestValue = -math.inf

		[childGrids, movesTochildGrids] = getChildGrids(currentGrid, availableMoves)

		for child in childGrids:
			#print("in first recurse: ", child)

			value = minimax2(child, False, startTime)
			bestValue = max(value, bestValue)

		return bestValue

	else:

		bestValue = math.inf

		[childGrids, movesTochildGrids] = getChildGrids(currentGrid, availableMoves)

		for child in childGrids:
			value = minimax2(child, True, startTime)
			bestValue = min(value, bestValue)

		return bestValue






def alphaBetaIDA(currentGrid, timeLimit):
	
	#This whole IDS is taking place to determine 1 overarching move. 
	# So the time limit keeps ticking (no reset) for all iterations of IDS
	startTime = time.clock()
	maxPlayerTurn = True
	alpha = -math.inf
	beta = math.inf
	maxDepth = 4
	maxScore = 0


	#Treating timeLimit as 0.2 here but as 0.15 in alphabeta???????
	while(time.clock() - startTime < timeLimit): 
	
		#print(maxDepth)
		scoreAtThisDepth = alphaBeta(currentGrid, alpha, beta, maxPlayerTurn, maxDepth, startTime)
		maxDepth += 1


		#The score could increase or decrease with more depth?
		#Return the highest value from all depth levels of this given child
		if scoreAtThisDepth > maxScore:
			maxScore = scoreAtThisDepth

	return maxScore
	#return alphaBeta(currentGrid, alpha, beta, maxPlayerTurn, maxDepth, startTime)


	#change order of move u look at so go to corner


def alphaBeta(currentGrid, alpha, beta, maxPlayerTurn, depth, startTime):

	#print("time: ",time.clock() - startTime)
	#print("depth = ", depth)
	#print(depth)
	if time.clock() - startTime > 0.15 or len(currentGrid.getAvailableMoves()) == 0:

		#print("HAPPENEDDGSDGDFHDFGHDFGHDFGHDFGHDFGHDFGHDFHDFGH", time.clock() - startTime)
		if maxPlayerTurn:
			return alpha
		else:
			return beta

	if depth == 0:
		
		#print("helllllloooooo")
		return totalHeuristic(currentGrid)


	availableMoves = currentGrid.getAvailableMoves()

	if maxPlayerTurn:

		[childGrids, movesTochildGrids] = getChildGrids(currentGrid, availableMoves)

		for child in childGrids:

			alpha = max(alpha, alphaBeta(child, alpha, beta, False, depth - 1, startTime ))


			if beta <= alpha:
				break #Beta cut off

		return alpha


	else:

		[childGrids, movesTochildGrids] = getChildGrids(currentGrid, availableMoves)

		for child in childGrids:
			#print("df---------------------------------------------------------")
			#print(beta)
			beta = min(beta, alphaBeta(child, alpha, beta, True, depth - 1, startTime))

			if beta <= alpha:
				break #Alpha cut off

		return beta











#def runAlphaBeta(currentGrid, alpha, beta, maxPlayerTurn, startTime):
	
# 	global start
# 	start = startTime
# 	maxDepth = 3

# 	return alphaBeta(currentGrid, alpha, beta, maxPlayerTurn, maxDepth)







# def alphaBeta(currentGrid, alpha, beta, maxPlayerTurn, depth):
# #def alphaBeta(currentGrid, alpha, beta, maxPlayerTurn, startTime, depth):
# 	'''
# 	Return: value(int) for a given child. Indicating success value by looking 
# 	into the "future" outcomes of moves.
# 	'''

# 	#p = depth + 1

# 	print("INFO: depth: ",depth, ". MaxTurn: ", maxPlayerTurn, ". Board: ", currentGrid.map )


# 	#print(currentGrid.map)
# 	#print("depth: ", depth)


# 	if time.clock() - startTime > 0.15 or len(currentGrid.getAvailableMoves()) == 0:

# 		return totalHeuristic(currentGrid)


# 	availableMoves = currentGrid.getAvailableMoves()

# 	if maxPlayerTurn:

# 		[childGrids, movesTochildGrids] = getChildGrids(currentGrid, availableMoves)

# 		for child in childGrids:
# 			#alpha = max(alpha, alphaBeta(child, alpha, beta, False, startTime, depth+1))
# 			#alpha = max(alpha, alphaBeta(child, alpha, beta, False))
# 			#alpha = max(alpha, alphaBeta(child, alpha, beta, False,p))
# 			alpha = max(alpha, alphaBeta(child, alpha, beta, False,depth-1))


# 			if beta <= alpha:
# 				break #Beta cut off

# 		return alpha

# 	else:

# 		[childGrids, movesTochildGrids] = getChildGrids(currentGrid, availableMoves)

# 		for child in childGrids:
# 			#beta = min(beta, alphaBeta(child, alpha, beta, True, startTime, depth+1))
# 			#beta = min(beta, alphaBeta(child, alpha, beta, True,p))
# 			beta = min(beta, alphaBeta(child, alpha, beta, True, depth -1))

# 			if beta <= alpha:
# 				break #Alpha cut off

# 		return beta



















































