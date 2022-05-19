#Daniel Kantor and Erin Li
#2/8/2022
#Homework 2 - Envrionment Class
#Description - Produces a 2x2 list to represent the enviornment that the agent interacts with

import random

class Environment:
    
    def __init__(self):
        self.environmentGrid = [[0 for x in range(10)] for y in range(10)] #create 10 lists inside another list, with each list having 10 entries and initialize the values to 0 (clean)
        
    #param: self
    #return: environmentGrid - the environment created with 50 dirty spots
    #description: creates an environment that has 50 dirty spots
    def createDirtyEnvironment(self):
        count = 0 
        while(count < 50): #runs until 50 spots have been made dirty
            randomX = random.randint(0,9) #generate random spots to attempt to make dirty
            randomY = random.randint(0,9)
            if(self.environmentGrid[randomX][randomY] == 0):  #if the spot is clean then make it dirty (value of 1 is dirty)
                self.environmentGrid[randomX][randomY] = 1
                count += 1
        
        return self.environmentGrid
        

    
    