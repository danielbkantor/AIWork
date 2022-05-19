#Daniel Kantor
#5/6/2022
#Final Project
#Program used to take in a query and using the information in inverted index json files and maximum frequency json file
# will calculate the how relevant each document is to the query that the user enters. The top 10 more relevant documents 
# will have their website links printed to the terminal
import json
import math
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re

removeStopWords = False 
lemmatizeWords = False
stopWords = set(stopwords.words('english'))

#Method for the user to input their query and what optimizations they want. The json files associated with the selected
#optimizations are then stored in a dictionary and the method to calculate weights is called and finally using the weights
#the method to determine the top 10 websites associated with the top 10 weights is called
# @param none
# @return none
def main():
     
    testQuery = input("Please enter your query: ") #user input query
    removeStopWords = get_bool("Do you want to remove stopwords? Enter True or False: ") #user input whether they want optimizations
    lemmatizeWords = get_bool("Do you want to use lemmatazation? Enter True or False: ")  
    finalWeights = dict()
    
    #depending on which optimizations the user selects different json files will be loaded and stored in a dictionary
    #then the calculateWeights function is called with the loaded files to calculate the weights to determine relevancy
    
    if removeStopWords and lemmatizeWords:
        with open("bothInvertedIndex.json") as file:
            invertedIndex = json.load(file)
        with open("bothMaxFreq.json") as file:
            maxFreq = json.load(file)
        
        finalWeights = calculateWeights(maxFreq, invertedIndex, testQuery)
            
    elif removeStopWords:
        with open("stopWordsInvertedIndex.json") as file:
            invertedIndex = json.load(file)
        with open("stopWordsMaxFreq.json") as file:
            maxFreq = json.load(file)
            
        finalWeights = calculateWeights(maxFreq, invertedIndex, testQuery)
            
    elif lemmatizeWords:
        with open("lemmatizeInvertedIndex.json") as file:
            invertedIndex = json.load(file)
        with open("lemmatizeMaxFreq.json") as file:
            maxFreq = json.load(file)

        finalWeights = calculateWeights(maxFreq, invertedIndex, testQuery)
        
    else:
        with open("baseInvertedIndex.json") as file:
            invertedIndex = json.load(file)
        with open("baseMaxFreq.json") as file:
            maxFreq = json.load(file)

        finalWeights = calculateWeights(maxFreq, invertedIndex, testQuery)
            
    getWebsites(finalWeights)

#Method used to calculate the weights of the query against all the documents 
# @param maxFreq - the dictionary containing the max frequencies associated with each document 
# @ param invertedIndex - the dictionary containing the counts of each word in each document
# @ return finalWeights - the dictionary containing the weights associated with each document
def calculateWeights(maxFreq, invertedIndex, testQuery):
    numerator = dict()      
    denominator = dict()
    finalWeights = dict()
    queryInvertedIndex = createQueryInvertedIndex(testQuery)
 
    numDocs = len(maxFreq)  #number of documents
    for word in testQuery.split(): #for each word in the query
        queryWordTF = queryInvertedIndex[word]/max(queryInvertedIndex.values()) #calculate the tf for the query
        if word in invertedIndex: #check if the word in the query is in the index
            numOccurences = len(invertedIndex[word]) #number of times a word appears in documents
            if "q" not in denominator: #if its the first word in the query 
                if math.log(numDocs/numOccurences) == 0: #if numDocs/numOccurences is 1 don't log
                    denominator["q"] = (queryWordTF + (numDocs/numOccurences)) ** 2 #
                else: #calculate denominator value for the query
                    denominator["q"] = (queryWordTF + math.log((numDocs/numOccurences))) ** 2
            else:
                if math.log(numDocs/numOccurences) == 0: #if numDocs/numOccurences is 1 don't log
                    denominator["q"] += (queryWordTF + (numDocs/numOccurences)) ** 2
                else:  #calculate denominator value for the query
                    denominator["q"] += (queryWordTF + math.log((numDocs/numOccurences))) ** 2
            for j in invertedIndex[word]:  #iterate through all the counts of the word that are associated with a document that are saved in the inverted index
                if j[0] not in numerator: #if the doc isnt in the dictionary yet
                    if math.log(numDocs/numOccurences) == 0: #if numDocs/numOccurences is 1 don't log
                        numerator[j[0]] = (j[1]/maxFreq[str(j[0])]) * (numDocs/numOccurences)
                    else: #calculate numerator value for the doc
                        numerator[j[0]] = (j[1]/maxFreq[str(j[0])]) * math.log((numDocs/numOccurences))
                else: #if the doc is already in the dictionary
                    if math.log(numDocs/numOccurences) == 0:  #if numDocs/numOccurences is 1 don't log
                        numerator[j[0]] += (j[1]/maxFreq[str(j[0])]) * (numDocs/numOccurences)
                    else: #calculate numerator value for the doc
                        numerator[j[0]] += (j[1]/maxFreq[str(j[0])]) * math.log((numDocs/numOccurences))
                if j[0] not in denominator: #if the doc isnt in the dictionary yet
                    if math.log(numDocs/numOccurences) == 0: #if numDocs/numOccurences is 1 don't log
                        denominator[j[0]] = (j[1]/maxFreq[str(j[0])]) * (numDocs/numOccurences) ** 2
                    else: #calculate denominator value for the doc
                        denominator[j[0]] = (j[1]/maxFreq[str(j[0])]) * math.log((numDocs/numOccurences)) ** 2
                else: #if the doc is already in the dictionary
                    if math.log(numDocs/numOccurences) == 0: #if numDocs/numOccurences is 1 don't log
                        denominator[j[0]] += (j[1]/maxFreq[str(j[0])]) * (numDocs/numOccurences) ** 2
                    else: #calculate denominator value for the doc
                        denominator[j[0]] += (j[1]/maxFreq[str(j[0])]) * math.log((numDocs/numOccurences)) ** 2
    
    for i in numerator: #calculate the final weights for each document using the values stored for the numerator and denominator
        finalWeights[i] = numerator[i] / (math.sqrt(denominator[i]) * math.sqrt(denominator["q"]))
    
    return finalWeights

