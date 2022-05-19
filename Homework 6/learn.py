import os   
import json
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()


#Variables to turn on and off option to remove stopwords and lemmatization
removeStopwords = False
lemmatization = False

def main():
    hamDict = {}
    spamDict = {}

    directory = "enron1\ham"
    directoryTwo = "enron1\spam"
    spamCount = 0
    hamCount = 0
    dictCount = 0
    numSpamFiles = 0
    numHamFiles = 0
    stopWords = set(stopwords.words('english'))

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        with open(f, "r") as openFile:
            for line in openFile:
                for word in line.split():
                    if removeStopwords and lemmatization:
                        if word.lower() not in stopWords:
                            newWord = lemmatizer.lemmatize(word)
                            if newWord not in hamDict and newWord not in spamDict:
                                dictCount += 1
                            hamDict[newWord] = hamDict.get(newWord, 0) + 1
                            hamCount += 1   
                    elif removeStopwords:
                        if word.lower() not in stopWords:
                            if word not in hamDict and word not in spamDict:
                                dictCount += 1
                            hamDict[word] = hamDict.get(word, 0) + 1
                            hamCount += 1
                    elif lemmatization:
                        newWord = lemmatizer.lemmatize(word)
                        if newWord not in hamDict and newWord not in spamDict:
                            dictCount += 1
                        hamDict[newWord] = hamDict.get(newWord, 0) + 1
                        hamCount += 1

                    else:
                        if word not in hamDict and word not in spamDict:
                            dictCount += 1
                        hamDict[word] = hamDict.get(word, 0) + 1
                        hamCount += 1
        numHamFiles += 1


    for filename in os.listdir(directoryTwo):
        f = os.path.join(directoryTwo, filename)
        with open(f, errors = "ignore") as openFile:
            for line in openFile:
                for word in line.split():
                    if removeStopwords and lemmatization:
                        if word.lower() not in stopWords:
                            newWord = lemmatizer.lemmatize(word)
                            if newWord not in hamDict and newWord not in spamDict:
                                dictCount += 1  
                            spamDict[newWord] = spamDict.get(newWord, 0) + 1
                            spamCount += 1
                    elif removeStopwords:
                        if word.lower() not in stopWords:
                            if word not in hamDict and word not in spamDict:
                                dictCount += 1  
                            spamDict[word] = spamDict.get(word, 0) + 1
                            spamCount += 1
                    elif lemmatization:
                        newWord = lemmatizer.lemmatize(word)
                        if newWord not in hamDict and newWord not in spamDict:
                            dictCount += 1
                        spamDict[newWord] = spamDict.get(newWord, 0) + 1
                        spamCount += 1
                    else:
                        if word not in hamDict and word not in spamDict:
                            dictCount += 1  
                        spamDict[word] = spamDict.get(word, 0) + 1
                        spamCount += 1

        numSpamFiles += 1
           
    wordList = [hamDict, spamDict]


    with open("knowledge.json", "w") as write_file:
        json.dump(wordList, write_file, indent=4)

    with open("info.txt", "w") as f:
        f.write(str(hamCount) + "\n")
        f.write(str(spamCount) + "\n")
        f.write(str(dictCount) + "\n")
        f.write(str(numHamFiles) + "\n")
        f.write(str(numSpamFiles))

if __name__ == "__main__":
    main()
