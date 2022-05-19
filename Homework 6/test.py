import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

 
example_sent = """This is a sample sentence showing off the stop words filtration corpora """
 
stop_words = set(stopwords.words('english'))

 
for word in example_sent.split(" "):
    print(lemmatizer.lemmatize(word))


for filename in os.listdir("enron1\ham"):
    f = os.path.join("enron1\ham", filename)
    with open(f, "r") as openFile:
        for line in openFile:
            for word in line.split():
                #print(lemmatizer.lemmatize(word))
                pass



    
