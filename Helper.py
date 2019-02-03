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
	#subtract difference between neighbors






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

	#square




	
















"""Proper heuristics"""

def heuristicMerges(grid):
	"""Count the number of merges: how many more available cells."""
	availableCells = grid.getAvailableCells()

	numOfAvailableCells = len(availableCells)
	#print("numAvailableCells = ", numOfAvailableCells)

	return numOfAvailableCells


def availableCells(grid):
	availableCells = grid.getAvailableCells()

	numOfAvailableCells = len(availableCells)

	return numOfAvailableCells




def sqrDiffOfTiles(grid):
	"""Sums the squared differences between adjacent tiles-- In an effort to
	 penalize placing very different tiles next to one another.
	 This will be subtracted from the total heuristic score.
	 """
	
	totalDifference = 0

	#Note: only need to check Right/Down so as not to double count comparisons
	for i in range(0,len(grid.map)):
		for j in range(0, len(grid.map)):

			#Compare Right & dont compare an edgeTile past the edge
			if(i < len(grid.map) - 1):

				rightDifference = abs(grid.map[i][j] - grid.map[i+1][j])

				totalDifference += (rightDifference * rightDifference)

			#Compare Down & dont compare an edgeTile past the edge
			if(j < len(grid.map) - 1):
				
				downDifference = abs(grid.map[i][j] - grid.map[i][j+1])
				
				totalDifference += (downDifference * downDifference)

	return totalDifference


def differenceOfTiles(grid):
	"""Sums the squared differences between adjacent tiles-- In an effort to
	 penalize placing very different tiles next to one another.
	 This will be subtracted from the total heuristic score.
	 """
	
	totalDifference = 0
	twosPenality = 10

	#Note: only need to check Right/Down so as not to double count comparisons
	for i in range(0,len(grid.map)):
		for j in range(0, len(grid.map)):
			#Compare Right & dont compare an edgeTile past the edge
			if(i < len(grid.map) - 1):
				totalDifference += abs(grid.map[i][j] - grid.map[i+1][j])
			#Compare Down & dont compare an edgeTile past the edge
			if(j < len(grid.map) - 1):
				totalDifference += abs(grid.map[i][j] - grid.map[i][j+1])


			if(i > 0):
				totalDifference += abs(grid.map[i][j] - grid.map[i-1][j])
			if(j > 0):
				totalDifference += abs(grid.map[i][j] - grid.map[i][j-1])






			#Penalize 2's
			#if grid.map[i][j] == 2 :

			#	twosPenality *= 100 






	return totalDifference #+ twosPenality



def squaresOfValues(grid):
	""" Sum the square of each tile value-- In an effort to 
	 value higher tiles over smaller ones, both resulting from merges.
	 This will be ADDED from the total heuristic score.
	 """
	sumOfSquares = 0

	for i in range(0,len(grid.map)):
		for j in range(0, len(grid.map)):

			tileValue = grid.map[i][j]

			sumOfSquares += (tileValue * tileValue)


	return sumOfSquares


	

def gradient(grid):
	"""Want to incentivize higher tiles in the corners and 
	lower ones in the center. NOTE: Differences sort of acheives this, 
	by placing very high tiles in the corner, they dont subtract from as many.


	#Ideally, penalize having lower values higher on in the game. Maybe compare
	using the max tile? Like we know if we have 1024 on the board, a 2 in
	a corner is REALLY bad, but if max is 128 its not a big deal.
	"""
	
	gradientScore = 0

	#Right now focus on the top-left corner.



	# maxValue = grid.getMaxTile() 

	# if grid.map[0][0] == maxValue:
	# 	gradientScore += maxValue*maxValue

	# elif grid.map[0][0] in [2,4,8,16,32]:

	# 	gradientScore -= (1 / (grid.map[0][0]/10))**2


	gradientMatrix = [
	[15,10,5,4],
	[10,9,4,3],
	[5,4,3,2],
	[4,3,2,1]]

	#gradientMatrix = [[7,6,5,4],[6,5,4,3],[5,4,3,2],[4,3,2,1]]
	#gradientMatrix = [[0.135759,0.121925,0.102812,0.099937],[0.0997992,0.0888405,0.076711,0.0724143],[0.060654,0.0562579,0.037116,0.0161889],[0.0125498,0.00992495,0.00575871,0.00335193]]


	for i in range(0,len(grid.map)):
		for j in range(0, len(grid.map)):

			tileValue = grid.map[i][j]

			gradientScore += grid.map[i][j] * gradientMatrix[i][j]



	maxValue = grid.getMaxTile()

	# if grid.map[0][0] == maxValue:
	# 	gradientScore *= 1.2

	return gradientScore



#def mono():

def newGradient(grid):

	thesum = 0

	thesum += (grid.map[3][0]*grid.map[3][0])**2
	thesum += grid.map[2][0]*grid.map[2][0]** 1.5
	thesum += grid.map[1][0]*grid.map[1][0] ** 1.3
	thesum += grid.map[0][0]*grid.map[0][0] ** 1.2



	return thesum







