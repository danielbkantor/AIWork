#Daniel Kantor
#2/17/2022
#Homework 3 
#Implement an adjacency list that reads creates the list by reading from a file. Then has various functionality including DFS, BFS, print the graph, store graph info in new file
#add connection, and search for a specific node in the graph. 

def main():
   
    adjDict = {} #dictionary used to represent the adjacency graph

    with open("testFile.txt", "r") as file:
        firstLine = file.readline() #read the first line of the file which is the number of nodes in the graph
        
        for i in range(1, int(firstLine) + 1): #create a key for each node in the graph and initalize each value as an empty list
            adjDict[str(i)] = list()

        for line in file: #get the connections from from the file and add them to the dictionary as key, value pairs
            splitFile = line.split()
            adjDict[splitFile[0]].append(splitFile[1])
    
    menu()
    
    menuNum = int(input("Please choose an option\n"))
    
    while(menuNum != 7):
        
        if(menuNum == 1):
            
            print(adjDict)
            
            vertex = input("\nPlease choose a vertex to print the vertices connceted to it\n")

            if vertex not in adjDict: #check if node you are searching for exists
                print("\nError -- Not a valid vertex -- Please reselect an option")
                menu()
                menuNum = int(input("Please choose an option\n"))
            else:
                print("\n" + vertex + ": " + ', '.join(adjDict[vertex]) + "\n")  #print list of nodes connected to node you are searching for
                menu()
                menuNum = int(input("Please choose a new option!\n"))
                
        elif(menuNum == 2):
            print("\nGRAPH:")            
            for i in adjDict: 
                print(i + ": " + ', '.join(adjDict[i])) # print all nodes and their connections
            
            print()
            menu()
            menuNum = int(input("Please choose a new option!\n"))
                
        elif(menuNum == 3):
            node = input("\nPlease enter which node you want to insert an edge to\n")
            
            if node not in adjDict: #check if node you are adding a connection to exists
                print("\nError -- The vertex " + node + " does not exist -- Please reselect an option")
                menu()
                menuNum = int(input("Please choose an option\n"))
            else:
                connectionVertex = input("\nPlease enter the vertex you want to connect to " + node + "\n")
                if connectionVertex in adjDict[node]: #check if the connection already exists
                    print("\nThis connection already exists -- Please reselect an option")
                    menu()
                    menuNum = int(input("Please choose an option\n"))
                else:
                    adjDict[node].append(connectionVertex) #add connection
                    menu()
                    menuNum = int(input("Please choose a new option!\n"))
                       
        elif(menuNum == 4):
            f = open("newFile.txt", "w")
            for key, values in adjDict.items(): #get all items in the dictionary
                for val in values:
                    f.write(key + " " + val + "\n")
                    
            f.close()
            print()
            menu()
            menuNum = int(input("Please choose a new option!\n"))
        
        elif(menuNum == 5):
            startingNode = input("\nPlease enter a starting node\n")
            if startingNode not in adjDict:  #check if your starting BFS node exists
                print("\nError -- Not a valid vertex -- Please reselect an option")
                menu()
                menuNum = int(input("Please choose an option\n"))
            else:
                print("\nBFS Result: " + ', '.join(BFS(startingNode, adjDict)).replace(',', '') + "\n") 
                menu()
                menuNum = int(input("Please choose a new option!\n"))
                
        elif(menuNum == 6):
            startingNode = input("\nPlease enter a starting node\n")
            if startingNode not in adjDict: #check if your starting DFS node exists
                print("\nError -- Not a valid vertex -- Please reselect an option")
                menu()
                menuNum = int(input("Please choose an option\n"))
            else:
                print("\nDFS Result: " + ', '.join(DFS(startingNode, adjDict)).replace(',', '') + "\n")
                menu()
                menuNum = int(input("Please choose a new option!\n"))  
        else:
            print("\nNot a valid option -- Please reselect!")
            menu()
            menuNum = int(input("Please choose an option\n"))
            
def BFS(startingNode, adjDict):
    
    seen = []
    BFSqueue = []
    
    BFSqueue.append(startingNode) #add starting node to queue
    
    while BFSqueue: #run until the queue is empty
        print(BFSqueue)
        top = BFSqueue.pop(0) #get top node in the queue (0 to get the first element om the list)
        #print(top)
        if top not in seen: #check if node has been visited yet
            seen.append(top)  
            for connection in adjDict[top]: #get all the connections of top node
                if connection not in seen: #if the connection hasnt been visited yet, then add it to the queue
                    BFSqueue.append(connection)
                
    return seen 
    
def DFS(startingNode, adjDict):
    
    seen = []
    DFSstack = []
    
    DFSstack.append(startingNode) #add starting node to stack 
    
    while DFSstack: #run until the stack is empty
        print(DFSstack)
        top = DFSstack.pop() #get top node in the stack
        #print(top)
        if top not in seen: #check if the node has been visited yet 
            seen.append(top) 
            for connection in adjDict[top]: #get all conections of the node
                if connection not in seen: #if the connection hasnt been visited yet, then add it to the stack
                    DFSstack.append(connection)
                
    return seen
      
def menu():
    print("1. Vertices Connected to")
    print("2. Print Graph")
    print("3. Add Conection")
    print("4. Store to file")
    print("5. BFS")
    print("6. DFS")
    print("7. Exit")
    
if __name__ == "__main__":
    main()