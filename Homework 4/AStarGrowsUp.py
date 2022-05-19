from ast import AST
import random
import math
size = 10

def main():
    envDict = createEnvironment()
    #envWeights = createWeights()
    BFSResultList = []
    DFSResultList = list()
    GBSResultList = list()
    AStarResultList = list()

    for i in range(1):
        envStates = createStates()
        #printMatrix(envStates)
        # GBSResultList.append(GBS(envDict, envStates))
        # BFSResultList.append(BFS(envDict, envStates))
        # DFSResultList.append(DFS(envDict, envStates))
        #print("DFS: ", DFS(envDict, envStates))
        #printMatrix(envStates)
        #print()
        #unVisit(envStates)
        #print()
        #printMatrix(envStates)
        #print("DFSBS: ", DFSSBS(envDict, envStates))
        #printMatrix(envStates)
        weightEnv = createEnvironmentWeight()
        print(AStar(weightEnv, envStates))

    # GBSResultList.remove([0] is False)
    # print(GBSResultList)

    # print(BFSResultList)

    # print("GBS: ", GBS(envDict, envStates))

    # print("BFS: ", BFS(envDict, envStates))


def createEnvironment():
    envDict = {}

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

def createEnvironmentWeight():
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

def createStates():
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
            # print("HERE")

    return states


def printMatrix(matrix):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matrix]))


def unVisit(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 2:
                matrix[i][j] = 0
    matrix[size - 1][size - 1] = 3


def heuristicMatrix():
    hMatrix = [[math.dist((size - 1, size - 1), (x, y)) for x in range(size)] for y in range(size)]
    return hMatrix

def BFS(envDict: dict, envStates):
    found = False
    stepCount = -1
    seen = []
    BFSqueue = [(0, 0)]

    # print(envStates)

    while BFSqueue:  # run until the queue is empty
        top = BFSqueue.pop(0)  # get top node in the queue (0 to get the first element om the list)
        if top == (size - 1, size - 1):
            stepCount += 1
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

    # print(seen)
    # print(stepCount)

    return found, stepCount


def DFS(environment: dict, envStates):
    stack = list()                          # Create a stack to control the order of the nodes visited LIFO
    visited = list()                        # Create a list of visited nodes to prevent visiting twice
    stack.append((0, 0))                    # Add the starting point to the stack
    found = False

    while len(stack) != 0:                  # While the stack isn't empty
        peek = stack.pop()                  # Take the top of the stack (end of the list) and check if it's been visited
        if peek == (size-1, size-1):
            found = True
            return found, len(visited), visited
        elif peek not in visited:            # If not, visit it (Add it to the list of visited nodes)
            visited.append(peek)
            for neighbor in environment[peek]:    # For each Neighbor listed in the graph put them on the stack
                if neighbor not in visited and envStates[neighbor[0]][neighbor[1]] != 1:  # No walls either
                    envStates[neighbor[0]][neighbor[1]] = 2
                    stack.append(neighbor)  # For each neighbor not visited, add them to the top of the stack

    #print("SAH DUDE", visited)
    return found, len(visited), visited


def DFSSBS(environment: dict, envStates):
    stack = list()                          # Create a stack to control the order of the nodes visited LIFO
    visited = list()                        # Create a list of visited nodes to prevent visiting twice
    stack.append((0, 0))                    # Add the starting point to the stack
    found = False

    while len(stack) != 0:                  # While the stack isn't empty
        peek = stack.pop()                  # Take the top of the stack (end of the list) and check if it's been visited
        neighbors = list()
        if peek == (size-1, size-1):
            found = True
            return found, len(visited), visited
        elif peek not in visited:            # If not, visit it (Add it to the list of visited nodes)
            visited.append(peek)
            for neighbor in environment[peek]:    # For each Neighbor listed in the graph put them on the stack
                if envStates[neighbor[0]][neighbor[1]] != 1 and envStates[neighbor[0]][neighbor[1]] != 2:
                    neighbors.append((neighbor, envStates[neighbor[0]][neighbor[1]]))
            if not neighbors:
                if len(visited) >= 2:
                    stack.append(visited[-2])
                    visited.append(visited[-2])
            for n in neighbors:
                envStates[n[0][0]][n[0][1]] = 2
                stack.append((n[0][0], n[0][1]))  # For each neighbor not visited, add them to the top of the stack

    #print(visited)
    return found, len(visited), visited

def AStar(environment: dict, stateMatrix):
    stepCount = 0 
    unVisit(stateMatrix)
    orderedList = list()

    hMatrix = heuristicMatrix()
    pos = (0, 0)
    prevCost = 0
    
    while True:
        stateMatrix[pos[0]][pos[1]] = 2
        #print(stateMatrix)
        for neighbor in environment[pos]:
            nS = stateMatrix[neighbor[0]][neighbor[1]] 
            if nS != 1 and nS != 2:
                nH = hMatrix[neighbor[0]][neighbor[1]]
                print(neighbor)
                orderedList.append((prevCost + neighbor[2] + nH, prevCost + neighbor[2], (neighbor[0], neighbor[1])))
            
        orderedList.sort(key = lambda   x: x[0])
        
        if not orderedList:
            return False, stepCount
        
        #print(orderedList)
        top = orderedList.pop(0)
        pos = top[2]
        prevCost = top[1]
        stepCount += 1

        if pos == (size - 1, size - 1):
            return True, stepCount #length list not step count ?

def GBS(environment: dict, stateMatrix):
    hMatrix = heuristicMatrix()
    pathList = list()
    found = False
    pos = (0, 0)
    # print(hMatrix)
    # print("-" * 50)
    # print(stateMatrix)
    while not found:
        stateMatrix[pos[0]][pos[1]] = 2
        H = hMatrix[pos[0]][pos[1]]
        hurList = list()
        neighborList = list()
        pathList.append(pos)

        for neighbor in environment[pos]:
            nS = stateMatrix[neighbor[0]][neighbor[1]]
            if nS != 1:
                nH = hMatrix[neighbor[0]][neighbor[1]]
                hurList.append(nH)
                neighborList.append(neighbor)

        if not neighborList:
            # print("Hey baby, take me out to dinner")
            # print(pathList)
            return False, len(pathList)

        minValue = min(hurList)
        minNeighbor = neighborList[hurList.index(minValue)]

        # print(minValue)
        # print(minNeighbor)

        if minValue == 0:
            # print(pathList)
            return True, len(pathList)
        elif minValue < H:
            len(pathList)
            pos = minNeighbor
        else:
            # print("Hey! listen!")

            return  False, len(pathList)


if __name__ == "__main__":
    main()
