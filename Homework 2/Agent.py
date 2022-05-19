#Daniel Kantor and Erin Li
#2/8/2022
#Homework 2 - Agent Class
#Description - Class used to represent the Agent, creates the starting location of agent, can randomly move it around the envrionment and can move it one spot in each direction

import random

class Agent:
    
    def __init__(self, locationX = None, locationY = None):
        self.locationX = locationX
        self.locationY = locationY
    
    #param: self, visitedLocations - list of locations that have already been visited
    #return: newlocation - the new starting location
    #description: generates the starting location for an agents
    def startingLocation(self, visitedLocations):
        while(True): 
            randomX = random.randint(0,9) # generates random starting locations
            randomY = random.randint(0,9)
            newLocation = [randomX, randomY]
            if newLocation not in visitedLocations: #if the generated location hasnt been used as a starting location then use it as a location
                self.locationX = randomX
                self.locationY = randomY
                break
        return newLocation
    
    #param: self
    #return: startLoc - the  starting location
    #description: generates the starting location for an agent that won't have its starting location change
    def staticStartingLocation(self): 
        self.locationX = random.randint(0,9)
        self.locationY = random.randint(0,9)
        startLoc = [self.locationX, self.locationY]
        return startLoc
    
    #param: self
    #return: none
    #description: generates random locations for the agent to "teleport" around the environment
    def randomLocation(self):
        self.locationX = random.randint(0,9)
        self.locationY = random.randint(0,9)        
    
    #param: self
    #return: none
    #description: moves the agent one grid to the left
    def moveLeft(self):
        self.locationX = self.locationX - 1
    
    #param: self
    #return: none
    #description: moves the agent one grid to the right
    def moveRight(self):
        self.locationX = self.locationX + 1
    
    #param: self
    #return: none
    #description: moves the agent one grid up
    def moveUp(self):
        self.locationY = self.locationY + 1
        
    #param: self
    #return: none
    #description: moves the agent one grid to the down
    def moveDown(self):
        self.locationY = self.locationY - 1
