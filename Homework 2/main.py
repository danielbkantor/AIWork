#Daniel Kantor and Erin Li
#2/8/2022
#Homework 2 - main method
#Description - file used to implement the different experiments using the experiment and agent classes

import Environment as e
import Agent as a
import random
import copy

def main():
    env = e.Environment()
    createEnv = env.createDirtyEnvironment() #create envrionment that will be used throughout the duration of experiment one and two
    experimentOne(createEnv)
    experimentTwo(createEnv)
    
    ag = a.Agent()
    startPosition = ag.staticStartingLocation() #set location that will be used throughout the duration of experiment one and two
    experimentThree(startPosition)
    experimentFour(startPosition)

#param: createEnv - envrionment that was generated for the experiment was used
#return: none
#description: the code to run the first experiment where the envrionment doesn't change and starting location does change every iteration and the agent moves either up, right, left, or down
def experimentOne(createEnv):
    ag = a.Agent()
    visitedLocation = []
    cleanCounterList = []
    for i in range(100):
        cleanCounter = 0
        tempEnv = copy.deepcopy(createEnv) #copy the envrionment for use each iteration 
        loc = ag.startingLocation(visitedLocation) #get the starting location of the agent
        visitedLocation.append(loc)
        if tempEnv[loc[0]][loc[1]] == 1: # determine if starting location dirty if so, clean starting location
            tempEnv[loc[0]][loc[1]] = 0
            cleanCounter += 1
        for i in range(75):
            randomMovement = random.randint(0,3) #generate a random number to determine which direction the agent moves
            if randomMovement == 0:
                if ag.locationX != 0:
                    ag.moveLeft()
                    if tempEnv[ag.locationX][ag.locationY] == 1: # determine if new location dirty if so, clean starting location
                        tempEnv[ag.locationX][ag.locationY] = 0
                        cleanCounter += 1
            elif randomMovement == 1:
                if ag.locationX != 9:
                    ag.moveRight()
                    if tempEnv[ag.locationX][ag.locationY] == 1: # determine if new location dirty if so, clean starting location
                        tempEnv[ag.locationX][ag.locationY] = 0
                        cleanCounter += 1
            elif randomMovement == 2:
                if ag.locationY != 9:
                    ag.moveUp()
                    if tempEnv[ag.locationX][ag.locationY] == 1: # determine if new location dirty if so, clean starting location
                        tempEnv[ag.locationX][ag.locationY] = 0
                        cleanCounter += 1
            else:
                if ag.locationY != 0:
                    ag.moveDown()
                    if tempEnv[ag.locationX][ag.locationY] == 1: # determine if new location dirty if so, clean starting location
                        tempEnv[ag.locationX][ag.locationY] = 0
                        cleanCounter += 1
                        
        cleanCounterList.append(cleanCounter)
    print("Average Spots Cleaned (Experiment 1): " + str(sum(cleanCounterList)/len(cleanCounterList)))  

#param: createEnv - envrionment that was generated for the experiment was used
#return: none
#description: the code to run the first experiment where the envrionment doesn't change and starting location does change every iteration and the agent moves around randomly          
def experimentTwo(createEnv):
    ag = a.Agent()
    visitedLocation = []
    cleanCounterList = []
    for i in range(100):
        cleanCounter = 0
        tempEnv = copy.deepcopy(createEnv) #copy the envrionment for use each iteration 
        loc = ag.startingLocation(visitedLocation) #get the starting location of the agent
        visitedLocation.append(loc)
        if tempEnv[loc[0]][loc[1]] == 1: # determine if starting location dirty if so, clean starting location
            tempEnv[loc[0]][loc[1]] = 0
            cleanCounter += 1
        for i in range(75):
            ag.randomLocation() #randomly move the agent to new location
            if tempEnv[ag.locationX][ag.locationY] == 1: # determine if new location dirty if so, clean starting location
                tempEnv[ag.locationX][ag.locationY] = 0
                cleanCounter += 1
                
        cleanCounterList.append(cleanCounter)
    print("Average Spots Cleaned (Experiment 2): " + str(sum(cleanCounterList)/len(cleanCounterList)))  

#param: startPosition - the starting position that the agent will always start in
#return: none
#description: the code to run the first experiment where the envrionment changes every iteration and the starting location is static and the agent moves either up, right, left, or down
def experimentThree(startPosition):
    cleanCounterList = []
    for i in range(100):
        cleanCounter = 0 
        tempStart = startPosition #save the starting location
        ag = a.Agent(tempStart[0], tempStart[1]) #create agent with the starting location
        env = e.Environment()
        createEnv = env.createDirtyEnvironment() # generate envrionment
        if createEnv[ag.locationX][ag.locationY] == 1: # determine if starting location dirty if so, clean starting location
            createEnv[ag.locationX][ag.locationY] = 0
            cleanCounter += 1
        for i in range(75):
            randomMovement = random.randint(0,3) #generate a random number to determine which direction the agent moves
            if randomMovement == 0:
                if ag.locationX != 0:
                    ag.moveLeft()
                    if createEnv[ag.locationX][ag.locationY] == 1: # determine if new location dirty if so, clean starting location
                        createEnv[ag.locationX][ag.locationY] = 0
                        cleanCounter += 1
            elif randomMovement == 1:
                if ag.locationX != 9:
                    ag.moveRight()
                    if createEnv[ag.locationX][ag.locationY] == 1: # determine if new location dirty if so, clean starting location
                        createEnv[ag.locationX][ag.locationY] = 0
                        cleanCounter += 1
            elif randomMovement == 2:
                if ag.locationY != 9:
                    ag.moveUp()
                    if createEnv[ag.locationX][ag.locationY] == 1: # determine if new location dirty if so, clean starting location
                        createEnv[ag.locationX][ag.locationY] = 0
                        cleanCounter += 1
            else:
                if ag.locationY != 0:
                    ag.moveDown()
                    if createEnv[ag.locationX][ag.locationY] == 1: # determine if new location dirty if so, clean starting location
                        createEnv[ag.locationX][ag.locationY] = 0
                        cleanCounter += 1
                        
        cleanCounterList.append(cleanCounter)
    print("Average Spots Cleaned (Experiment 3): " + str(sum(cleanCounterList)/len(cleanCounterList)))  

#param: startPosition - the starting position that the agent will always start in
#return: none
#description: the code to run the first experiment where the envrionment changes every iteration and the starting location is static and the agent moves around randomly
def experimentFour(startPosition):
    cleanCounterList = []
    for i in range(100):
        cleanCounter = 0 
        tempStart = startPosition #save the starting location 
        ag = a.Agent(tempStart[0], tempStart[1]) #create agent with the starting location
        env = e.Environment()
        createEnv = env.createDirtyEnvironment() # generate envrionment
        if createEnv[ag.locationX][ag.locationY] == 1: # determine if starting location dirty if so, clean starting location
            createEnv[ag.locationX][ag.locationY] = 0
            cleanCounter += 1
        for i in range(75):
            ag.randomLocation()  #randomly move the agent
            if createEnv[ag.locationX][ag.locationY] == 1: # determine if new location dirty if so, clean starting location
                createEnv[ag.locationX][ag.locationY] = 0
                cleanCounter += 1
                
        cleanCounterList.append(cleanCounter)
    print("Average Spots Cleaned (Experiment 4): " + str(sum(cleanCounterList)/len(cleanCounterList)))  
                     
if __name__ == "__main__":
    main()