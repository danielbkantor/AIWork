import random

graph = {0: [1, 2],
             1: [0, 2, 3],
             2: [0, 1, 3, 4, 5],
             3: [1, 2, 4],
             4: [2, 3, 5],
             5: [2, 4],
             6: []
             }
def main():

    
    map = [-1, -1, -1, -1, -1, -1, -1]

        
    assignColors(0, map)
    
    print(map)

    
    
def assignColors(node, map):    
    colors = [1, 2, 3]  
    if -1 not in map:
        return True

    for c in colors:
        if checkMap(node, c, map):
            map[node] = c
            if assignColors(mostConstraining(map), map) is True:
                return True
            map[node] = -1
    return False
    
        
def checkMap(node, color, map):
    for i in graph[node]:
        if map[i] == color:
            return False
    return True

def mostConstrained(map):
    node = 0
    topCount = 0
    emptyIndex = 0
    for index, i in enumerate(map):
        count = 0
        if i == -1:
            if not graph[index]:
                emptyIndex = index
            for j in graph[index]:
                if map[j] != -1:
                    count += 1
        if count > topCount:
            node = index
            topCount = count
    if topCount == 0:
        return emptyIndex
    
    return node
            
def mostConstraining(map):
    val = -1
    returnIndex = 0 
    for index, i in enumerate(graph.values()):  
        if map[index] == -1:
            if len(i) > val:
                val = len(i)
                returnIndex = index
    return returnIndex
        
                     
def leastConstrainig(map):
    pass
    

if __name__ == "__main__":
    main()