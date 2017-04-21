'''
Compares two files of information for accurracy based on
the sentances that were tagged.
'''


class fileCompare:

    def __init__(self):
        self.__testFile = "./wordSets/brown_test.txt"
        self.__fileMade = "./wordSets/POStagged.txt"
        self.testString = self.__getFile(self.__testFile)
        self.madeString = self.__getFile(self.__fileMade)
        self.lengthGone = self.getLength(self.testString)

        #self.testString = self.fixString(self.testString)
        #self.madeString = self.fixString(self.madeString)
        self.lengthGone = self.getLength(self.testString)

        self.total = 0
        self.correct = 0
        self.wrong = 0

        self.getSentence()
        #self.deleteUntil()
        #self.compareFile()

    #def checkSentence(self):

    def fixString(self,stringType):
        tmpString = ""
        for char in stringType:
            if(char == '"' or char == ',' or char == '``' or char == "." or "''"):
                tmpString+=char
                tmpString+=" "
            else:
                tmpString += char
        return tmpString
        #print tmpString
    def compareLines(self,line1,line2):
        if(line1 == line2):
            return True
        else:
            return False

    def checkArea(self):
        return True


    def getLength(self,tmp):
        count = 0
        try:
            for char in tmp:
                if(char == '\n'):
                    count +=1
            return count
        except:
            print "error"
    def getWord(self,line,amount):
        word = ""
        count = 0
        on = True
        for char in line:
            if(char != ' ' and on):
                word+=char
            else:
                on = False
            if(char == '\n'):
                on = True
                count +=1
                word+= " "
            if(count == amount):
                return word
        return word

    def getSentence(self):
        for i in range(40):
            if(self.testString[i] == self.madeString[i]):
                deleteLine(1)
    def getLine(self,area,amount):
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


    def deleteLine(self,typeF):
        if(typeF ==1):
            for char in self.testString:
                if(char != "\n"):
                    self.testString = self.testString[1:]
                else:
                    self.testString = self.testString[1:]
                    return
        elif(typeF ==2):
            for char in self.madeString:
                if(char != "\n"):
                    self.madeString = self.madeString[1:]
                else:
                    self.madeString = self.madeString[1:]
                    return

    # checks to see of the observation marks the end of a 'sentence'.
    # True if it marks the end, false otherwise.
    def __isTriggerObs(self, obs):
        triggerLst = [".", ",", "?", "!"]
        if obs in triggerLst:
            return True
        return False
    def checkIgnore(self,wordset1,wordset2):
        wordset1.replace(".","")
        wordset2.replace(".","")
        return wordset1,wordset2


    def compareFile(self):
        for i in range(220):
            #print '\n'
            curTestLine = self.getLine(self.testString,3)
            curMadeLine= self.getLine(self.madeString,3)

            curTestWords = self.getWord(curTestLine,3)
            curMadeWords = self.getWord(curMadeLine,3)

            #curTestWords,curMadeWords = self.checkIgnore(curTestWords,curMadeWords)

            #print curTestWords,curMadeWords
            #print (self.getWord(curTestLine,3))

            if(curTestWords ==curMadeWords):
                #print curTestLine,curMadeLine
                testTag = self.getLine(self.testString,1)
                madeTag = self.getLine(self.madeString,1)

                #the tags correct
                if(testTag == madeTag):
                    self.total +=1
                    self.correct+=1
                    self.deleteLine(2)
                    self.deleteLine(1)
                    print "Correct---",testTag,madeTag
                #the tags incorrect
                else:
                    print "Wrong---", testTag,madeTag
                    self.wrong +=1
                    self.total +=1
                    self.deleteLine(2)
                    self.deleteLine(1)
            else:
                print "Current in test:" ,curTestWords,"In made: ",curMadeWords
                self.deleteUntil()

            #if(self.checkArea() == True):
        #print self.madeString
        print self.correct, self.total
    def __getFile(self,fileName):
        fileString = ""
        try:
            rawFile = open(fileName,'r')
            for line in rawFile:
                fileString +=line
                #item = line.strip('\n')
                #lookup.append(item)
        except IOError:
            print(fileName + " does not exist or is corrupt.")
            sys.exit(0)

        return fileString

    def deleteUntil(self):
        if(self.__isTriggerObs(self.testString[0])):
            self.deleteLine(1)
            return
        #print self.madeString
        for char in self.testString:
            if(self.__isTriggerObs(char)):
                #print self.madeString
                #self.deleteLine(1)
                #print self.testString
                return
            else:
                self.testString = self.testString[1:]

        #print self.madeString

if(__name__ == "__main__"):
    FC = fileCompare()