#Method to create the inverted index for the test query to be used to calculate weights
# @param testQuery - the query to use to create the inverted index
# @ return queryInvertedIndex - the inverted index associated with the query
def createQueryInvertedIndex(testQuery):
    lemmatizer = WordNetLemmatizer()
    queryInvertedIndex = dict()
    for word in testQuery.split(): #iterate through all the words in the query
        word = re.sub("[^a-zA-Z0-9']+", '' , word) #process the query to remove special characters and make it lowercase
        word = word.lower()
        print(word)
        #if statements so that depending on which optimizations are selected the inverted index will be created using those optimizations
        if lemmatizeWords and removeStopWords:
            if word not in stopWords:
                lemmatizeWord = lemmatizer.lemmatize(word)
                if lemmatizeWord not in queryInvertedIndex:
                    queryInvertedIndex[lemmatizeWord] = 1
                else:
                    queryInvertedIndex[lemmatizeWord] += 1
        if lemmatizeWords:
            lemmatizeWord = lemmatizer.lemmatize(word)
            if lemmatizeWord not in queryInvertedIndex:
                queryInvertedIndex[lemmatizeWord] = 1
            else:
                queryInvertedIndex[lemmatizeWord] += 1
        elif removeStopWords:
             if word not in stopWords:
                if word not in queryInvertedIndex:
                    queryInvertedIndex[word] = 1
                else:
                    queryInvertedIndex[word] += 1
        else:
            if word not in queryInvertedIndex:
                queryInvertedIndex[word] = 1
            else:
               queryInvertedIndex[word] += 1
               
    return queryInvertedIndex

# Method that uses the final weights, sorts all the weights and then using the keys of the sorted weights
# gets the top 10 most relevant websites associated with the keys and prints them to the screen
# @param finalWeights - the dictonary contianing the weights
# @return none
def getWebsites(finalWeights):
    sortedWeights = dict(sorted(finalWeights.items(), key = lambda item: item[1], reverse= True)) #sort the dictionary of weights in descending order
    
    lenDict = len(sortedWeights)
    counter = 0
    file = open("websiteList.txt", "r") #open the text file of websites and save it in a list
    websiteList = file.readlines()
    websiteList = ' '.join(websiteList).split()
    
    counter = 0
    if lenDict < 10: #if theres less than 10 relevant websites
        for i in sortedWeights: #iterate through the dictionary
            print("Website Rank #" + str(counter + 1) + " : " + websiteList[int(i)]) #print the website associated with the key in the sorted dictionary
            counter += 1
    else:
        for i in sortedWeights: #iterate through the dictionary
            if counter == 10: #stop when 10 websites have been printed
                break
            else:
                print("Website Rank #" + str(counter + 1) + " : " + websiteList[int(i)])  #print the website associated with the key in the sorted dictionary
                counter += 1
    
# Method used to make sure the user enter true or false when selecting their optimzations
# returning a boolean value associated with the user input    
# @param prompt - string of what the user is being asked to input
# @ return True or False
def get_bool(prompt):
    while True: #run until return
        try:
           return {"true":True,"false":False}[input(prompt).lower()] #return True/False if its a valid input
        except KeyError:
           print("Invalid input please enter True or False!") 

main()

