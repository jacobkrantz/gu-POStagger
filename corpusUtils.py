from nltk.corpus import brown
import sys

'''
fileName: corpusUtils.py
Names:    Jacob Krantz Max Dulin
Date:     3/28/17
Description:
    classes and functions that act upon the Brown Corpus for
    the purpose of generating word sets.
CorpusUtils:
    -
'''

class CorpusUtils:

    def __init__(self):
        self.__taggedWords = []


    # builds the testing and training files using the taggedWords
    # list already built.
    # - percentTst: integer percent to train on.
    # - percentCorp: integer percent of corpus to be used.
    def buildSets(self, percentTrain, percentCorp):
        self.__taggedWords,corpSize = self.__cutLst(percentCorp)
        testSet,trainSet = self.__loadSets(percentTrain)

        self.__terminalWrite(testSet,trainSet,corpSize, percentCorp)

        self.__outputWords('./wordSets/brown_test.txt', testSet)
        self.__outputWords('./wordSets/brown_train.txt', trainSet)


    # queries the brown corpus for all tagged words.
    # returns list of tagged words in tuples.
    def getTaggedWords(self):
        self.__taggedWords = brown.tagged_words()
        return self.__taggedWords


    #----------------------------
    #      Private Functions
    #----------------------------

    # outputs the given tagged words to a specified file.
    def __outputWords(self, fileName, wordLst):
        fname = open(fileName, 'w')

        for tup in wordLst:
            word = tup[0]
            tag = tup[1]

            fname.write(word)
            fname.write(" ")
            fname.write(tag)
            fname.write("\n")


    # reduces the corpus to desired of total size
    # removes non-alphanumeric characters
    # percentCorp applies to beginning or corpus
    def __cutLst(self, percentCorp):
        trimLst = []

        for i in range(0,len(self.__taggedWords)-1):
            s = self.__taggedWords[i][0]

            if s.isalnum(): # removes all non-alphanumeric entries
                trimLst.append(self.__taggedWords[i])

        length = len(trimLst) * percentCorp / 100
        trimLst = trimLst[:length]
        return trimLst, len(trimLst)


    #build the training and test sets for HMM to use.
    #test set: first percentTrain
    #training set: remaining items
    def __loadSets(self, percentTrain):
        testSet = []
        length = len(self.__taggedWords)
        upperRange = length * percentTrain / 100

        for i in range(0,upperRange):
            word = self.__taggedWords[i][0]
            tag = self.__taggedWords[i][1]
            tup = (word,tag);
            testSet.append(tup)

        # self.__taggedWords is now the trainSet
        return testSet, self.__taggedWords[upperRange:]


    #outputs set lengths and their percentage of used corpus
    def __terminalWrite(self, testSet,trainSet,CorpSize, percentCorp):
        testLen  = len(testSet)
        trainLen = len(trainSet)

        perCorpus = str(percentCorp) + ".0%"
        perTest  = testLen / float(CorpSize)
        perTrain = trainLen / float(CorpSize)
        perTest  = "{0:.1f}".format(perTest * 100)
        perTrain = "{0:.1f}".format(perTrain * 100)

        corSizeStr = str(testLen + trainLen) + " items (" + perCorpus + ")"
        print("Size of corpus:     " + corSizeStr)
        print("Testing Set size:   " + str(testLen) + "  " + str(perTest) + "%")
        print("Training Set size:  " + str(trainLen) + "  " + str(perTrain) + "%")


if(__name__ == "__main__"):
    cu = CorpusUtils()
    cu.getTaggedWords()
    cu.buildSets(35,15)
