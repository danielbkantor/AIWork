#Daniel Kantor
#5/6/2022
#Final Project
#A program that will crawl the muhlenberg domain saving the HTML contents of each website to a file. The contents of each file
#is then cleaned by removing all the HTML tags, taking only the words removing all special characters and putting them in lowercase
#these words for each file is then stored in a clean file and from all of these files an inverted index is created
#there is also options to remove stopwords and lemmatize words when cleaning the text and then creating the inverted index

import requests
import re
import os
import json
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

removeStopWords = False #change values to make the inverted index associated with choices
lemmatizeWords = False
stopWords = set(stopwords.words('english'))

if not os.path.exists("rawFiles" ): #make the folders if they don't already exist
    os.makedirs("rawFiles")
    
if not os.path.exists("cleanFiles" ):
    os.makedirs("cleanFiles" )

#Method to web crawl. will go to each url get all the urls in its HTML and add them to the stack of URLS. 
#it will also save the HTML contents of the website to a file to be later cleaned and used. at the end calls
#the method to clean the files
# @return none
# @ param
def main():

    urlStack = ["http://www.muhlenberg.edu/"] #stack of urls to visit
    seenUrls = ["http://www.muhlenberg.edu/"] #list of urls that have been visited
    baseUrl = "http://www.muhlenberg.edu/" #base url to append to relative links
    numUrlsVisited = 0
    
    while numUrlsVisited < 10000: #run until 10000 pages have been crawled
        if urlStack: #make sure the is something in the stack
            newUrl = urlStack.pop() #take a new link 
        else:
            break
        if "http://" not in newUrl and "https://" not in newUrl: #fix the url if it doesnt have http
            newUrl = "http://" + newUrl
        try:
            r = requests.get(newUrl) #get the html from that link
        except requests.exceptions.ConnectionError: #make sure the URL works
            r.status_code = "Connection refused"
        except requests.exceptions.InvalidSchema:
            r.status_code = "Connection refused"
        if r.status_code == 200: #make sure the link is valid
            textWebsite = r.text #convert the html into parseable text
            urls = re.findall("href=['|\"]([^'|\"]*)", textWebsite) #find all the valid links in the html by looking for href= tags followed by and opening " or ' 
            for url in urls:                                        #and then all possible characters until a closing " ' is found
                if url: 
                    if url[0] == "/": #check if the url is a relative link
                        modifyUrl = baseUrl + url[1::] #add the base url to the relative link
                        if "#" in url: #if the url is a jump point on the page, remove the jump point to get the rest of the url 
                            modifyUrl = modifyUrl.split("#")[0]
                        if ".svg" not in modifyUrl and ".png" not in modifyUrl and ".css" not in modifyUrl and ".ico" not in modifyUrl and ".pdf" not in modifyUrl and ".xls" not in modifyUrl: #make sure the url leads to an html page
                            if modifyUrl not in seenUrls: #if the url hasnt been visited yet then append it to the stack 
                                urlStack.append(modifyUrl)
                                seenUrls.append(modifyUrl) #add the new url to the list of seen urls
                    else: #if the url is an absolute link
                        if "www.muhlenberg.edu" in url: #check that the url leads to the muhlenberg website
                            if "#" in url: #if the url is a jump point on the page, remove the jump point to get the rest of the url 
                                url = url.split("#")[0]
                            if ".svg" not in url and ".png" not in url and ".css" not in url and ".ico" not in url and ".pdf" not in url and ".xls" not in url: #make sure the url leads to an html page
                                if url not in seenUrls: #if the url hasnt been visited yet then append it to the stack 
                                    urlStack.append(url)
                                    seenUrls.append(url) #add the new url to the list of seen urls 
                                                       
            with open(os.path.join("rawFiles" , "rawDoc" + str(numUrlsVisited) +".txt"), "w", errors= "ignore") as f: #write the information found at the url to its own file
                f.write("URL: " + newUrl + "\n")
                f.write(r.text)
             
        numUrlsVisited += 1
    
    print("The crawling has finished!")
    print("The number of pages retrieved: " + str(numUrlsVisited))
    
    cleanFiles()

