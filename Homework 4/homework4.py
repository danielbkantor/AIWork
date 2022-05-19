import random
size = 10

def main():
    envDict = createEnvironment()
    envStates = createStates()
    envWeights = createWeights()
    BFSResultList = []
    for i in range(100):
        BFSResultList.append(BFS(envDict))
    print(BFSResultList)
    
    #print(BFS(envDict))
    
def createEnvironment():
    envDict = {}

    for i in range(0, size):
        for j in range(0, size):
            envDict[i, j] = list()       
            if(i < size - 1):
                envDict[(i, j)].append((i + 1, j))
            if(i > 0):
                envDict[(i, j)].append((i - 1, j))
            if(j < size - 1):
                envDict[(i, j)].append((i, j + 1))
            if(j > 0):
                envDict[(i, j)].append((i, j - 1))

    #print(envDict)  
    return envDict

def createStates():
    states = [[0 for x in range(size)] for y in range (size)]       
    states[size - 1][size - 1] = 3
    counter = 0

    while counter < 7:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        if((x == 0 and y == 0) or (x== size - 1 and y == size - 1)):
            pass
        elif states[x][y] == 1:
            pass
        else:
            states[x][y] = 1
            counter += 1
            #print("HERE")
    
    return states

def createWeights():
    weights  = [[0 for x in range(size)] for y in range(size)]

    for i in range(size):
        for j in range(size):
            weight = random.randint(1, 20)
            if(i == j):
                weights[i][j] = 0
            elif weights[j][i] < 1:
                weights[i][j] = weight
                weights[j][i] = weight
            

    #print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
    #     for row in weights]))
    
    return weights

def BFS(envDict):
    
    envStates = createStates()
    found = False
    stepCount = -1
    seen = []
    BFSqueue = []

    #print(envStates)
    
    BFSqueue.append((0,0)) #add starting node to queue

    while BFSqueue: #run until the queue is empty
        top = BFSqueue.pop(0) #get top node in the queue (0 to get the first element om the list)
        if top == (size - 1, size - 1):
            stepCount += 1
            found = True
            break
        elif top not in seen: #check if node has been visited yet
            seen.append(top) 
            stepCount += 1 
            for connection in envDict[top]: #get all the connections of top node
                if connection not in seen and envStates[connection[1]][connection[0]] != 1: #if the connection hasnt been visited yet, then add it to the queue
                    envStates[connection[1]][connection[0]] = 2
                    BFSqueue.append(connection)
                    
                    
                
    #print(seen)
    #print(stepCount)
    
    return (stepCount, found)


    
if __name__ == "__main__":
    main()