#Daniel Kantor
#2/8/2022
#Homework 2 - List Comprehensions
#Description - Generates lists using python list comprehensions for specific scenarios 

def main():
    catList = ["cat" for x in range(500)] 
    print(catList)
    
    countDown = [x for x in range(100, 0, -1)]
    print(countDown)
    
    hundredSquares = [[(x) * (x) for x in range(1, 101)] for y in range(0, 100)] #get the square of all the numbers between 1 and 100 and put it in a list
    print(hundredSquares)                                                        #running it 100  times and putting the resulting list in its own list   
    
    s = "Today is Monday and it is not very hot"
    wordLength = [len(x) for x in s.split()]
    print(wordLength)
    
if __name__ == "__main__":
    main()
