from pathlib import Path
import frequencies
import json
import sys
import os

class InvIndex:
    #class for inverted index
    def __init__(self, indexDict={}):
        self.indexDict = indexDict        #nested dictionary {token : {doc_id : occurences}}


    #creates a inverted index from folder of domains
    def createInvIndex(self, root):
        for root, dirs, pages in os.walk(root):
            for page in pages:
                with open(page) as f:
                    jsonDict = json.load(f)
                    pageName = jsonDict['url']
                    f = frequencies.frequencies()
                    tokens = f.tokenizeFromContent(jsonDict['content'])
                    wordFrequencies = f.computeWordFrequencies(tokens)
                    for token, count in wordFrequencies.items():
                        if token not in self.indexDict.keys():
                            self.indexDict[token] = {}
                        self.indexDict[token][page] = count
                

    #retrieves number of indexed documents
    def getNumberOfDocs(self):
        pages = set()
        for doc, frequency in self.indexDict.values():
            pages.add(doc)
        return len(pages)

    #retrieves number of unique tokens indexed
    def getNumberOfUniqueTokens(self):
        return len(indexDict)

    #retrieves size of index
    def getSize(self):
        return sys.getsizeof(indexDict)

def main():
    folderPath = Path('ANALYST/')
    myInvIndex = InvIndex()
    myInvIndex.createInvIndex(folderPath)
    print("Number of Docs: " + myInvIndex.getNumberOfDocs())
    print("Number of Unique Tokens: " + myInvIndex.getNumberOfUniqueTokens())
    print("Size of Inverted Index: " + myInvIndex.getSize())
    


if __name__ == '__main__':
    main()