# def potentialMerges(grid):

# 	numPotentialMerges = 0

# 	for i in range(0,len(grid.map)):
# 		for j in range(0, len(grid.map)):

# 			if(i < len(grid.map) - 1):

# 				if grid.map[i][j] == grid.map[i+1][j]:
# 					numPotentialMerges += 1

# 			if(j < len(grid.map) - 1):

# 				if grid.map[i][j] == grid.map[i][j+1]:
# 					numPotentialMerges += 1

# 	return numPotentialMerges







def potentialMerges(grid):

	numPotentialMerges = 0

	for i in range(0,len(grid.map)):
		for j in range(0, len(grid.map)):

			if(i < len(grid.map) - 1):

				if grid.map[i][j] == grid.map[i+1][j]:
					numPotentialMerges += grid.map[i][j]

			if(j < len(grid.map) - 1):

				if grid.map[i][j] == grid.map[i][j+1]:
					numPotentialMerges += grid.map[i][j]

			if(i > 0):

				if grid.map[i][j] == grid.map[i-1][j]:
					numPotentialMerges += grid.map[i][j]

			if(j > 0):

				if grid.map[i][j] == grid.map[i][j-1]:
					numPotentialMerges += grid.map[i][j]



	return numPotentialMerges





#Check off: Squarevalues, 





def monotinicity(grid):


	monoScore = 0

	for i in range(0,len(grid.map)):

		x1 = grid.map[0][i]
		x2 = grid.map[1][i]
		x3 = grid.map[2][i]
		x4 = grid.map[3][i]


		if (x1 <= x2 <= x3 <= x4) or (x1 >= x2 >= x3 >= x4):
			monoScore += min(x1,x2,x3,x4)



		y1 = grid.map[i][0]
		y2 = grid.map[i][1]
		y3 = grid.map[i][2]
		y4 = grid.map[i][3]


		if (y1 <= y2 <= y3 <= y4) or (y1 >= y2 >= y3 >= y4):
			monoScore += min(y1,y2,y3,y4)

	return monoScore















