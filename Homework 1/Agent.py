import random

class Agent:
    
    def __init__(self, name, age, locationX, locationY):
        self.name = name
        self.__age = age
        self.__locationX = locationX
        self.__locationY = locationY
        
    def setName(self, name):
        self.name = name
        
    def getName(self):
        return self.name
    
    def MoveLocationRandom(self):
        self.__locationX = self.__locationX + random.randint(1,100)
        print("New Location X (Random): " + str(self.__locationX))
        
    def MoveLocationSouth(self):
        self.__locationY = self.__locationY - 10
        print("New Location Y (South): " + str(self.__locationY))
        
    def MoveLocationBasedOnAge(self):
        if self.__age > 10:
            self.__locationX = self.__locationX + self.__age
            print("New Location X (Age): " + str(self.__locationX))
        else:
            self.__locationY = self.__locationY + self.__age
            print("New Location Y (Age): " + str(self.__locationY))
