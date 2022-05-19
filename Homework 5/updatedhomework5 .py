import random

# Flags
mConstrained = True
mConstraining = True
lConstraining = False
fChecking = False

# Global Variables
size = 200
bias = .99


def randGraph():
    graph1 = dict()
    for i in range(size):
        graph1[i] = list()

    for i in range(size):
        for j in range(size):
            if i != j:
                choice = random.random()
                if choice >= bias:
                    if i not in graph1[j] and j not in graph1[i]:
                        graph1[i].append(j)
                        graph1[j].append(i)
    return graph1


def makeMap():
    c_map = [-1 for x in range(size)]

    return c_map


# graph = {0: [1, 2],
#          1: [0, 2, 3],
#          2: [0, 1, 3, 4, 5],
#          3: [1, 2, 4],
#          4: [2, 3, 5],
#          5: [2, 4],
#          6: []
#          }


def main():

    c_graph = randGraph()
    
    print(c_graph)
    
    c_map = makeMap()

    assignColors(0, c_map, c_graph)
    
    #print(c_map)
    print(c_map)
    
    #leastConstraining(c_map, c_graph, 0)

def assignColors(node, c_map, graph):
    print(c_map)
    colors = [1, 2, 3]  
    if -1 not in c_map:
        return True
    for c in colors:
        if checkMap(node, c, c_map, graph):
            c_map[node] = c
            if mConstrained is True:
                if assignColors(mostConstrained(c_map, graph), c_map, graph) is True:
                    return True
                c_map[node] = -1
            elif mConstraining is True:
                if assignColors(mostConstraining(c_map, graph, []), c_map, graph) is True:
                    return True
                c_map[node] = -1
            elif lConstraining is True:
                if assignColors(leastConstraining(c_map, graph), c_map, graph) is True:
                    return True
                c_map[node] = -1
            else:
                nextNode = random.randint(0, size - 1)
                if assignColors(nextNode, c_map, graph) is True:
                    return True
                c_map[node] = -1
    return False
    
        
def checkMap(node, color, c_map, graph):
    for i in graph[node]:
        if c_map[i] == color:
            return False
    return True


def mostConstrained(c_map, graph):
    topCount = 0
    tieList = list()
    for index, i in enumerate(c_map):
        count = 0
        if i == -1:
            for j in graph[index]:
                if c_map[j] != -1:
                    count += 1
        if count > topCount:
            tieList = [index]
            topCount = count
        elif count == topCount:
            tieList.append(index)
    if mConstraining:
        return mostConstraining(c_map, graph, tieList)
    else:
        return tieList[0]


def mostConstraining(c_map, graph, tie_list):
    val = -1
    returnIndex = 0
    if mConstrained:
        for o in tie_list:
            if c_map[o] == -1:
                if len(graph[o]) > val:
                    val = len(graph[o])
                    returnIndex = o
    elif lConstraining:
        return leastConstraining(c_map, graph, returnIndex)
    else:
        for index, i in enumerate(graph.values()):
            if c_map[index] == -1:
                if len(i) > val:
                    val = len(i)
                    returnIndex = index
    return returnIndex
         
def getNumValuesRemaining(c_map, graph, node):
    count = 3
    oneFlag = False
    twoFlag = False
    threeFlag = False
    
    for i in graph[node]:
        if c_map[i] == 1 and oneFlag == False:
            count -= 1
            oneFlag = True
        elif c_map[i] == 2 and twoFlag == False:
            count -= 1
            twoFlag = True
        elif c_map[i] == 3 and threeFlag == False:
            count -= 1
            threeFlag = True
    return count
                             
def leastConstraining(c_map, graph, node):
    largestCount = -1
    bestColor = -1
    for c in range(1, 4):
        sum = 0 
        c_map[node] = c
        for i in graph[node]:
            sum += getNumValuesRemaining(c_map, graph, i)
        if sum > largestCount:
            bestColor = c
            largestCount = sum
    print(bestColor)     
    return node, bestColor  
    

if __name__ == "__main__":
    main()