#Daniel Kantor 
#4/20/2022
#Homework 7
#A program that will crawl the muhlenberg.edu website and sotore the contents of 500 pages that have been crawled in 
#thier own txt files. Each file stores the URL of the page, number of relative links found on the page, the number of absolute links 
#found on the page and the contents of the HTML file

import requests
import re

def main():

    urlStack = ["http://www.muhlenberg.edu/"] #stack of urls to visit
    seenUrls = ["http://www.muhlenberg.edu/"] #list of urls that have been visited
    baseUrl = "http://www.muhlenberg.edu/" #base url to append to relative links
    numUrlsVisited = 0
    totalRelative = 0
    totalAbsolute = 0
    
    while numUrlsVisited < 500: #run until 500 pages have been crawled
        newUrl = urlStack.pop() #take a new link 
        relativeUrl = 0
        absoluteUrl = 0
        r = requests.get(newUrl) #get the html from that link
        if r.status_code == 200: #make sure the link is valid
            textWebsite = r.text #convert the html into parseable text
            urls = re.findall("href=['|\"]([^'|\"]*)", textWebsite) #find all the valid links in the html by looking for href= tags followed by and opening " or ' 
            for url in urls:                                        #and then all possible characters until a closing " ' is found
                if url: 
                    if url[0] == "/": #check if the url is a relative link
                        relativeUrl += 1
                        totalRelative += 1
                        modifyUrl = baseUrl + url[1::] #add the base url to the relative link
                        if "#" in url: #if the url is a jump point on the page, remove the jump point to get the rest of the url 
                            modifyUrl = modifyUrl.split("#")[0]
                        if ".svg" not in modifyUrl and ".png" not in modifyUrl and ".css" not in modifyUrl and ".ico" not in modifyUrl and ".pdf" not in modifyUrl and ".xls" not in modifyUrl: #make sure the url leads to an html page
                            if modifyUrl not in seenUrls: #if the url hasnt been visited yet then append it to the stack 
                                urlStack.append(modifyUrl)
                                seenUrls.append(modifyUrl) #add the new url to the list of seen urls
                    else: #if the url is an absolute link
                        absoluteUrl += 1
                        totalAbsolute += 1
                        if "www.muhlenberg.edu" in url: #check that the url leads to the muhlenberg website
                            if "#" in url: #if the url is a jump point on the page, remove the jump point to get the rest of the url 
                                url = url.split("#")[0]
                            if ".svg" not in url and ".png" not in url and ".css" not in url and ".ico" not in url and ".pdf" not in url and ".xls" not in url: #make sure the url leads to an html page
                                if url not in seenUrls: #if the url hasnt been visited yet then append it to the stack 
                                    urlStack.append(url)
                                    seenUrls.append(url) #add the new url to the list of seen urls 
                                    
            with open(str(numUrlsVisited) +".txt", "w", errors= "ignore") as f: #write the information found at the url to its own file
                f.write("URL: " + newUrl + "\n")
                f.write("Number of relative URLs: " + str(relativeUrl) + "\n")
                f.write("Number of relative URLs: " + str(absoluteUrl) + "\n")
                f.write("HTML:" + "\n")
                f.write(r.text)
             
        numUrlsVisited += 1
    
    print("The crawling has finished!")
    print("The number of pages retrieved: " + str(numUrlsVisited))
    print("Number of relative URLS: " + str(totalRelative))
    print("Number of absolute URLS: " + str(totalAbsolute))
    print("Total URLS found: " + str(totalRelative + totalAbsolute))

    
    
main()  