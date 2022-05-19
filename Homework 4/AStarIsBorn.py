# AStarIsBorn.py
# Daniel Kantor and Josh Freeman
# 3/4/2022
# Homework 4
# A program that implements and averages 4 different search algorithms DFS, BFS, GBS, and A*
import random
import math

size = 10  # The dimensions of the square grid x by x


def main():
    envDict = createEnvironment()  # Create the environment
    weightEnvDict = createEnvironmentWeight()  # Create a dictionary of weights (costs)
    # Results Lists
    BFSResultList = list()
    DFSResultList = list()
    GBSResultList = list()
    AStarResultList = list()

    for i in range(100):  # Run each algorithm on 100 different environments
        envStates = createStates()
        BFSResultList.append(BFS(envDict, envStates))
        DFSResultList.append(DFS(envDict, envStates))
        GBSResultList.append(GBS(envDict, envStates))
        AStarResultList.append(AStar(weightEnvDict, envStates))

    # Average the results
    BFSAvg = averageSteps(BFSResultList)
    DFSAvg = averageSteps(DFSResultList)
    GBSAvg = averageSteps(GBSResultList)
    AStarAvg = averageSteps(AStarResultList)

    # Print them pretty
    print("BFS: " + str(BFSAvg[0]) + " average number of steps \n     " + str(BFSAvg[1]) + " times found.")
    print("DFS: " + str(DFSAvg[0]) + " average number of steps \n     " + str(DFSAvg[1]) + " times found.")
    print("GBS: " + str(GBSAvg[0]) + " average number of steps \n     " + str(GBSAvg[1]) + " times found.")
    print("AStar: " + str(AStarAvg[0]) + " average number of steps \n     " + str(AStarAvg[1]) + " times found.")


def averageSteps(resultList):
    counter = 0  # Count the number of successful runs
    totalSteps = 0  # The sum of all the trials
    for checkList in resultList:  # For each successful run of the algorithm
        if checkList[0] is True:  # add the number of steps to the total
            totalSteps += checkList[1]
            counter += 1

    return totalSteps / counter, counter  # Return the average and how many runs succeeded


def createEnvironment():  # Create the environment
    envDict = dict()  # Create an empty dictionary and fill it with coordinates (0, 0) to one less than the size

    for i in range(0, size):
        for j in range(0, size):
            envDict[i, j] = list()
            if i < size - 1:
                envDict[(i, j)].append((i + 1, j))
            if i > 0:
                envDict[(i, j)].append((i - 1, j))
            if j < size - 1:
                envDict[(i, j)].append((i, j + 1))
            if j > 0:
                envDict[(i, j)].append((i, j - 1))

    return envDict


def createEnvironmentWeight(): #Create the environment with weighted connections for A* use
    envDict = {}

    for i in range(0, size):
        for j in range(0, size):
            envDict[i, j] = list()
    for i in range(0, size):
        for j in range(0, size):
            if i < size - 1:
                weight = random.randint(1, 20)
                envDict[(i, j)].append((i + 1, j, weight))
                envDict[(i + 1, j)].append((i, j, weight))
            if j < size - 1:
                weight = random.randint(1, 20)
                envDict[(i, j)].append((i, j + 1, weight))
                envDict[(i, j + 1)].append((i, j, weight))
    return envDict


def createStates(): #Creates a matrix that represents the states of each node in the environment and populates it with walls
    states = [[0 for x in range(size)] for y in range(size)]
    states[size - 1][size - 1] = 3
    counter = 0

    while counter < 7:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        if (x == 0 and y == 0) or (x == size - 1 and y == size - 1):
            pass
        elif states[x][y] == 1:
            pass
        else:
            states[x][y] = 1
            counter += 1

    return states