def totalHeuristic(grid):


	#return squaresOfValues(grid) + potentialMerges(grid)*100 + math.sqrt(differenceOfTiles(grid)) +monotinicity(grid)*10


	#Rightmost depth 4
	#return heuristicMerges(grid)*4 + squaresOfValues(grid) - math.sqrt(differenceOfTiles(grid)) + monotinicity(grid)*10

	#Leftmost (depth 4)
	return heuristicMerges(grid) + gradient(grid) + potentialMerges(grid) + squaresOfValues(grid) - math.sqrt(differenceOfTiles(grid))

	# middle(depth 3)
	#return heuristicMerges(grid)*4 + squaresOfValues(grid) - math.sqrt(differenceOfTiles(grid))



	#avg square
	#square of square of bottom right

	#avgOfSquares = squaresOfValues(grid)/(16-availableCells(grid))
	#return avgOfSquares + newGradient(grid)







	#Leftmost
	#return squaresOfValues(grid) + availableCells(grid) - differenceOfTiles(grid)*2 + potentialMerges(grid) + monotinicity(grid) * 100


	#Submit:
	#return squaresOfValues(grid) + availableCells(grid) - differenceOfTiles(grid) + potentialMerges(grid) + monotinicity(grid)



	#Left most batch of 10
	#return availableCells(grid)*4 + squaresOfValues(grid) - math.sqrt(differenceOfTiles(grid))














	#0 leftmost run a bunch
	#return squaresOfValues(grid) + potentialMerges(grid)*1000 - math.sqrt(differenceOfTiles(grid))


	#1 left mid
	#return squaresOfValues(grid) + potentialMerges(grid)*1000 - math.sqrt(differenceOfTiles(grid))

	#2 mid right
	#return squaresOfValues(grid) + monotinicity(grid)*100 + potentialMerges(grid)













	#1
	#return heuristicMerges(grid)*4 + squaresOfValues(grid) - math.sqrt(differenceOfTiles(grid))
	
	#2
	#return potentialMerges(grid) + squaresOfValues(grid) - math.sqrt(differenceOfTiles(grid))





	#Left most 
	#return squaresOfValues(grid) + monotinicity(grid) + potentialMerges(grid) + availableCells(grid)

	#Middle
	#return squaresOfValues(grid) + monotinicity(grid)*10 + potentialMerges(grid) + availableCells(grid)

	#rightMiddle
	#return squaresOfValues(grid) + monotinicity(grid)*10 + potentialMerges(grid)*10 + availableCells(grid)

	#right
	#return squaresOfValues(grid) + monotinicity(grid)*100 + potentialMerges(grid) + availableCells(grid)









	#print("squares: ",squaresOfValues(grid), ". gradient: ",gradient(grid), ". difference tiles: ",differenceOfTiles(grid))#round(differenceOfTiles(grid)),0)))
	#return squaresOfValues(grid) + gradient(grid) - differenceOfTiles(grid)
	# print("mergesVal: "+str(heuristicMerges(grid)*4) + "\n" +
	# "gradientVal: " + str(heuristicGradientValues(grid)) + "\n" +
	# "maxTileVal: " + str(math.log(grid.getMaxTile())*4) + "\n" +
	# "clusterVal: " + str(heuristicClusterLikeTiles(grid))+"\n"
	# )

	#print("merge: ", heuristicMerges(grid)*4, ". squares: ",squaresOfValues(grid),". difference: ",- round(math.sqrt(differenceOfTiles(grid)),0),". gradient: ", round(gradient(grid),0) )
	#return heuristicMerges(grid)*4 + squaresOfValues(grid) - math.sqrt(differenceOfTiles(grid)) + gradient(grid)

	#print("merge: ", heuristicMerges(grid)*100, ". squares: ",squaresOfValues(grid)/100,". gradient: ",round(math.sqrt(gradient(grid)),0),". diffTiles: ",- round(math.sqrt(differenceOfTiles(grid)),0))
	#return heuristicMerges(grid)*100 + squaresOfValues(grid)/100 + math.sqrt(gradient(grid)) - math.sqrt(differenceOfTiles(grid))

	
	#print("merge: ", (heuristicMerges(grid)* grid.getMaxTile())**2, ". squares: ",squaresOfValues(grid),". gradient: ",- round(math.sqrt(differenceOfTiles(grid)),0))
	#return (heuristicMerges(grid)* grid.getMaxTile())**2 + squaresOfValues(grid) - math.sqrt(differenceOfTiles(grid))


	"""Is depth 3 or 4 better?"""


	"""Okay heristic weights"""
	#print("merge: ", heuristicMerges(grid)*10, ". squareValues: ",math.sqrt(math.sqrt(squaresOfValues(grid))),". diffTiles: ",-math.sqrt(differenceOfTiles(grid)))
	#return heuristicMerges(grid)*10 + math.sqrt(squaresOfValues(grid)) - math.sqrt(differenceOfTiles(grid))


	""" merges, difference of tiles, squares of value"""
	"""Past heuristic weights and end values that WORK"""
	#heuristicMerges(grid)*4 + squaresOfValues(grid) - math.sqrt(differenceOfTiles(grid)) :: 1024,512,256,128,64 CLOSE!!

	#return heuristicMerges(grid) + squaresOfValues(grid) + gradient(grid) - math.sqrt(sqrDiffOfTiles(grid))*10
	# snake = []
	# for i, col in enumerate(zip(*grid.map)):
	# 	snake.extend(reversed(col) if i % 2 == 0 else col)

	# m = max(snake)
	# return sum(x/10**n for n, x in enumerate(snake)) - \
	# math.pow((grid.map[3][0] != m)*abs(grid.map[3][0] - m), 2)
	
	#print("merge: ", (heuristicMerges(grid)* 4, ". squares: ",squaresOfValues(grid), "difference tiles: ",round(math.sqrt(differenceOfTiles(grid)),0)))#". gradient: ",- round(math.sqrt(differenceOfTiles(grid)),0))

	#return squaresOfValues(grid) + potentialMerges(grid)*1000 - math.sqrt(differenceOfTiles(grid)) + gradient(grid)
	

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






def alphaBetaIDS(currentGrid, timeLimit):
	
	#This whole IDS is taking place to determine 1 overarching move. 
	# So the time limit keeps ticking (no reset) for all iterations of IDS
	startTime = time.clock()
	maxPlayerTurn = True
	alpha = -math.inf
	beta = math.inf
	maxDepth = 1
	maxScore = 0


	#Treating timeLimit as 0.2 here but as 0.15 in alphabeta???????
	while(time.clock() - startTime < timeLimit): 
	
		scoreAtThisDepth = alphaBeta(currentGrid, alpha, beta, maxPlayerTurn, maxDepth, startTime)
		maxDepth += 1

		#print("maxdepth: ",maxDepth)
		#The score could increase or decrease with more depth?
		#Return the highest value from all depth levels of this given child
		if scoreAtThisDepth > maxScore:
			maxScore = scoreAtThisDepth

	return maxScore
	#return alphaBeta(currentGrid, alpha, beta, maxPlayerTurn, maxDepth, startTime)


	#change order of move u look at so go to corner


def alphaBeta(currentGrid, alpha, beta, maxPlayerTurn, depth, startTime):
	#print(depth)

	if time.clock() - startTime > 0.15 or len(currentGrid.getAvailableMoves()) == 0:

		print("RANNNNNNNNN OUUTTUTUUTUTUTUT OF TIMEMEMEMEMEMEMMEMM")
		if maxPlayerTurn:
			return alpha
		else:
			return beta

	if depth == 0:
		
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








