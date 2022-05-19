from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import json
import math
import os


messageCounter = 1
lemmatizer = WordNetLemmatizer()
removeStopwords = False
lemmatization = False
   
def main():
    global messageCounter
    displayMessages = False
    directories = [["enron2\ham", "enron2\spam"], ["enron3\ham", "enron3\spam"]]

    for i in directories:
        messageCounter = 1
        results = []
        for j in i:
            results.extend(checkDirectories(j, displayMessages))
              
        print(results)
                
        accuracy = (results[0] + results[3]) / sum(results)
        precision = results[3] / (results[3] + results[1])
        recall = results[3] / (results[3] + results[2])

        print(accuracy, precision, recall)

def getInfo():
    f = open("knowledge.json")
    f2 = open("info.txt")
    data = json.load(f) 
    hamDict = data[0]
    spamDict = data[1]
    counts = []
    for line in f2:
        counts.append(int(line.strip('\n')))
    print(counts)
    probFileHam = math.log(counts[3]/(counts[3] + counts[4]))
    probFileSpam = math.log(counts[4]/(counts[3] + counts[4]))   

    return hamDict, spamDict, probFileHam, probFileSpam, counts 

def checkDirectories(directory, displayMessages):
    stopWords = set(stopwords.words('english'))
    global messageCounter
    info = getInfo()
    
    print(info)

    hamDict = info[0]
    spamDict = info[1]
    probFileHam = info[2]
    probFileSpam = info[3]
    counts = info[4]
    
    truePositive = 0
    falsePositive = 0 
    falseNegative = 0
    trueNegative = 0

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        with open(f, errors = "ignore"  ) as openFile:
            hamProb = 0
            spamProb = 0
            for line in openFile:
                for word in line.split():
                    if removeStopwords and lemmatization:
                        if word.lower() not in stopWords:
                            newWord = lemmatizer.lemmatize(word)
                            wordHamProb = math.log((hamDict.get(newWord, 0) + 1)/(counts[0] + counts[2]))
                            wordSpamProb = math.log((spamDict.get(newWord, 0) + 1)/(counts[1] + counts[2]))
                            hamProb += wordHamProb
                            spamProb += wordSpamProb
                    elif removeStopwords:
                        if word.lower() not in stopWords:
                            wordHamProb = math.log((hamDict.get(word, 0) + 1)/(counts[0] + counts[2]))
                            wordSpamProb = math.log((spamDict.get(word, 0) + 1)/(counts[1] + counts[2]))
                            hamProb += wordHamProb
                            spamProb += wordSpamProb
                    elif lemmatization:
                        newWord = lemmatizer.lemmatize(word)
                        wordHamProb = math.log((hamDict.get(newWord, 0) + 1)/(counts[0] + counts[2]))
                        wordSpamProb = math.log((spamDict.get(newWord, 0) + 1)/(counts[1] + counts[2]))
                        hamProb += wordHamProb
                        spamProb += wordSpamProb
                    else:
                        wordHamProb = math.log((hamDict.get(word, 0) + 1)/(counts[0] + counts[2]))
                        wordSpamProb = math.log((spamDict.get(word, 0) + 1)/(counts[1] + counts[2]))
                        hamProb += wordHamProb
                        spamProb += wordSpamProb
            hamProb += probFileHam
            spamProb += probFileSpam
            
            if "ham" in directory:
                if hamProb > spamProb:
                    if displayMessages:
                        print("Message " + str(messageCounter) + ": Ham. Real: Ham" )
                    trueNegative += 1
                else:
                    if displayMessages:
                        print("Message " + str(messageCounter) + ": Spam. Real: Ham" )
                    falsePositive += 1
            else:
                if hamProb > spamProb:
                    if displayMessages:
                        print("Message " + str(messageCounter) + ": Ham. Real: Spam" )
                    falseNegative += 1
                else:
                    if displayMessages:
                        print("Message " + str(messageCounter) + ": Spam. Real: Spam" )
                    truePositive += 1

            messageCounter += 1
    
    if "ham" in directory:
        return trueNegative, falsePositive
    else:
        return falseNegative, truePositive


if __name__ == "__main__":
    main()