# Un-visit each node has been. And double-check the exit is still 3
def unVisit(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 2:
                matrix[i][j] = 0
    matrix[size - 1][size - 1] = 3


# Use Euclidian distance to generate a matrix of Heuristics corresponding to the coordinates in the graph
def heuristicMatrix():
    hMatrix = [[math.dist((size - 1, size - 1), (x, y)) for x in range(size)] for y in range(size)]
    return hMatrix


# Breadth First Search
def BFS(envDict: dict, envStates):
    found = False
    stepCount = 0
    seen = []
    BFSqueue = [(0, 0)]

    while BFSqueue:  # run until the queue is empty
        top = BFSqueue.pop(0)  # get top node in the queue (0 to get the first element om the list)
        if top == (size - 1, size - 1):
            found = True
            break
        elif top not in seen:  # check if node has been visited yet
            seen.append(top)
            stepCount += 1
            for connection in envDict[top]:  # get all the connections of top node
                if connection not in seen and envStates[connection[0]][
                    connection[1]] != 1:  # if the connection hasn't been visited yet, then add it to the queue
                    envStates[connection[0]][connection[1]] = 2
                    BFSqueue.append(connection)

    return found, stepCount


# Depth First Search with Stepwise counting
def DFS(environment: dict, stateMatrix):
    unVisit(stateMatrix)  # Clear the visited nodes in the matrix
    visited = list()  # Create a list of visited nodes to keep a traversal path
    stack = list()  # A stack of nodes to visit and
    stack.append((0, 0))  # Append the start to the stack
    found = False  # Has the exit been found

    while stack:  # While the stack is not empty
        peek = stack[-1]  # Take the item from the top of the stack but do not remove it
        visited.append(peek)  # Add it to the path
        neighbors = list()  # Create a list of potential places to go

        if stateMatrix[peek[0]][peek[1]] == 3:  # If the peek is the exit
            found = True  # We found it!
            return found, len(visited), visited

        stateMatrix[peek[0]][peek[1]] = 2  # Otherwise, set the state of peek to 2 (visited)

        for neighbor in environment[peek]:  # For each neighbor check if we can go there
            if stateMatrix[neighbor[0]][neighbor[1]] == 0 or stateMatrix[neighbor[0]][neighbor[1]] == 3:
                neighbors.append(neighbor)  # Add it to the Neighbor list

        if not neighbors:  # If the Neighbor list is empty
            stack.pop(-1)  # Pop the top of the stack going back one node
        else:
            stack.append(neighbors[0])  # Otherwise, add the first neighbor to the stack

    return found, len(visited), visited  # If we never find the exit return


# A* algorithm finds the most efficient path to the exit
def AStar(environment: dict, stateMatrix):
    stepCount = 0  # Keeps track of how many nodes we visit
    unVisit(stateMatrix)  # Makes sure the environment is not already visited
    orderedList = list()  # A heap

    hMatrix = heuristicMatrix()  # The matrix keeping track of the Euclidean distance for each node
    pos = (0, 0)  # Starting position
    prevCost = 0  # The traversal cost of all previous nodes

    while True:
        stateMatrix[pos[0]][pos[1]] = 2  # Visit the current node
        for neighbor in environment[pos]:  # For each neighbor of the current node get it's state
            nS = stateMatrix[neighbor[0]][neighbor[1]]
            if nS != 1 and nS != 2:  # If it's not a wall or already visited
                nH = hMatrix[neighbor[0]][neighbor[1]]  # Get the heuristic of that neighbor
                orderedList.append((prevCost + neighbor[2] + nH, prevCost + neighbor[2], (neighbor[0], neighbor[1])))
            # Add it to the list and update the cost to get to that neighbor
        orderedList.sort(key=lambda x: x[0])  # Order the list

        if not orderedList:  # If the ordered list is empty there is no solution
            return False, stepCount

        top = orderedList.pop(0)  # Get the next minimum traversal cost + Heuristic node
        pos = top[2]  # Get its position
        prevCost = top[1]  # Get its cost and make it the previous cost
        stepCount += 1  # Count it

        if pos == (size - 1, size - 1):  # If we are at the exit
            return True, stepCount  # Finish


# Greedy Best Search
def GBS(environment: dict, stateMatrix):
    unVisit(stateMatrix)  # Set all 2s to 0s
    hMatrix = heuristicMatrix()  # Set the Heuristics matrix
    pathList = list()  # A list of the path taken
    found = False  # If the exit is found
    pos = (0, 0)  # Starting Pos

    while not found:  # While the Exit is not found
        stateMatrix[pos[0]][pos[1]] = 2  # Set the current state to visited
        H = hMatrix[pos[0]][pos[1]]  # Check the Heuristic of this node
        hurList = list()  # Create a list of Heuristics
        neighborList = list()  # Create a List of Neighbors
        pathList.append(pos)  # Add our start position to the path

        for neighbor in environment[pos]:  # For each neighbor Check its state
            nS = stateMatrix[neighbor[0]][neighbor[1]]
            if nS != 1:  # If it's not a wall add its heuristic and itself to their respective lists
                nH = hMatrix[neighbor[0]][neighbor[1]]
                hurList.append(nH)
                neighborList.append(neighbor)

        if not neighborList:  # If there are no neighbors we didn't find the exit
            return False, len(pathList)

        minValue = min(hurList)  # Find the minimum Heuristic in the list
        minNeighbor = neighborList[hurList.index(minValue)]  # It has the same index as its corresponding node

        if minValue == 0:  # If the heuristic is 0 the exit has been found
            return True, len(pathList)
        elif minValue < H:  # Otherwise, check to see if the heuristic is less than the current node
            pos = minNeighbor  # Make the minimum Neighbor the new pos
        else:
            return False, len(pathList)


if __name__ == "__main__":
    main()
