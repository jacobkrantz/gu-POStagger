
'''
Author: Max Dulin
Date Made: April 19th
Date Last edited: April 21st
Language: Written in Python 2.7

The program compares two files for the tag similarites
Run compareSentences to do this.


To compile type "python Compare.py" into the terminal
'''

class Compare:

    def __init__(self):
        self.__testFile = "./wordSets/brown_test.txt"
        self.__fileMade = "./wordSets/POStagged.txt"
        self.testString = self.__getFile(self.__testFile)
        self.madeString = self.__getFile(self.__fileMade)
        self.count = 0
        self.wrong = 0
        self.correct = 0

        self.wrongLst = []
        self.correctLst = []
        #print length




    #compares two sentences together.
    #If true, the sentences are the same in terms of words
    #If false, the sentences are not the same in terms of words
    def __checkSentences(self,line1,line2):
        #line1 = self.__getSentence(self.testString)
        #line2 = self.__getSentence(self.madeString)
        #for
        for word in range(self.__sentenceLength(line1)):
            word1 = self.__getWord(line1)
            word2 = self.__getWord(line2)
            #print word1,word2
            if(self.__compareLines(word1,word2) == False):
                return False
            else:

                line1 = self.deleteLine(line1)
                line2 = self.deleteLine(line2)
        return True

    #gets the amount of words that are in the sentence
    def __sentenceLength(self,sentence):
        count = 0
        for char in sentence:
            if(char == '\n'):
                count +=1
        return count + 1

    #Compares a valid sentence's tags.
    #If the sentence is not valid then it skips and moves onto
    #the next one.
    def compareSentences(self):
        nextCount = 0
        try:
            for char in self.madeString:
                sentence1 = self.__getSentence(self.testString)
                sentence2= self.__getSentence(self.madeString)

                #if the sentences are the same
                if(self.__checkSentences(sentence1,sentence2) == True):

                    #checks the word + tag for every line
                    for i in range(self.__sentenceLength(sentence1)):
                        line1 = self.__getLine(sentence1,1)
                        line2 = self.__getLine(sentence2,1)

                        #if they're the same, add one to correct
                        if(line1 == line2):
                            self.count+=1
                            self.correct +=1
                            self.correctLst.append(line1)
                        #if they're different then add one to wrong
                        else:
                            #print line1,line2
                            #self.wrongLst.append(line1,line2)
                            self.count+=1
                            self.wrong+=1
                            self.wrongLst.append([line1,line2])
                        #need to increment/delete the spot in both cases

                        sentence1 = self.deleteLine(sentence1)
                        sentence2 = self.deleteLine(sentence2)
                    #delete the sentences off of the strings;
                    self.testString = self.__deleteSentence(self.testString)
                    self.madeString = self.__deleteSentence(self.madeString)

                    #else same word different tag, add 1 to count and wrong
                else:
                    #if the sentence isn't in the created file then delete and move on
                    self.testString = self.__deleteSentence(self.testString)

        #can't figure out how to find out how many sentences are in the test file
        #So I wrote this to iterate until it crashes.
        except:
            pass


    #deletes a single sentence
    def __deleteSentence(self,typeF):
        for i in range(self.__sentenceLength(typeF)):
            if(self.__isTriggerObs(typeF[0])):
                typeF = self.deleteLine(typeF)
                return typeF
            else:
                typeF = self.deleteLine(typeF)
                #print typeF



    def deleteLine(self,sentence):
        for char in sentence:
            if(char == '\n'):
                sentence = sentence[1:]
                return sentence
            else:
                sentence = sentence[1:]


    # checks to see of the observation marks the end of a 'sentence'.
    # True if it marks the end, false otherwise.
    def __isTriggerObs(self, obs):
        triggerLst = [".", ",", "?", "!"]
        if obs in triggerLst:
            return True
        return False

    #get the amount of lines the specified amount
    def __getLine(self,area,amount):
        line = ""
        count = 0
        for char in area:
            if(char != '\n'):
                line+=char
            else:
                count+=1
                line+="\n"
            if(count == amount):
                return line
        return line

    #get a full sentence
    def __getSentence(self,tmpString):
        sentence = ""
        for char in tmpString:
            if(self.__isTriggerObs(char)):
                sentence += char
                return sentence
            else:
                sentence += char

    #get the amount of WORDS in the specified amount
    def __getWord(self,line):
        word = ""
        count = 0
        on = True
        for char in line:
            if(char != ' '):
                word+=char
            else:
                return word
        return word

    #true is the lines are equal, false otherwise
    def __compareLines(self,line1,line2):
        if(line1 == line2):
            return True
        else:
            return False

    #opening the file, returning a string with them. FileName is the file
    def __getFile(self,fileName):
        fileString = ""
        try:
            rawFile = open(fileName,'r')
            for line in rawFile:
                fileString +=line
                #item = line.strip('\n')
                #lookup.append(item)
            return fileString
        except IOError:
            print(fileName + " does not exist or is corrupt.")
            sys.exit(0)

            return fileString
    #return the total count of words checked
    def getCount(self):
        return self.count

    #return the amount of tags correct
    def getCorrect(self):
        return self.correct
    #return the amount of tags incorrect
    def getWrong(self):
        return self.wrong

    #returns the percent correct
    def percentCorrect(self):
        return float(self.correct/float(self.count))

if(__name__ == "__main__"):
    FC =Compare()
    FC.compareSentences()
    print FC.getCorrect()
    print FC.percentCorrect(),"%"
