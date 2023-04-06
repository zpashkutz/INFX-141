import re
from bs4 import BeautifulSoup
import scraper

class frequencies:
    '''
    Class to tokenize and calculate word frequencies from a file
    '''
    def __init__(self):     #initialize token list and frequencies dictionary
        self.tokens = []
        self.Frequencies = {}
    
    #O(n) runtime complexity. Runtime increases as files get larger
    def tokenizeFromFile(self, TextFilePath:str) -> list:   #takes a list
        try:
            file = open(TextFilePath, "r", encoding='utf-8')
        except Exception:
            print("Invalid file input")
            exit()
        for line in file:                               #iterate through each line in the file
            line = re.split(r"[-;,.\"\s]\s*", line)     #separate the words in each line 
            for word in line:                           #iterate through words in a line
                if re.fullmatch(r"\w+", word):          #if the word is alphanumeric
                    word = word.lower()                 #convert all characters in word to lower case
                    self.tokens.append(word)            #add word to list of tokens                
        return self.tokens
    
    def tokenizeFromContent(self, content) -> list:
        html_content = BeautifulSoup(content, 'html.parser')    #read html from content
        return scraper.get_words(html_content)

    #O(n) runtime complexity. Runtime increases as the amount of tokens increases
    def computeWordFrequencies(self, Tokens:list) -> dict:  #takes list of tokens and creates dictionary that has count of occurrences
        for token in Tokens:                                #iterate through list of tokens
            if token in self.Frequencies.keys():            #if the token is already in the dictionary
                self.Frequencies[token] += 1                     #increase the count by 1
            else:                                               
                self.Frequencies[token] = 1                 #otherwise add that token to the dictionary and set count to 1
        return self.Frequencies
    
    #O(n) runtime complexity. The more tokens there are, the longer it will take
    def getFreqs(self, Frequencies:dict):      #prints tokens and their frequencies
        freqs = []
        for word, count in sorted(Frequencies.items(), key=lambda token: token[1], reverse=True):
            if len(freqs) < 50:
                freqs.append(word + " - " + str(count))
            else:
                break
        return freqs
        
    #O(n) runtime complexity. The larger the lists of tokens, the longer it will take.  
    def compareFiles(self,  tokens1:list, tokens2:list) -> int:    #returns number of words in common
        inCommon = []
        for word in tokens1:
            if word in tokens2:
                inCommon.append(word)
        for word in inCommon:
            print(word)
        return len(inCommon)
    
def main():
    file1 = input("Input file name: ")
    f = frequencies()
    tokens1 = f.tokenize(file1)
    tokenDict = f.computeWordFrequencies(tokens1)
    f.printFreq(tokenDict)
    
if __name__ == "__main__":
    main()
