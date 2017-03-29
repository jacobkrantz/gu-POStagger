import numpy as np
import sys
'''
fileName: buildMatrices.py
Names:    Jacob Krantz Max Dulin
Date:     11/19/16
to run:   -requires 'brown_train.txt', generated in 'buildSets.py'
          -python2.7
Output:   -trains HMM on the input data. Outputs constructed matrices
           and cooresponding lookups
'''

#imports the training set created by buildSets.py
def getTraining():
    wordLst = []
    try:
        trainSet = open('./wordSets/brown_train.txt','r')

        for line in trainSet:
            splitLine = line.strip('\n')
            splitLine = splitLine.split(' ')
            word = splitLine[0]
            tag = splitLine[1]
            tup = (word,tag);
            wordLst.append(tup)
    except:
        print("Error: ./wordSets/brown_train.txt does not exist or is corrupt.")
        sys.exit(0)

    return wordLst


#returns number of tags used in training set
#tagDict= {[tag,#occurances],...}
def countTags(wordLst):
    tagDict = {}
    for i in wordLst:
        if i[1] in tagDict:
            tagDict[i[1]] += 1
        else:
            tagDict[i[1]] = 1
    return tagDict, len(tagDict.keys())


# converts dictionary keys into list.
# Added by greatest to least counts
def makeTagLst(tagDict):
    tagLst = []

    for i in range(0,len(tagDict)):
        largest = max(tagDict, key=tagDict.get)
        tagLst.append(largest)
        del tagDict[largest]
    return tagLst


# builds the bigram list with bigrams inserted as tuples
def makeBigramLst(wordLst):
    bigramLst = []
    for i in range(0,len(wordLst) - 1):
        tup = (wordLst[i][1],wordLst[i+1][1]);
        bigramLst.append(tup)
    return bigramLst


# adds bigrams and their respective frequencies into a dictionary
def makeBigramDict(bigramLst):
    bigramDict = {}
    for i in bigramLst:
        if i in bigramDict:
            bigramDict[i] += 1
        else:
            bigramDict[i] = 1
    return bigramDict


# computes probabilities of a tag given the previous tag
# populates matrixB with these values as floating point decimals
def insertProbA(matrixA,bigramDict,tagLst,tagDict):
    for entry in bigramDict:
        iTag = entry[0]
        jTag = entry[1]

        count  = bigramDict[entry]
        divisor = tagDict[iTag]
        probability = count / float(divisor)

        iIndex = tagLst.index(iTag) #finds index in matrix with tagLst
        jIndex = tagLst.index(jTag)

        matrixA[iIndex,jIndex] = probability

    return matrixA

# computes probabilities of a word given a tag
# populates matrixB with these values as floating point decimals
def insertProbB(matrixB,WTDict,tagDict,wordLookup,tagLst,tagProb):
    for tup in WTDict:
        tag = tup[1]
        word = tup[0]
        iIndex = tagLst.index(tag)  #finds index in matrix with lookup
        jIndex = wordLookup.index(word)

        count = WTDict[tup]
        divisor = tagDict[tag]
        probability = count / float(divisor)
        tagProbability = tagProb[tag]

        matrixB[iIndex,jIndex] = probability * tagProbability

    return matrixB


#WTDict KEY: tuple of world and its tag VALUE: #occurances
def makeWTDict(wordLst):
    WTDict = {}
    for tup in wordLst:
        if tup in WTDict:
            WTDict[tup] += 1
        else:
            WTDict[tup] = 1
    return WTDict

#returns a dictionary of the probability of a tag
#equation: tagProb = count(tag) / count(all tags)
def makeTagProb(tagDict):
    tagProb = {}
    totCount = 0
    for i in tagDict:
        totCount += tagDict[i]
    for i in tagDict:
        tagProb[i] = tagDict[i] / float(totCount)
    return tagProb

#adds unique words to a list. used as a lookup for word positions in matrices
def makeWordLookup(wordLst):
    wordLookup = []
    for tup in wordLst:
        if tup[0] not in wordLookup:
            wordLookup.append(tup[0])
    return wordLookup

# outputs a list to a file
def printLookup(fileName,lst):
    lookup = open(fileName,'w')
    for item in lst:
        lookup.write(item)
        lookup.write('\n')
    lookup.close()
    return

# outputs a dictionary to a file
def printTagProb(fileName,tagProb):
    tagFile = open(fileName,'w')
    for item in tagProb:
        tagFile.write(item)
        tagFile.write(' ')
        tagFile.write(str(tagProb[item]))
        tagFile.write('\n')
    tagFile.close()
    return


# MatrixA: transition probabilities moving from i tag to j tag.
#          indeces of matrix determined by tagLst.
def buildA(wordLst,tagCount,tagDict,tagLst):
    matrixA = np.zeros((tagCount,tagCount), dtype=np.float) # inititalzie matrix A
    bigramLst  = makeBigramLst(wordLst)
    bigramDict = makeBigramDict(bigramLst)
    matrixA = insertProbA(matrixA,bigramDict,tagLst,tagDict)

    np.savetxt("./wordSets/matrixA.txt",matrixA, newline = '\n', fmt = '%.10f')

    return matrixA


#tagLst:  lookup for i index. wordLst: lookup for j index
#matrixB: probability of a word given a tag. (tag i, word j)
def buildB(wordLookup,tagCount,tagDict,tagLst,WTDict,tagProb):
    i = tagCount
    j = len(wordLookup)
    matrixB = np.zeros((i,j), dtype=np.float) # initialize matrix B

    matrixB = insertProbB(matrixB,WTDict,tagDict,wordLookup,tagLst,tagProb)

    np.savetxt("./wordSets/matrixB.txt",matrixB, newline = '\n', fmt = '%.10f')

    return matrixB

def main():
    wordLst = getTraining()

    tagDict, tagCount = countTags(wordLst)
    tagLst = makeTagLst(tagDict.copy())
    WTDict = makeWTDict(wordLst)
    tagProb = makeTagProb(tagDict)

    wordLookup = makeWordLookup(wordLst)

    printLookup("./wordSets/tagLookup.txt",tagLst)
    printLookup("./wordSets/wordLookup.txt",wordLookup)
    printTagProb("./wordSets/tagProb.txt",tagProb)

    matrixA = buildA(wordLst,tagCount,tagDict,tagLst)
    matrixB = buildB(wordLookup,tagCount,tagDict,tagLst,WTDict,tagProb)

    print("Unique number of tags:  " + str(len(tagLst)))
    print("Unique number of words: " + str(len(wordLookup)))

main()