#A method to clean the contents of the rawfiles. It iterates through all the files in the rawFiles folder removes all the HTML, CSS, and JS 
#and extracts all the words. The words extracted are t hen put into lowercase and all special characters are removed and the words are saved 
#in a clean file associated with the raw file is came from
# @return none
# @param none
def cleanFiles():
    for filename in os.listdir("rawFiles"):  #go through all the raw files
        f = os.path.join("rawFiles", filename)
        numFile = re.findall("\d+", f)[0] #find the digit in the raw file name to use in the clean file
        with open(f, errors = "ignore") as openFile:
            contents = openFile.read()
            cleanContents = BeautifulSoup(contents, 'lxml') #remove all the non text tags
            with open(os.path.join("cleanFiles", "clean" + numFile +".txt"), "w", errors= "ignore") as f: 
                spaceContentWords = " ".join(cleanContents.text.split()) #get each word individually
                f.write(spaceContentWords.split()[0] + " "  + spaceContentWords.split()[1] + "\n") #save the URL individually
                for word in spaceContentWords.split()[2:]: #go through all the other words in the file and remove all special characters, make it lowercase and save it to the clean file
                    wordRemovedSpecialChar = re.sub("[^a-zA-Z0-9']+", '' , word)
                    f.write(wordRemovedSpecialChar.lower() + "\n") 
                         
    createInvertedIndex()

#A method to create the inverted index. It first gets the website in each clean file and adds that to a list of websites 
#then iterating through all the cleaned files, depending on which optimizations are selected it will create an inverted index
#associated with those options. The inverted index is then written to a json file along with a json file containing 
#all the maximum frequencies of a word in each file
# @param
# @return none                           
def createInvertedIndex():
    invertedIndex = {}
    lemmatizer = WordNetLemmatizer()
    websiteList = list()

    for filename in os.listdir("cleanFiles"): #iterate through all the clean files
        f = os.path.join("cleanFiles", filename)
        numFile = re.findall("\d+", f)[0] #find the digit in the clean file name to use in the inverted index
        with open(f, errors = "ignore") as openFile:
            websiteList.append(next(openFile)[5:].replace("\n", "")) #add the website url in the file to the list 
            for line in openFile: #go through all the words in the each file
                for word in line.split():
                    if lemmatizeWords and removeStopWords: 
                        if word not in stopWords: #check if the word is a stopword, if it is ignore it 
                            lemmatizeWord = lemmatizer.lemmatize(word) #lemmatize the word
                            if lemmatizeWord not in invertedIndex: #check if the word is already in the index
                                invertedIndex[lemmatizeWord] = [[numFile, 1]] #if the word isn't in the index, add it with the doc num and count of 1
                            else:
                                numFlag = False
                                for i in invertedIndex[lemmatizeWord]: #check if the word assocoiated with a specific doc num is in the index
                                    if i[0] == numFile:                 #if it is add one to its count
                                        i[1] = i[1] + 1
                                        numFlag = True
                                if numFlag == False:    #if the word associated with a specific doc num isn't in the index add it with a count of 1
                                    invertedIndex[lemmatizeWord].append([numFile, 1])  
                    elif lemmatizeWords:
                        lemmatizeWord = lemmatizer.lemmatize(word)  #lemmatize the word
                        if lemmatizeWord not in invertedIndex: #check if the word is already in the index
                            invertedIndex[lemmatizeWord] = [[numFile, 1]] #if the word isn't in the index, add it with the doc num and count of 1
                        else:
                            numFlag = False
                            for i in invertedIndex[lemmatizeWord]: #check if the word assocoiated with a specific doc num is in the index
                                if i[0] == numFile:                 #if it is add one to its count
                                    i[1] = i[1] + 1
                                    numFlag = True
                            if numFlag == False:    #if the word associated with a specific doc num isn't in the index add it with a count of 1
                                invertedIndex[lemmatizeWord].append([numFile, 1]) 
                    elif removeStopWords:
                        if word not in stopWords: #check if the word is a stopword, if it is ignore it 
                            if word not in invertedIndex:  #check if the word is already in the index
                                invertedIndex[word] = [[numFile, 1]] #if the word isn't in the index, add it with the doc num and count of 1
                            else:
                                numFlag = False
                                for i in invertedIndex[word]: #check if the word assocoiated with a specific doc num is in the index
                                    if i[0] == numFile:         #if it is add one to its count
                                        i[1] = i[1] + 1
                                        numFlag = True
                                if numFlag == False:  #if the word associated with a specific doc num isn't in the index add it with a count of 1
                                    invertedIndex[word].append([numFile, 1])  
                    else:
                        if word not in invertedIndex: #check if the word is already in the index
                            invertedIndex[word] = [[numFile, 1]] #if the word isn't in the index, add it with the doc num and count of 1
                        else:
                            numFlag = False
                            for i in invertedIndex[word]: #check if the word assocoiated with a specific doc num is in the index
                                if i[0] == numFile:         #if it is add one to its count
                                    i[1] = i[1] + 1
                                    numFlag = True
                            if numFlag == False:   #if the word associated with a specific doc num isn't in the index add it with a count of 1
                                invertedIndex[word].append([numFile, 1])                       
    
    #Code used to write the max frequency and inverted index dictonaries to a json file depending on which
    #optimazation are being utilized
    if lemmatizeWords and removeStopWords:
        maxFreqDict = getMaxFreq(invertedIndex)
        with open("bothMaxFreq.json", "w") as outfile:
            json.dump(maxFreqDict, outfile, indent=4)
        with open("bothInvertedIndex.json", "w") as outfile:
            json.dump(invertedIndex, outfile, indent=4)
    
    elif lemmatizeWords:
        maxFreqDict = getMaxFreq(invertedIndex)
        with open("lemmatizeMaxFreq.json", "w") as outfile:
            json.dump(maxFreqDict, outfile, indent=4)
        with open("lemmatizeInvertedIndex.json", "w") as outfile:
            json.dump(invertedIndex, outfile, indent=4)
            
    elif removeStopWords:
        maxFreqDict = getMaxFreq(invertedIndex)
        with open("stopWordsMaxFreq.json", "w") as outfile:
            json.dump(maxFreqDict, outfile, indent=4)
        with open("stopWordsInvertedIndex.json", "w") as outfile:
            json.dump(invertedIndex, outfile, indent=4)

    else:
        maxFreqDict = getMaxFreq(invertedIndex)
        with open("baseMaxFreq.json", "w") as outfile:
            json.dump(maxFreqDict, outfile, indent=4)
        with open("baseInvertedIndex.json", "w") as outfile:
            json.dump(invertedIndex, outfile, indent=4)
    
    with open("websiteList.txt", "w") as outfile: #write the list of websites to a text file
        for website in websiteList:
            outfile.write(website + "\n")

#get the max frequency of a word for each document
# @param invertedIndex - the index used to iterate through the find all the max frequencies
# @return maxFreq - the dictionary containing the max frequencies associated with each document 
def getMaxFreq(invertedIndex):
    maxFreq = dict()
    for i in invertedIndex.values(): #go through all the values in the inverted index
        for j in i: #iterate through all the lists associated with a given word
            if j[0] not in maxFreq: #if the doc doesn't have a max frequency yet, set it to the frequency of the word you are at
                maxFreq[j[0]] = j[1]
            elif maxFreq[j[0]] < j[1]: #if the doc does have a max frequency, if the one currently set it lower than change it to the higher value
                maxFreq[j[0]] = j[1]
                
    return maxFreq
                          
main()  
