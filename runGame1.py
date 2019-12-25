#NAME: ISHIKA SAXENA
#ANDREWID: isaxena
import math, copy, string
import random
# cmu_112_graphics_final taken from 15-112 CMU Fundamentals in Programming & Computer Science Course: 
# Taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics_final import *
# tkinter from https://docs.python.org/3/library/tkinter.html
from tkinter import *
from PIL import Image
# PIL from https://www.pythonware.com/products/pil/
from splashScreen1 import *
from instructions1 import *
from middleMode1 import *
from board1 import *
from word1 import *
from rack1 import *

# The bag of tiles. Contains distribution of letters and point values of letters.
class Bag(object):
    def __init__(self, app):
        self.app = app
        self.numOfTiles = 100
        self.letterValuesDict = self.getLetterValues() #points for each letter
        self.letterAmountsDict = self.getLetterAmounts() #amounts of each letter in bag

        self.bagList = []
        self.initializeStartingBag()

        self.currentAmtOfTiles = 100
    

    # Returns dictionary mapping each tile (letter) to its corresponding point value
    def getLetterValues(self):
        letterValuesDict = dict()
        letterValuesDict["A"] = 1
        letterValuesDict["B"] = 3
        letterValuesDict["C"] = 3
        letterValuesDict["D"] = 2
        letterValuesDict["E"] = 1
        letterValuesDict["F"] = 4
        letterValuesDict["G"] = 2
        letterValuesDict["H"] = 4
        letterValuesDict["I"] = 1
        letterValuesDict["J"] = 8
        letterValuesDict["K"] = 5
        letterValuesDict["L"] = 1
        letterValuesDict["M"] = 3
        letterValuesDict["N"] = 1
        letterValuesDict["O"] = 1
        letterValuesDict["P"] = 3
        letterValuesDict["Q"] = 10
        letterValuesDict["R"] = 1
        letterValuesDict["S"] = 1
        letterValuesDict["T"] = 1
        letterValuesDict["U"] = 1
        letterValuesDict["V"] = 4
        letterValuesDict["W"] = 4
        letterValuesDict["X"] = 8
        letterValuesDict["Y"] = 4
        letterValuesDict["Z"] = 10
        letterValuesDict["!"] = 0 #blank tile
        return letterValuesDict

    # Returns dictionary mapping each tile (letter) to its amount in the bag at 
    # the start. 
    def getLetterAmounts(self):
        letterAmountsDict = dict()
        letterAmountsDict["A"] = 9
        letterAmountsDict["B"] = 2
        letterAmountsDict["C"] = 2
        letterAmountsDict["D"] = 4
        letterAmountsDict["E"] = 12
        letterAmountsDict["F"] = 2
        letterAmountsDict["G"] = 3
        letterAmountsDict["H"] = 2
        letterAmountsDict["I"] = 9
        letterAmountsDict["J"] = 1
        letterAmountsDict["K"] = 1
        letterAmountsDict["L"] = 4
        letterAmountsDict["M"] = 2
        letterAmountsDict["N"] = 6
        letterAmountsDict["O"] = 8
        letterAmountsDict["P"] = 2
        letterAmountsDict["Q"] = 1
        letterAmountsDict["R"] = 6
        letterAmountsDict["S"] = 4
        letterAmountsDict["T"] = 6
        letterAmountsDict["U"] = 4
        letterAmountsDict["V"] = 2
        letterAmountsDict["W"] = 2
        letterAmountsDict["X"] = 1
        letterAmountsDict["Y"] = 2
        letterAmountsDict["Z"] = 1
        letterAmountsDict["!"] = 2 #blank tiles
        return letterAmountsDict

    # Initializes starting bag by adding Tiles to it in correct amounts
    def initializeStartingBag(self):
        for letter in string.ascii_uppercase:
            numOfTilesOfThisLetter = self.letterAmountsDict[letter]
            for i in range(numOfTilesOfThisLetter):
                self.bagList.append(Tile(letter, self.letterValuesDict[letter], 0, 0))
        # add the blank tiles (bc they're not a letter):
        for i in range(self.letterAmountsDict["!"]):
            self.bagList.append(Tile("!", self.letterValuesDict["!"], 0, 0))
    
    # takes a tile out randomly AND also returns the tile taken out
    def takeFromBag(self): 
        if(self.currentAmtOfTiles > 14):
            self.currentAmtOfTiles -= 1
            randPos = random.randint(0, len(self.bagList)-1)
            return self.bagList.pop(randPos)
        else:
            self.app.gameOver = True



# Tile class contains specification for the tiles that are in your rack/on the board
class Tile(object):
    def __init__(self, letter, pointValueOfLetter, x, y):
        self.letter = letter
        self.pointVal = pointValueOfLetter
        self.x = x
        self.y = y
        self.currentFill = "#DEB887"
        self.isClickedOn = False        #detect whether clicked on by player
    
    def __repr__(self):
        return str(self.letter) + ":" + str(self.pointVal)
    
    def __eq__(self, other):
        return (isinstance(other, Tile) and (self.letter == other.letter) and (self.pointVal == other.pointVal) and (self.x == other.x) and (self.y == other.y))

    def updateFill(self):
        if self.isClickedOn == True:
            self.currentFill = "#948f8b"
        else:
            self.currentFill = "#DEB887"



# Player class contains attributes of Player, such as their selectedTiles and possibleWord they're building
class Player(object):
    def __init__(self, app, name, bag):
        self.app = app
        self.name = name
        self.score = 0
        self.bag = bag       # pass in bag when u create player SO each player gets the same bag 
        self.rack = Rack(self.app, self.bag) 
        self.wordInstance = Word("forCompClass", self.bag)
        self.putBack = []      
        self.isTurn = False     
        self.selectedWord = ""   
        self.selectedWordIsValid = None
        self.selectedTiles = [] 
        self.boardAndWordValid = None   
        self.possibleWord = ""
        self.wordList = []
        self.updownDone = None
        self.leftRightDone = None
        self.selectedPositionIsValid = None
        self.selectedWordDictIsValid = None
        self.wordSelectingIsDone = False
        self.clickList = []
        self.listOfPossibleWordsBasedOnRack = []
        self.sortedListOfPossibleWords = []
        self.stringRack = []  
        self.finalPlacementOfWords = [] 
        self.tryThisRowCol= [-1, -1]
        self.placedLetter1 = ""
        self.placedLetter2 = ""
        self.placedLetter3 = ""
        self.placedLetter4 = ""
        self.currentBoardSelectionTuple = (-1, -1)

    # amtOfIncrease is dependent on the WORD that the player forms/associated point values
    def increasePlayerScore(self, amtOfIncrease):
        self.score += amtOfIncrease
    
    def createStringRack(self):
        if len(self.rack.rackList) < 7:
            self.app.gameOver = True
        else:
            for tile in self.rack.rackList:
                if isinstance(tile, Tile):
                    if isinstance(tile.letter, str):
                        self.stringRack.append(tile.letter)
    
        # Creates the list  of possible words (from list of generated words of needed length) 
    # based on the Rack
    def createListOfPossibleWordsBasedOnRack(self):        
        # And now, add in len 3 words (so that all len 4 words are checked before because normally of more points)
        for word in self.wordInstance.len3DictSet: 
            word = word.upper()
            count = 0
            listVersion = []
            #making word into list
            for c in word:
                listVersion.append(c)
            # we are creating a list of words for which the computer has n-1 letters (n being the len of the word)
            for c in listVersion:
                if c not in self.stringRack:
                    count = count+1
                elif word.count(c) > self.stringRack.count(c): #if not enough of a certain letter in rack
                    count = 100 #we skip this word
            if count > 1 or count==0:
                continue
            elif count == 1:
                self.listOfPossibleWordsBasedOnRack.append(word)
    
    # Calculate score of word based on just letter values
    def calculateRawScore(self, word):
        score = 0
        for c in word:
            if "'" not in c:
                score += self.app.b1.letterValuesDict[c]
        return score
    
    # Create the SORTED list of possible words the computer can make
    def createSortedListOfPossibleWords(self): 
        import operator
        # Create dictionary mapping each word to its score
        tempDict = dict()
        for word in self.listOfPossibleWordsBasedOnRack:
            score = self.calculateRawScore(word)
            tempDict[word] = score
        # Below line adapted from: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
        # Essentially sorting the keys of the dictionary based on their values (i.e. scores) in high to low
        sortOfTuples = sorted(tempDict.items(), key=operator.itemgetter(1), reverse=True)
        for (word, score) in sortOfTuples:
            self.sortedListOfPossibleWords.append(word)
    
    
    def findPossibleRowColToPlace(self, word): 
        # Find the letter we need
        whatLetterWeNeed = ""                   
        listVersion = []
        for c in word:
            listVersion.append(c)
        for c in listVersion:
            if c not in self.stringRack:
                whatLetterWeNeed = c
                break
        
        # Have all the letters
        if whatLetterWeNeed == "":
            self.tryThisRowCol[0] = -1
            self.tryThisRowCol[1] = -1
            return "nope"

        # Find the row, col needed
        for row in range (len(self.app.board.textBoard)):
            for col in range (len(self.app.board.textBoard[0])):
                if self.app.board.textBoard[row][col] == whatLetterWeNeed:
                    self.tryThisRowCol[0] = row
                    self.tryThisRowCol[1] = col
                    return whatLetterWeNeed
        
        
        for row in range (len(self.app.board.textBoard)):
            for col in range (len(self.app.board.textBoard[0])):
                if self.app.board.textBoard[row][col] != "-":
                    return "nope"
        
        return "pick a word"

    def helpp(self):
        self.createStringRack()
        self.createListOfPossibleWordsBasedOnRack()
        self.createSortedListOfPossibleWords()
        for word in self.sortedListOfPossibleWords:
            hm = self.findPossibleRowColToPlace(word)
            if hm == "nope" or hm == "pick a word":
                continue
            else:
                print(word) #words that u have 2 letters for and 1 letter is on board
        #self.app.help = False



# Computer (or AI) class is a subclass of Player class
# It contains attributes relevant to the computer forming its own word based on
# location of other words on the board
class Computer(Player):
    def __init__(self, app, name, bag):
        super().__init__(app, name, bag)
        self.wordInstance = Word("forCompClass", self.bag)
        self.listOfPossibleWordsBasedOnRack = []
        self.sortedListOfPossibleWords = []
        self.stringRack = []  
        self.createStringRack()
        self.createListOfPossibleWordsBasedOnRack()
        self.createSortedListOfPossibleWords()
        self.tryThisRowCol = [-1, -1] 
        self.finalPlacementOfWords = [] 
        self.placedLetter1 = ""
        self.placedLetter2 = ""
        self.placedLetter3 = ""
        self.placedLetter4 = ""
        self.app.hasSkippedTurn = False
    
    # String version of rack (as rack is a list of Tile instances)
    def createStringRack(self):
        if len(self.rack.rackList) < 7:
            self.app.gameOver = True
        else:
            for tile in self.rack.rackList:
                if isinstance(tile, Tile):
                    if isinstance(tile.letter, str):
                        self.stringRack.append(tile.letter)
    
    # Called when the computer has made its turn and we must reset everything and call the next player (human)
    def removeFromRackAndReplenishWhenDone(self):
        placedLetters = [self.placedLetter1, self.placedLetter2, self.placedLetter3, self.placedLetter4]
        #print(placedLetters)
        #print(self.rack.rackList)
        for letter in placedLetters:
            for tile in self.rack.rackList:
                if tile.letter == letter:
                    self.rack.takeFromRack(tile)
        #print(self.rack.rackList)
        self.rack.replenishRack()
        #print(self.rack.rackList)
        self.stringRack = []
        self.listOfPossibleWordsBasedOnRack = []
        self.sortedListOfPossibleWords = []
        self.placedLetter1 = ""
        self.placedLetter2 = ""
        self.placedLetter3 = ""
        self.placedLetter4 = ""
        self.tryThisRowCol = [-1, -1]
        self.clickList = []
        self.createStringRack() 
        self.createListOfPossibleWordsBasedOnRack() 
        self.createSortedListOfPossibleWords()
        self.app.getNextPlayer()
    
    # Calculates the computer's score taking into account double word etc tiles and letter values
    def calculateComputerScore(self, word):
        listOfLetters = []
        special = []
        score = 0
        for (row, col) in self.clickList:
            letter = self.app.board.textBoard[row][col]
            listOfLetters.append(letter)
            if (row, col) in self.app.board.doubleLetterLocations:
                score += 2*self.app.b1.letterValuesDict[letter]
            elif (row, col) in self.app.board.tripleLetterLocations:
                score += 3*self.app.b1.letterValuesDict[letter]
            else:
                score += self.app.b1.letterValuesDict[letter]
            if (row, col) in self.app.board.doubleWordLocations:
                special.append("dw")
            elif(row, col) in self.app.board.tripleWordLocations:
                special.append("tw")
        #find missing letters (i.e. letters besides the ones u placed down)
        for c in word:
            if c not in listOfLetters:
                score = score + self.app.b1.letterValuesDict[c]
        #do dw and tw calcs
        for thing in special:
            if thing == "dw":
                score = score*2
            elif thing == "tw":
                score = score*3
        self.score += score

    
    # Creates the list  of possible words (from list of generated words of needed length) 
    # based on the Rack
    def createListOfPossibleWordsBasedOnRack(self):
        # First add words of len 5 to list
        for word in self.wordInstance.len5DictSet:
            word = word.upper()
            count = 0
            listVersion = []
            # making word into a list for easier traversal
            for c in word:
                listVersion.append(c)
            # we are creating a list of words for which the computer has n-1 letters (n being the len of the word)
            for c in listVersion:
                if c not in self.stringRack:
                    count = count+1
                elif word.count(c) > self.stringRack.count(c): #if not enough of a certain letter in rack
                    count = 100 #we skip this word
            if count > 1 or count==0:
                continue
            elif count == 1:
                self.listOfPossibleWordsBasedOnRack.append(word)

        # Next add words of length 4 to list
        for word in self.wordInstance.len4DictSet:
            word = word.upper()
            count = 0
            listVersion = []
            # making word into a list for easier traversal
            for c in word:
                listVersion.append(c)
            # we are creating a list of words for which the computer has n-1 letters (n being the len of the word)
            for c in listVersion:
                if c not in self.stringRack:
                    count = count+1
                elif word.count(c) > self.stringRack.count(c): #if not enough of a certain letter in rack
                    count = 100 #we skip this word
            if count > 1 or count==0:
                continue
            elif count == 1:
                self.listOfPossibleWordsBasedOnRack.append(word)
        
        # And now, add in len 3 words (so that all len 4 words are checked before because normally of more points)
        for word in self.wordInstance.len3DictSet: 
            word = word.upper()
            count = 0
            listVersion = []
            #making word into list
            for c in word:
                listVersion.append(c)
            # we are creating a list of words for which the computer has n-1 letters (n being the len of the word)
            for c in listVersion:
                if c not in self.stringRack:
                    count = count+1
                elif word.count(c) > self.stringRack.count(c): #if not enough of a certain letter in rack
                    count = 100 #we skip this word
            if count > 1 or count==0:
                continue
            elif count == 1:
                self.listOfPossibleWordsBasedOnRack.append(word)
    
    # Calculate score of word based on just letter values
    def calculateRawScore(self, word):
        score = 0
        for c in word:
            if "'" not in c:
                score += self.app.b1.letterValuesDict[c]
        return score
    
    # Create the SORTED list of possible words the computer can make
    def createSortedListOfPossibleWords(self): 
        import operator
        # Create dictionary mapping each word to its score
        tempDict = dict()
        for word in self.listOfPossibleWordsBasedOnRack:
            score = self.calculateRawScore(word)
            tempDict[word] = score
        # Below line adapted from: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
        # Essentially sorting the keys of the dictionary based on their values (i.e. scores) in high to low
        sortOfTuples = sorted(tempDict.items(), key=operator.itemgetter(1), reverse=True)
        for (word, score) in sortOfTuples:
            self.sortedListOfPossibleWords.append(word)
    
    # Finds the location of the 1 letter that the computer must find on the board
    # If not found or the computer has all letters needed for the word, returns "nope"
    # If the board is completely empty, returns "pick a word" to indicate that the computer must
    # simply place a word since it's currently empty
    def findPossibleRowColToPlace(self, word): 
        # Find the letter we need
        whatLetterWeNeed = ""                   
        listVersion = []
        for c in word:
            listVersion.append(c)
        for c in listVersion:
            if c not in self.stringRack:
                whatLetterWeNeed = c
                break
        
        # Have all the letters
        if whatLetterWeNeed == "":
            self.tryThisRowCol[0] = -1
            self.tryThisRowCol[1] = -1
            return "nope"

        # Find the row, col needed
        for row in range (len(self.app.board.textBoard)):
            for col in range (len(self.app.board.textBoard[0])):
                if self.app.board.textBoard[row][col] == whatLetterWeNeed:
                    self.tryThisRowCol[0] = row
                    self.tryThisRowCol[1] = col
                    return whatLetterWeNeed
        
        
        for row in range (len(self.app.board.textBoard)):
            for col in range (len(self.app.board.textBoard[0])):
                if self.app.board.textBoard[row][col] != "-":
                    return "nope"
        
        return "pick a word"
        
    # Given a word with length 3, determine which case it is
    # Does the computer have the first 2 letters, or the last 2 letters, or etc
    def determineWhichCase3(self, word):
        letter1 = word[0]
        letter2 = word[1]
        letter3 = word[2]
        if letter1 in self.stringRack and letter2 in self.stringRack:
            self.placedLetter1 = letter1
            self.placedLetter2 = letter2
            return "haveFirst2Letters"
        elif letter2 in self.stringRack and letter3 in self.stringRack:
            self.placedLetter1 = letter2
            self.placedLetter2 = letter3
            return "haveLast2Letters"
        elif letter1 in self.stringRack and letter3 in self.stringRack:
            self.placedLetter1 = letter1
            self.placedLetter2 = letter3
            return "haveSide2Letters"
        else:
            return "nope"
    
    # Given a word with length 4, determine which case it is
    # Does the computer have the first 3 letters, or the last 3 letters, or etc
    def determineWhichCase4(self, word):
        letter1 = word[0]
        letter2 = word[1]
        letter3 = word[2]
        letter4 = word[3]
        #have First3Letters, Last3Letters, First1Last2Letters, First2Last1Letters
        if letter1 in self.stringRack and letter2 in self.stringRack and letter3 in self.stringRack:
            self.placedLetter1 = letter1
            self.placedLetter2 = letter2
            self.placedLetter3 = letter3
            return "haveFirst3Letters"
        elif letter2 in self.stringRack and letter3 in self.stringRack and letter4 in self.stringRack:
            self.placedLetter1 = letter2
            self.placedLetter2 = letter3
            self.placedLetter3 = letter4
            return "haveLast3Letters"
        elif letter1 in self.stringRack and letter3 in self.stringRack and letter4 in self.stringRack:
            self.placedLetter1 = letter1
            self.placedLetter2 = letter3
            self.placedLetter3 = letter4
            return "haveFirst1Last2Letters"
        elif letter1 in self.stringRack and letter2 in self.stringRack and letter4 in self.stringRack:
            self.placedLetter1 = letter1
            self.placedLetter2 = letter2
            self.placedLetter3 = letter4
            return "haveFirst2Last1Letters"
        else:
            return "nope"
    
    # Given a word with length 5, determine which case it is
    # Does the computer have the first 4 letters, or the last 4 letters, or etc
    def determineWhichCase5(self, word):
        letter1 = word[0]
        letter2 = word[1]
        letter3 = word[2]
        letter4 = word[3]
        letter5 = word[4]
        if letter1 in self.stringRack and letter2 in self.stringRack and letter3 in self.stringRack\
            and letter4 in self.stringRack:
            self.placedLetter1 = letter1
            self.placedLetter2 = letter2
            self.placedLetter3 = letter3
            self.placedLetter4 = letter4
            return "haveFirst4Letters"
        elif letter2 in self.stringRack and letter3 in self.stringRack and letter4 in self.stringRack\
            and letter5 in self.stringRack:
            self.placedLetter1 = letter2
            self.placedLetter2 = letter3
            self.placedLetter3 = letter4
            self.placedLetter4 = letter5
            return "haveLast4Letters"

    
    # This method controls the placing of word by the computer, a sort of backtracking idea
    # that loops through the list of possible words, and then calls methods to check whether 
    # these words would have valid placements. If a word does have valid placement, goes to the next word
    # It checks words of higher scores first.
    def theComputerCheckGame(self): 
        self.app.hasSkippedTurn = False # the computer hasn't skipped a turn yet
        for word in self.sortedListOfPossibleWords:
            # If at the last word in list, call next player and reset everything
            if self.sortedListOfPossibleWords.index(word) == len(self.sortedListOfPossibleWords)-1:
                self.app.hasSkippedTurn = True
                for tile in self.rack.rackList:
                    self.rack.takeFromRack(tile) 
                self.rack.replenishRack()
                self.stringRack = []
                self.listOfPossibleWordsBasedOnRack = []
                self.sortedListOfPossibleWords = []
                self.placedLetter1 = ""
                self.placedLetter2 = ""
                self.placedLetter3 = ""
                self.placedLetter4 = ""
                self.tryThisRowCol = [-1, -1]
                self.clickList = []
                self.createStringRack() 
                self.createListOfPossibleWordsBasedOnRack()
                self.createSortedListOfPossibleWords()
                self.app.getNextPlayer()
                return
            
            # what letter computer needs
            whatLetterWeNeed = self.findPossibleRowColToPlace(word)
            if whatLetterWeNeed == "nope": #ie whatLetterWeNeed isn't found on board
                continue
            elif whatLetterWeNeed == "pick a word": #ie no letters currently on the board
                firstCompWord = word #computer is simply going to place current word, if it's of length 3
                if len(firstCompWord) == 3:
                    self.placedLetter1 = firstCompWord[0]
                    self.placedLetter2 = firstCompWord[1]
                    self.placedLetter3 = firstCompWord[2]
                    self.app.board.textBoard[7][7] = self.placedLetter1
                    self.app.board.textBoard[7][8] = self.placedLetter2
                    self.app.board.textBoard[7][9] = self.placedLetter3
                    self.clickList.append((7,7))
                    self.clickList.append((7,8))
                    self.clickList.append((7,9))
                    self.calculateComputerScore(firstCompWord)
                    self.setUpDrawCase2a(self.placedLetter1, self.placedLetter2, self.placedLetter3)
                    self.removeFromRackAndReplenishWhenDone()
                    return
                else:
                    continue

            if self.tryThisRowCol[0] == -1 or self.tryThisRowCol[1] == -1: #computer has all required tiles, so it's not missing 1
                continue
            
            # Dealing with len 3 and len 4 words
            # Determine which case they are
            if len(word) == 3:
                print('in len3')
                case = self.determineWhichCase3(word)
            elif len(word) == 4:
                print('in len 4')
                case = self.determineWhichCase4(word)
            elif len(word) == 5:
                case = self.determineWhichCase5(word)
            print(word, case, whatLetterWeNeed, self.tryThisRowCol[0], self.tryThisRowCol[1], end=" ")
            # Determine the val, True or False, of whether they can be placed there or not
            if case == "haveFirst2Letters":
                val = self.decideIfPlacingCase1(word)
            elif case == "haveLast2Letters":
                val = self.decideIfPlacingCase2(word)
            elif case == "haveSide2Letters":
                val = self.decideIfPlacingCase3(word)
            elif case == "haveFirst3Letters":
                print("ARE U IN HERE 11")
                val = self.decideIfPlacingCase1Len4(word)
            elif case == "haveLast3Letters":
                val = self.decideIfPlacingCase2Len4(word)
            elif case == "haveFirst1Last2Letters":
                val = self.decideIfPlacingCase3Len4(word)
            elif case == "haveFirst2Last1Letters":
                val = self.decideIfPlacingCase4Len4(word)
            elif case == "haveFirst4Letters":
                val = self.decideIfPlacingCase1Len5(word)
            elif case == "haveLast4Letters":
                val = self.decideIfPlacingCase2Len5(word)
            else: #no valid case
                print("moving on to next word")
                #if index of word is last thing in list ie
                #we've reached the end, shuffle and continue
                if self.sortedListOfPossibleWords.index(word) == len(self.sortedListOfPossibleWords)-1:
                    print("ye shuffles")
                    self.app.hasSkippedTurn = True
                    for tile in self.rack.rackList:
                        self.rack.takeFromRack(tile) 
                    self.rack.replenishRack()
                    self.stringRack = []
                    self.listOfPossibleWordsBasedOnRack = []
                    self.sortedListOfPossibleWords = []
                    self.placedLetter1 = ""
                    self.placedLetter2 = ""
                    self.placedLetter3 = ""
                    self.placedLetter4 = ""
                    self.tryThisRowCol = [-1, -1]
                    self.clickList = []
                    self.createStringRack() #stringrackprobs @ish
                    self.createListOfPossibleWordsBasedOnRack()
                    self.createSortedListOfPossibleWords()
                    self.app.getNextPlayer()
                    return
                else:
                    print("WaH DID YOU GO HERE 33")
                    continue
            
            # Condition on the value of val
            print("DID YOU READCH HERE 22")
            print("val",val)
            # If true ie can be placed, place it and calculate score and reset everything
            if val == True:
                print("in true shouldn't it go")
                self.calculateComputerScore(word)
                self.removeFromRackAndReplenishWhenDone()
                return
            # Else, continue until you find a word that works
            elif val == False:
                print("in false")
                if self.sortedListOfPossibleWords.index(word) == len(self.sortedListOfPossibleWords)-1:
                    print("ye shuffles - in", str(case), "false")
                    self.app.hasSkippedTurn = True
                    for tile in self.rack.rackList:
                        self.rack.takeFromRack(tile) 
                    self.rack.replenishRack()
                    self.stringRack = []
                    self.listOfPossibleWordsBasedOnRack = []
                    self.sortedListOfPossibleWords = []
                    self.placedLetter1 = ""
                    self.placedLetter2 = ""
                    self.placedLetter3 = ""
                    self.placedLetter4 = ""
                    self.tryThisRowCol = [-1, -1]
                    self.clickList = []
                    self.createStringRack() #stringrackprobs @ish
                    self.createListOfPossibleWordsBasedOnRack()
                    self.createSortedListOfPossibleWords()
                    self.app.getNextPlayer()
                    #print(self.app.board.textBoard)
                    return
                else:
                    print('in hereeee')
                    #print(self.app.board.textBoard)
                    continue #go to next word in list of possib words, which could very well be a len4 word
                
    def decideIfPlacingCase2Len5(self, word): #have last 4 letters
        row = self.tryThisRowCol[0]
        col = self.tryThisRowCol[1]
        letter2 = word[1]
        letter3 = word[2]
        letter4 = word[3]
        letter5 = word[4]
        if row+4 < 15 and row-4 > -1 and col+4 < 15 and col-4 > -1 and row+5 < 15 and col+5 < 15:
            if self.app.board.textBoard[row+1][col] == "-" and self.app.board.textBoard[row+2][col] == "-" \
                and self.app.board.textBoard[row+3][col] == "-" and self.app.board.textBoard[row+4][col] == "-"\
                and self.app.board.textBoard[row+1][col-1] == "-" and self.app.board.textBoard[row+1][col+1] == "-"\
                and self.app.board.textBoard[row+2][col-1] == "-" and self.app.board.textBoard[row+2][col+1] == "-"\
                and self.app.board.textBoard[row+3][col-1] == "-" and self.app.board.textBoard[row+3][col+1] == "-"\
                and self.app.board.textBoard[row+4][col-1] == "-" and self.app.board.textBoard[row+4][col+1] == "-"\
                and self.app.board.textBoard[row+5][col] == "-" and self.app.board.textBoard[row-1][col] == "-":
                self.app.board.textBoard[row+1][col] = letter2
                self.app.board.textBoard[row+2][col] = letter3
                self.app.board.textBoard[row+3][col] = letter4
                self.app.board.textBoard[row+4][col] = letter5
                self.clickList.append((row+1, col))
                self.clickList.append((row+2, col))
                self.clickList.append((row+3, col))
                self.clickList.append((row+4, col))
                self.setUpDrawCase3a(letter2, letter3, letter4, letter5)
                return True
            elif self.app.board.textBoard[row][col+1] == "-" and self.app.board.textBoard[row][col+2] == "-" \
                and self.app.board.textBoard[row][col+3] == "-" and self.app.board.textBoard[row][col+4] == "-"\
                and self.app.board.textBoard[row+1][col+1] == "-" and self.app.board.textBoard[row-1][col+1] == "-"\
                and self.app.board.textBoard[row+1][col+2] == "-" and self.app.board.textBoard[row-1][col+2] == "-"\
                and self.app.board.textBoard[row+1][col+3] == "-" and self.app.board.textBoard[row-1][col+3] == "-"\
                and self.app.board.textBoard[row+1][col+4] == "-" and self.app.board.textBoard[row-1][col+4] == "-"\
                and self.app.board.textBoard[row][col+5] == "-" and self.app.board.textBoard[row][col-1] == "-":
                self.app.board.textBoard[row][col+1] = letter2
                self.app.board.textBoard[row][col+2] = letter3
                self.app.board.textBoard[row][col+3] = letter4
                self.app.board.textBoard[row][col+4] = letter5
                self.clickList.append((row, col+1))
                self.clickList.append((row, col+2))
                self.clickList.append((row, col+3))
                self.clickList.append((row, col+4))
                self.setUpDrawCase3a(letter2, letter3, letter4, letter5)
                return True
            else:
                return False
        else:
            return False

    def decideIfPlacingCase1Len5(self, word): #have 1st 4 letters
        row = self.tryThisRowCol[0]
        col = self.tryThisRowCol[1]
        letter1 = word[0]
        letter2 = word[1]
        letter3 = word[2]
        letter4 = word[3]
        if row+4 < 15 and row-4 > -1 and col+4 < 15 and col-4 > -1:
            if self.app.board.textBoard[row-4][col] == "-" and self.app.board.textBoard[row-3][col] == "-" \
                and self.app.board.textBoard[row-2][col] == "-" and self.app.board.textBoard[row-1][col] == "-" \
                and self.app.board.textBoard[row-4][col-1] == "-"  and self.app.board.textBoard[row-4][col+1] == "-" \
                and self.app.board.textBoard[row-3][col-1] == "-" and self.app.board.textBoard[row-3][col+1] == "-" \
                and self.app.board.textBoard[row-2][col-1] == "-" and self.app.board.textBoard[row-2][col+1] == "-" \
                and self.app.board.textBoard[row-1][col-1] == "-" and self.app.board.textBoard[row-1][col+1] == "-" \
                and self.app.board.textBoard[row-5][col] == "-" and self.app.board.textBoard[row+1][col] == "-":
                self.app.board.textBoard[row-4][col] = letter1
                self.app.board.textBoard[row-3][col] = letter2
                self.app.board.textBoard[row-2][col] = letter3
                self.app.board.textBoard[row-1][col] = letter4
                self.clickList.append((row-4, col))
                self.clickList.append((row-3, col))
                self.clickList.append((row-2, col))
                self.clickList.append((row-1, col))
                self.setUpDrawCase3a(letter1, letter2, letter3, letter4)
                return True
            elif self.app.board.textBoard[row][col-4] == "-" and self.app.board.textBoard[row][col-3] == "-" \
                and self.app.board.textBoard[row][col-2] == "-" and self.app.board.textBoard[row][col-1] == "-" \
                and self.app.board.textBoard[row+1][col-4] == "-"  and self.app.board.textBoard[row-1][col-4] == "-" \
                and self.app.board.textBoard[row+1][col-3] == "-" and self.app.board.textBoard[row-1][col-3] == "-" \
                and self.app.board.textBoard[row+1][col-2] == "-" and self.app.board.textBoard[row-1][col-2] == "-" \
                and self.app.board.textBoard[row+1][col-1] == "-" and self.app.board.textBoard[row-1][col-1] == "-" \
                and self.app.board.textBoard[row][col-5] == "-" and self.app.board.textBoard[row][col+1] == "-":
                self.app.board.textBoard[row][col-4] = letter1
                self.app.board.textBoard[row][col-3] = letter2
                self.app.board.textBoard[row][col-2] = letter3
                self.app.board.textBoard[row][col-1] = letter4
                self.clickList.append((row, col-4))
                self.clickList.append((row, col-3))
                self.clickList.append((row, col-2))
                self.clickList.append((row, col-1))
                self.setUpDrawCase3a(letter1, letter2, letter3, letter4)
                return True
            else:
                return False
        else:
            return False

    # Determines whether computer can place a word of case 4, len 4, meaning that
    # The computer has the first, second, and fourth letter of the word and must find the third one
    # (More comments given in decideIfPlacingCase1(self, word) below)
    def decideIfPlacingCase4Len4(self, word):
        row = self.tryThisRowCol[0]
        col = self.tryThisRowCol[1]
        letter1 = word[0]
        letter2 = word[1]
        letter4 = word[3]
        if row+3 < 15 and row-3 > -1 and col+3 < 15 and col-3 > -1:
            if self.app.board.textBoard[row-2][col] == "-" and self.app.board.textBoard[row-1][col] == "-" and self.app.board.textBoard[row+1][col] == "-" \
                and self.app.board.textBoard[row-2][col+1] == "-" and self.app.board.textBoard[row-2][col-1] == "-" \
                and self.app.board.textBoard[row-1][col+1] == "-" and self.app.board.textBoard[row-1][col-1] == "-" \
                and self.app.board.textBoard[row+1][col+1] == "-" and self.app.board.textBoard[row+1][col-1] == "-" \
                and self.app.board.textBoard[row-3][col] == "-" and self.app.board.textBoard[row+2][col] == "-":
                self.app.board.textBoard[row-2][col] = letter1
                self.app.board.textBoard[row-1][col] = letter2
                self.app.board.textBoard[row+1][col] = letter4
                self.clickList.append((row-2, col))
                self.clickList.append((row-1, col))
                self.clickList.append((row+1, col))
                # Draw the tiles on the board if True
                self.setUpDrawCase2a(letter1, letter2, letter4)
                return True
            elif self.app.board.textBoard[row][col-2] == "-" and self.app.board.textBoard[row][col-1] == "-" and self.app.board.textBoard[row][col+1] == "-" \
                and self.app.board.textBoard[row-1][col-2] == "-" and self.app.board.textBoard[row+1][col-2] == "-" \
                and self.app.board.textBoard[row-1][col-1] == "-" and self.app.board.textBoard[row+1][col-1] == "-" \
                and self.app.board.textBoard[row-1][col+1] == "-" and self.app.board.textBoard[row+1][col+1] == "-" \
                and self.app.board.textBoard[row][col-3] == "-" and self.app.board.textBoard[row][col+2] == "-":
                self.app.board.textBoard[row][col-2] = letter1
                self.app.board.textBoard[row][col-1] = letter2
                self.app.board.textBoard[row][col+1] = letter4
                self.clickList.append((row, col-2))
                self.clickList.append((row, col-1))
                self.clickList.append((row, col+1))
                # Draw the tiles on the board if True
                self.setUpDrawCase2a(letter1, letter2, letter4)
                return True
            else:
                return False
        else:
            return False

    # Determines whether computer can place a word of case 3, len 4, meaning that
    # the computer has the first, third, and fourth letter of the word and must find the third one
    def decideIfPlacingCase3Len4(self, word):
        row = self.tryThisRowCol[0]
        col = self.tryThisRowCol[1]
        letter1 = word[0]
        letter3 = word[2]
        letter4 = word[3]
        if row+3 < 15 and row-3 > -1 and col+3 < 15 and col-3 > -1:
            #PLACE VERTICALLY
            if self.app.board.textBoard[row-1][col] == "-" and self.app.board.textBoard[row+1][col] == "-" and self.app.board.textBoard[row+2][col] == "-" \
                and self.app.board.textBoard[row-1][col+1] == "-" and self.app.board.textBoard[row-1][col-1] == "-" \
                and self.app.board.textBoard[row+1][col+1] == "-" and self.app.board.textBoard[row+1][col-1] == "-" \
                and self.app.board.textBoard[row+2][col+1] == "-" and self.app.board.textBoard[row+2][col-1] == "-" \
                and self.app.board.textBoard[row-2][col] == "-" and self.app.board.textBoard[row+3][col] == "-":
                self.app.board.textBoard[row-1][col] = letter1
                self.app.board.textBoard[row+1][col] = letter3
                self.app.board.textBoard[row+2][col] = letter4
                self.clickList.append((row-1, col))
                self.clickList.append((row+1, col))
                self.clickList.append((row+2, col))
                self.setUpDrawCase2a(letter1, letter3, letter4)
                return True
            #PLACE HORIZ
            elif self.app.board.textBoard[row][col-1] == "-" and self.app.board.textBoard[row][col+1] == "-" and self.app.board.textBoard[row][col+2] == "-" \
                and self.app.board.textBoard[row-1][col-1] == "-" and self.app.board.textBoard[row+1][col-1] == "-" \
                and self.app.board.textBoard[row-1][col+1] == "-" and self.app.board.textBoard[row+1][col+1] == "-" \
                and self.app.board.textBoard[row-1][col+2] == "-" and self.app.board.textBoard[row+1][col+2] == "-" \
                and self.app.board.textBoard[row][col-2] == "-" and self.app.board.textBoard[row][col+3]:
                self.app.board.textBoard[row][col-1] = letter1
                self.app.board.textBoard[row][col+1] = letter3
                self.app.board.textBoard[row][col+2] = letter4
                self.clickList.append((row, col-1))
                self.clickList.append((row, col+1))
                self.clickList.append((row, col+2))
                self.setUpDrawCase2a(letter1, letter3, letter4)
                return True
            else:
                return False
        else:
            return False

    # Determines whether computer can place a word of case 2, len 4, meaning that
    # The computer has the last 3 letters of the word
    def decideIfPlacingCase2Len4(self, word): 
        row = self.tryThisRowCol[0]
        col = self.tryThisRowCol[1]
        letter2 = word[1]
        letter3 = word[2]
        letter4 = word[3]
        print(letter2, letter3, letter4)
        if row+3 < 15 and row-3 > -1 and col+3 < 15 and col-3 > -1:
            #PLACE BELOW
            if self.app.board.textBoard[row+1][col] == "-" and self.app.board.textBoard[row+2][col] == "-" and self.app.board.textBoard[row+3][col] == "-" \
                and self.app.board.textBoard[row+1][col+1] == "-" and self.app.board.textBoard[row+1][col-1] == "-" \
                and self.app.board.textBoard[row+2][col+1] == "-" and self.app.board.textBoard[row+2][col-1] == "-" \
                and self.app.board.textBoard[row+3][col+1] == "-" and self.app.board.textBoard[row+3][col-1] == "-" \
                and self.app.board.textBoard[row-1][col] == "-":
                self.app.board.textBoard[row+1][col] = letter2
                self.app.board.textBoard[row+2][col] = letter3
                self.app.board.textBoard[row+3][col] = letter4
                self.clickList.append((row+1, col))
                self.clickList.append((row+2, col))
                self.clickList.append((row+3, col))
                self.setUpDrawCase2a(letter2, letter3, letter4)
                return True
            #PLACE RIGHT
            elif self.app.board.textBoard[row][col+1] == "-" and self.app.board.textBoard[row][col+2] == "-" and self.app.board.textBoard[row][col+3] == "-" \
                and self.app.board.textBoard[row-1][col+1] == "-" and self.app.board.textBoard[row+1][col+1] == "-" \
                and self.app.board.textBoard[row-1][col+2] == "-" and self.app.board.textBoard[row+1][col+2] == "-" \
                and self.app.board.textBoard[row-1][col+3] == "-" and self.app.board.textBoard[row+1][col+3] == "-" \
                and self.app.board.textBoard[row][col-1] == "-":
                self.app.board.textBoard[row][col+1] = letter2
                self.app.board.textBoard[row][col+2] = letter3
                self.app.board.textBoard[row][col+3] = letter4
                self.clickList.append((row, col+1))
                self.clickList.append((row, col+2))
                self.clickList.append((row, col+3))
                self.setUpDrawCase2a(letter2, letter3, letter4)
                return True
            else:
                return False
        else:
            return False

    # Determines whether computer can place a word of case 1, len 4, meaning that
    # The computer has the first 3 letters of the word
    def decideIfPlacingCase1Len4(self, word): 
        row = self.tryThisRowCol[0]
        col = self.tryThisRowCol[1]
        print("row", str(row), "col", str(col))
        letter1 = word[0]
        letter2 = word[1]
        letter3 = word[2]
        if row+3 < 15 and row-3 > -1 and col+3 < 15 and col-3 > -1:
            #PLACE ABOVE
            if self.app.board.textBoard[row-3][col] == "-" and self.app.board.textBoard[row-2][col] == "-" and self.app.board.textBoard[row-1][col] == "-" \
                and self.app.board.textBoard[row-3][col+1] == "-" and self.app.board.textBoard[row-3][col-1] == "-" \
                and self.app.board.textBoard[row-2][col+1] == "-" and self.app.board.textBoard[row-2][col-1] == "-" \
                and self.app.board.textBoard[row-1][col+1] == "-" and self.app.board.textBoard[row-1][col-1] == "-" \
                and self.app.board.textBoard[row+1][col] == "-":
                self.app.board.textBoard[row-3][col] = letter1
                self.app.board.textBoard[row-2][col] = letter2
                self.app.board.textBoard[row-1][col] = letter3
                print("lettersappendingToTXTB:", letter1, letter2, letter3)
                self.clickList.append((row-3, col))
                self.clickList.append((row-2, col))
                self.clickList.append((row-1, col))
                self.setUpDrawCase2a(letter1, letter2, letter3)
                return True
            #PLACE LEFT
            elif self.app.board.textBoard[row][col-3] == "-" and self.app.board.textBoard[row][col-2] == "-" and self.app.board.textBoard[row][col-1] == "-" \
                and self.app.board.textBoard[row-1][col-3] == "-" and self.app.board.textBoard[row+1][col-3] == "-" \
                and self.app.board.textBoard[row-1][col-2] == "-" and self.app.board.textBoard[row+1][col-2] == "-" \
                and self.app.board.textBoard[row-1][col-1] == "-" and self.app.board.textBoard[row+1][col-1] == "-" \
                and self.app.board.textBoard[row][col+1] == "-":
                self.app.board.textBoard[row][col-3] = letter1
                self.app.board.textBoard[row][col-2] = letter2
                self.app.board.textBoard[row][col-1] = letter3
                print("lettersappendingToTXTB:", letter1, letter2, letter3)
                self.clickList.append((row, col-3))
                self.clickList.append((row, col-2))
                self.clickList.append((row, col-1))
                self.setUpDrawCase2a(letter1, letter2, letter3)
                return True
            else:
                print("not append worhty")
                return False 
        else:
            print("not append worthy")
            return False

    # Determines whether computer can place a word of case 3, len 3, meaning that
    # The computer has the first and last letter of the word
    def decideIfPlacingCase3(self, word):
        row = self.tryThisRowCol[0]
        col = self.tryThisRowCol[1]
        letter1 = word[0]
        letter3 = word[2]
        if row+2 < 15 and row-2 > -1 and col+2 < 15 and col-2 > -1:
            #PLACE ONE TILE ABOVE & ONE TILE BELOW
            if self.app.board.textBoard[row-1][col] == "-" and self.app.board.textBoard[row+1][col] == "-" \
                and self.app.board.textBoard[row-2][col] == "-" and self.app.board.textBoard[row+2][col] == "-" \
                and self.app.board.textBoard[row+1][col+1] == "-" and self.app.board.textBoard[row+1][col-1] == "-" \
                and self.app.board.textBoard[row-1][col+1] == "-" and self.app.board.textBoard[row-1][col-1] == "-":
                self.app.board.textBoard[row-1][col] = letter1
                self.app.board.textBoard[row+1][col] = letter3
                self.clickList.append((row-1, col))
                self.clickList.append((row+1, col))
                self.setUpDrawCase1a(letter1, letter3)
                return True
            #PLACE ONE TILE LEFT & ONE TILE RIGHT
            elif self.app.board.textBoard[row][col-1] == "-" and self.app.board.textBoard[row][col+1] == "-" \
                and self.app.board.textBoard[row][col-2] == "-" and self.app.board.textBoard[row][col+2] == "-" \
                and self.app.board.textBoard[row+1][col+1] == "-" and self.app.board.textBoard[row+1][col-1] == "-" \
                and self.app.board.textBoard[row-1][col+1] == "-" and self.app.board.textBoard[row-1][col-1] == "-":
                self.app.board.textBoard[row][col-1] = letter1
                self.app.board.textBoard[row][col+1] = letter3
                self.clickList.append((row, col-1))
                self.clickList.append((row, col+1))
                self.setUpDrawCase1a(letter1, letter3)
                return True
            else:
                return False
        else:
            return False

    # Determines whether computer can place a word of case 2, len 3, meaning that
    # The computer has the last 2 letters of the word
    def decideIfPlacingCase2(self, word): #have last 2 letters
        row = self.tryThisRowCol[0]
        col = self.tryThisRowCol[1]
        letter2 = word[1]
        letter3 = word[2]
        if row+2 < 15 and row-2 > -1 and col+2 < 15 and col-2 > -1:
            #PLACE BELOW
            if self.app.board.textBoard[row+2][col] == "-" and self.app.board.textBoard[row+1][col] == "-" \
                and self.app.board.textBoard[row+2][col+1] == "-" and self.app.board.textBoard[row+2][col-1] == "-" \
                and self.app.board.textBoard[row+1][col+1] == "-" and self.app.board.textBoard[row+1][col-1] == "-" \
                and self.app.board.textBoard[row-1][col] == "-":
                self.app.board.textBoard[row+1][col] = letter2
                self.app.board.textBoard[row+2][col] = letter3
                self.clickList.append((row+1, col))
                self.clickList.append((row+2, col))
                self.setUpDrawCase1a(letter2, letter3)
                return True
            #PLACE RIGHT
            elif self.app.board.textBoard[row][col+1] == "-" and self.app.board.textBoard[row][col+2] == "-" \
                and self.app.board.textBoard[row-1][col+1] == "-" and self.app.board.textBoard[row-1][col+2] == "-" \
                and self.app.board.textBoard[row+1][col+1] == "-" and self.app.board.textBoard[row+1][col+2] == "-" \
                and self.app.board.textBoard[row][col-1] == "-":
                self.app.board.textBoard[row][col+1] = letter2
                self.app.board.textBoard[row][col+2] = letter3
                self.clickList.append((row, col+1))
                self.clickList.append((row, col+2))
                self.setUpDrawCase1a(letter2, letter3)
                return True
            else:
                return False
        else:
            return False

    # Determines whether computer can place a word of case 1, len 3, meaning that
    # The computer has the first 2 letters of the word
    def decideIfPlacingCase1(self, word):   
        row = self.tryThisRowCol[0]
        col = self.tryThisRowCol[1]
        letter1 = word[0]
        letter2 = word[1]
        if row+2 < 15 and row-2 > -1 and col+2 < 15 and col-2 > -1:
            #PLACE ABOVE
            if self.app.board.textBoard[row-2][col] == "-" and self.app.board.textBoard[row-1][col] == "-" \
                and self.app.board.textBoard[row-2][col+1] == "-" and self.app.board.textBoard[row-2][col-1] == "-" \
                and self.app.board.textBoard[row-1][col+1] == "-" and self.app.board.textBoard[row-1][col-1] == "-" \
                and self.app.board.textBoard[row+1][col] == "-":
                #update textboard with new stuff
                self.app.board.textBoard[row-2][col] = letter1
                self.app.board.textBoard[row-1][col] = letter2
                #draw them via adding them to clicklist
                self.clickList.append((row-2, col))
                self.clickList.append((row-1, col))
                self.setUpDrawCase1a(letter1, letter2)
                return True 
            #PLACE LEFT
            elif self.app.board.textBoard[row][col-2] == "-" and self.app.board.textBoard[row][col-1] == "-" \
                and self.app.board.textBoard[row-1][col-1] == "-" and self.app.board.textBoard[row-1][col-2] == "-" \
                and self.app.board.textBoard[row+1][col-1] == "-" and self.app.board.textBoard[row+1][col-2] == "-" \
                and self.app.board.textBoard[row][col+1] == "-":
                self.app.board.textBoard[row][col-2] = letter1
                self.app.board.textBoard[row][col-1] = letter2
                self.clickList.append((row, col-2))
                self.clickList.append((row, col-1))
                self.setUpDrawCase1a(letter1, letter2)
                return True
            else:
                return False #ie go to next word
        else:
            return False
    
    def setUpDrawCase1a(self, letter1, letter2): 
        #Appending tiles, with their location and point values, for length 3 to then draw them
        self.app.board.finalizedTilesToDraw.append( (self.clickList[0][0], self.clickList[0][1], letter1, self.bag.letterValuesDict[letter1]) )
        self.app.board.finalizedTilesToDraw.append( (self.clickList[1][0], self.clickList[1][1], letter2, self.bag.letterValuesDict[letter2]) )
        

    def setUpDrawCase2a(self, letter1, letter2, letter3): 
        #Appending tiles, with their location and point values, for length 4 to then draw them
        self.app.board.finalizedTilesToDraw.append( (self.clickList[0][0], self.clickList[0][1], letter1, self.bag.letterValuesDict[letter1]) )
        self.app.board.finalizedTilesToDraw.append( (self.clickList[1][0], self.clickList[1][1], letter2, self.bag.letterValuesDict[letter2]) )
        self.app.board.finalizedTilesToDraw.append( (self.clickList[2][0], self.clickList[2][1], letter3, self.bag.letterValuesDict[letter3]) )

    def setUpDrawCase3a(self, letter1, letter2, letter3, letter4):
        #Appending tiles
        self.app.board.finalizedTilesToDraw.append( (self.clickList[0][0], self.clickList[0][1], letter1, self.bag.letterValuesDict[letter1]) )
        self.app.board.finalizedTilesToDraw.append( (self.clickList[1][0], self.clickList[1][1], letter2, self.bag.letterValuesDict[letter2]) )
        self.app.board.finalizedTilesToDraw.append( (self.clickList[2][0], self.clickList[2][1], letter3, self.bag.letterValuesDict[letter3]) )
        self.app.board.finalizedTilesToDraw.append( (self.clickList[3][0], self.clickList[3][1], letter4, self.bag.letterValuesDict[letter4]) )
        





# Button class holds specifications for drawing buttons and a method for drawing the button
class Button(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.isClickedOn = False
        self.fillColor = "#DEB887"
        self.endX = self.x+2*self.size
        self.endY = self.y+0.5*self.size

    def drawButton(self, canvas):
        canvas.create_rectangle(self.x, self.y, self.endX, self.endY,
                                fill=self.fillColor, width=3)
        canvas.create_text((self.x+self.x+2*self.size)/2, self.y+(self.size/3.5), 
                        text="Place My Word",fill="brown",font="Helvetica 15 bold")
    
    def updateFill(self):
        if self.isClickedOn == True:
            self.fillColor = "#42a980"
        else:
            self.fillColor = "#DEB887"

class PlaceWordButton(Button):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
        self.isClickedOn = False
        self.fillColor = "#DEB887"
        self.endX = self.x + 2*self.size
        self.endY = self.y + 0.35*self.size
    
    def drawButton(self, canvas):
        canvas.create_rectangle(self.x, self.y, self.endX, self.endY,
                                fill=self.fillColor, width=3)
        canvas.create_text((self.x+self.x+2*self.size)/2, self.y+(self.size/5.5), 
                        text="Place Word",fill="brown",font="Helvetica 15 bold")

class BackButton(Button):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
        self.isClickedOn = False
        self.fillColor = "#DEB887"
        self.endX = self.x + self.size
        self.endY = self.y + self.size
    
    def drawButton(self, canvas):
        canvas.create_rectangle(self.x, self.y, self.endX, self.endY,
                                fill=self.fillColor, width=3)
        canvas.create_text(self.x + (self.size/2), self.y+(self.size/2), text="<--", fill="brown",font="Helvetica 15 bold")

class InstructionsButton(Button):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
        self.isClickedOn = False
        self.fillColor = "#DEB887"
        self.endX = self.x + self.size
        self.endY = self.y + self.size
    
    def drawButton(self, canvas):
        canvas.create_oval(self.x, self.y, self.endX, self.endY, fill=self.fillColor, width=3)
        canvas.create_text(self.x + (self.size/2), self.y+(self.size/2), text="i", fill="brown",font="Helvetica 15 bold")

class ShuffleAndSkipButton(Button):
    def __init__(self, x, y, size, text):
        super().__init__(x, y, size)
        self.text = text
        self.isClickedOn = False
        self.fillColor = "#DEB887"
        self.endX = self.x + 1.5*self.size
        self.endY = self.y + 0.5*self.size
    
    def drawButton(self, canvas):
        canvas.create_rectangle(self.x, self.y, self.endX, self.endY,
                                fill=self.fillColor, width=3)
        canvas.create_text( (self.x + self.x+self.size)/2 + self.x/40,  self.y+(self.size/4.5),
                            text=self.text, fill="brown", font="Helvetica 15 bold")



# GameComputerMode is where the game essentially "occurs", especially via the method computerCheckGame
# It draws everything and moves players around as well. This Game Mode is for the Computer/AI mode
class GameComputerMode(Mode):
    def appStarted(mode):
        mode.b1 = Bag(mode)
        mode.createPlayers()
        mode.setTileAttributes() 
        mode.createButtons()
        mode.createBoard()
        mode.gameOver = False
        mode.hasSkippedTurn = False
        mode.help = False
    
    def createBoard(mode):
        mode.board = Board(mode)           
    
    def createButtons(mode):
        mode.myWordButton = Button(mode.width/4.5 + mode.width/1.9, 
                            mode.height/25 + (8.25*(mode.height/10)), 
                            mode.width/10)
        
        mode.backButton = BackButton(mode.width/20, mode.height/20, mode.width/20)
        mode.instructionsButton = InstructionsButton(mode.width - mode.width/10, mode.height/20, mode.width/20)
        mode.shuffleButton = ShuffleAndSkipButton(mode.width-mode.width/6, mode.height/25 + (7.25*mode.height/10), mode.width/15, text="Shuffle")
        mode.skipButton = ShuffleAndSkipButton(mode.width-mode.width/6, mode.height/25 + (7.75*mode.height/10), mode.width/15, text="Skip")

    def setTileAttributes(mode):
        mode.tileSize = mode.width/15        
    
    # Initialize the players, one of which is a Computer in this game mode
    def createPlayers(mode):
        #mode.p1 = Player(mode, "Human", mode.b1)
        #mode.p3 = Computer(mode, "Computer", mode.b1)

        coolp1 = mode.app.middleMode.getPlayer1Name()
        coolp2 = mode.app.middleMode.getPlayer2Name()
        if coolp1 == "Player 1" and coolp2 == "Player 2":
            mode.p1 = Player(mode, coolp1, mode.b1)
            mode.p2 = Player(mode, coolp2, mode.b1)
        else:
            mode.p1 = Player(mode, coolp1, mode.b1)
            mode.p2 = Computer(mode, coolp2, mode.b1)

        mode.playerList = [mode.p1, mode.p2]
        mode.currentPlayer = mode.playerList[0]
    
    def keyPressed(mode, event):
        if(event.key == "Space"):
            mode.app.setActiveMode(mode.app.splashScreenMode)
        elif(event.key == "P"): 
            mode.passYourTurn()
        elif(event.key == "S"): 
            mode.shuffleYourRack()
        elif(event.key == "r"):
            if mode.gameOver == True:
                mode.appStarted()
                mode.app.setActiveMode(mode.app.splashScreenMode)
        elif(event.key == "h"):
            mode.help = True
            if mode.currentPlayer.name != "Computer":
                mode.currentPlayer.helpp()
                #mode.app.setActiveMode(mode.app.gameMode)
                #mode.getNextPlayer()
                #mode.help = False
        elif(event.key == "d"):
            mode.help = False

    # Pass your turn ; gets next player
    def passYourTurn(mode):
        mode.getNextPlayer()
    
    # Shuffle your rack ; gets next player
    def shuffleYourRack(mode):
        for tile in mode.currentPlayer.rack.rackList:
            mode.currentPlayer.rack.takeFromRack(tile) #gets rid of all letters in rack
        mode.currentPlayer.rack.replenishRack()
        mode.getNextPlayer()
    
    def mousePressed(mode, event):
        # Detect click on tile
        if mode.gameOver == False:
            for tile in mode.currentPlayer.rack.rackList:
                if(tile.x <= event.x <= tile.x+mode.tileSize) and (tile.y <= event.y <= tile.y+mode.tileSize):
                    tile.isClickedOn = not tile.isClickedOn
                    tile.updateFill()
                    # create selected tiles
                    mode.createSelectedTilesList(tile)
            
            mode.checkMyWordClicking(event.x, event.y)
            mode.createBoardClickList(event.x, event.y)
            mode.checkBackButtonInstructionsClicking(event.x, event.y)

    def checkBackButtonInstructionsClicking(mode, mouseX, mouseY):
        if (mode.backButton.x <= mouseX <= mode.backButton.endX) and (mode.backButton.y <= mouseY <= mode.backButton.endY):
            mode.backButton.isClickedOn = not mode.backButton.isClickedOn
            mode.app.setActiveMode(mode.app.splashScreenMode)
            mode.appStarted()
        
        if (mode.instructionsButton.x <= mouseX <= mode.instructionsButton.endX) and (mode.instructionsButton.y <= mouseY <= mode.instructionsButton.endY):
            mode.instructionsButton.isClickedOn = not mode.backButton.isClickedOn
            mode.app.setActiveMode(mode.app.instructionsMode)
        
        if (mode.shuffleButton.x <= mouseX <= mode.shuffleButton.endX) and (mode.shuffleButton.y <= mouseY <= mode.shuffleButton.endY):
            mode.shuffleButton.isClickedOn = not mode.shuffleButton.isClickedOn
            mode.shuffleYourRack()
        
        if (mode.skipButton.x <= mouseX <= mode.skipButton.endX) and (mode.skipButton.y <= mouseY <= mode.skipButton.endY):
            mode.skipButton.isClickedOn = not mode.skipButton.isClickedOn
            mode.passYourTurn()
    
    # Check if Place Word Button is being clicked
    def checkMyWordClicking(mode, mouseX, mouseY):
        if (mode.myWordButton.x <= mouseX <= mode.myWordButton.endX) and (mode.myWordButton.y <= mouseY <= mode.myWordButton.endY):
            mode.myWordButton.isClickedOn = not mode.myWordButton.isClickedOn
            mode.myWordButton.updateFill()
            
            # Go through click list and set selectedPositionIsValid to false if there's a 
            # tile not connected to the others that are already on the board
            for (row, col) in mode.currentPlayer.clickList:
                if row-1==-1 and col-1==-1:
                    mode.currentPlayer.selectedPositionIsValid = False
                    mode.checkGame()
                    return
                    continue
                elif row-1==-1 and col+1==15:
                    mode.currentPlayer.selectedPositionIsValid = False
                    mode.checkGame()
                    return
                    continue
                elif row+1==15 and col-1==-1:
                    mode.currentPlayer.selectedPositionIsValid = False
                    mode.checkGame()
                    return
                    continue
                elif row+1==15 and col+1==15:
                    mode.currentPlayer.selectedPositionIsValid = False
                    mode.checkGame()
                    return
                    continue
                elif col-1 == -1 and (mode.board.textBoard[row-1][col] == "-" or (row-1, col) in mode.currentPlayer.clickList) \
                    and (mode.board.textBoard[row+1][col] == "-" or (row+1, col) in mode.currentPlayer.clickList) \
                    and (mode.board.textBoard[row][col+1] == "-" or (row, col+1) in mode.currentPlayer.clickList):
                    mode.currentPlayer.selectedPositionIsValid = False
                    continue
                elif col+1 == 15 and (mode.board.textBoard[row-1][col] == "-" or (row-1, col) in mode.currentPlayer.clickList) \
                    and (mode.board.textBoard[row+1][col] == "-" or (row+1, col) in mode.currentPlayer.clickList) \
                    and (mode.board.textBoard[row][col-1] == "-" or (row, col-1) in mode.currentPlayer.clickList):
                    mode.currentPlayer.selectedPositionIsValid = False
                    continue
                elif row-1 == -1 and (mode.board.textBoard[row][col+1] == "-" or (row, col+1) in mode.currentPlayer.clickList) \
                    and (mode.board.textBoard[row][col-1] == "-" or (row, col-1) in mode.currentPlayer.clickList) \
                    and (mode.board.textBoard[row+1][col] == "-" or (row+1, col) in mode.currentPlayer.clickList):
                    mode.currentPlayer.selectedPositionIsValid = False
                    continue
                elif row+1 == 15 and (mode.board.textBoard[row][col+1] == "-" or (row, col+1) in mode.currentPlayer.clickList) \
                    and (mode.board.textBoard[row][col-1] == "-" or (row, col-1) in mode.currentPlayer.clickList) \
                    and (mode.board.textBoard[row-1][col] == "-" or (row-1, col) in mode.currentPlayer.clickList):
                    mode.currentPlayer.selectedPositionIsValid = False
                    continue
                else:
                    mode.currentPlayer.selectedPositionIsValid = True
                    break
            
            # If there's no tile that makes valid location true, go automatically to
            # checkGame, where the game is run, with location validity as False
            if mode.currentPlayer.selectedPositionIsValid == False:
                mode.checkGame()
                return
            
            # ONLY IF valid location is true, then form the word
            mode.board.formPossibleWord()
            # After forming it, update position validity again
            mode.board.updateSelectedPositionIsValid()
            for possibleWord in mode.currentPlayer.wordList:
                print("eeek")
                print(possibleWord)
                w1 = Word(possibleWord, mode.b1)
                if w1.checkWordInDictionary() == True:
                    print("in true")
                    mode.currentPlayer.selectedWordDictIsValid = True
                    print("dict check", mode.currentPlayer.selectedWordDictIsValid)
                else:
                    print("in false")
                    mode.currentPlayer.selectedWordDictIsValid = False
                    print("dict check", mode.currentPlayer.selectedWordDictIsValid)
                    break
            print(mode.currentPlayer.wordList)
            mode.checkGame()
    
    # Checks whether human's position placement is valid
    # If location or word is invalid, then reset everything (tiles in rackList
    # that have been placed need to go back to rack), draw error message, 
    # and let player try again.
    # Else if both are TRUE, then reset everything / call next player ie computer
    def checkGame(mode):
        if mode.currentPlayer.selectedPositionIsValid == False:
            mode.currentPlayer.selectedTiles = []
            mode.currentPlayer.possibleWord = ""
            mode.currentPlayer.wordList = []
            for tile in mode.currentPlayer.rack.rackList:
                    tile.isClickedOn = False
                    tile.updateFill()
            mode.currentPlayer.clickList = []

            for (row, col) in mode.board.rowscolsToRemoveIfPlayerMessesUp:
                (x0, y0, x1, y1) = mode.board.getCellBounds(row, col)
                stringLetter = mode.board.textBoard[row][col]
                pointVal = mode.b1.letterValuesDict[stringLetter]
                while (row, col, stringLetter, pointVal) in mode.board.finalizedTilesToDraw:
                    mode.board.finalizedTilesToDraw.remove((row, col, stringLetter, pointVal))

            for (row, col) in mode.board.rowscolsToRemoveIfPlayerMessesUp:
                mode.board.textBoard[row][col] = "-"
            mode.board.rowscolsToRemoveIfPlayerMessesUp = []

            mode.board.okayToDrawTiles = True
            mode.myWordButton.isClickedOn = False
            mode.myWordButton.updateFill() 
        elif mode.currentPlayer.selectedWordDictIsValid == False:
            mode.currentPlayer.selectedTiles = []
            mode.currentPlayer.possibleWord = ""
            mode.currentPlayer.wordList = []
            for tile in mode.currentPlayer.rack.rackList:
                    tile.isClickedOn = False
                    tile.updateFill()
            mode.currentPlayer.clickList = []

            for (row, col) in mode.board.rowscolsToRemoveIfPlayerMessesUp:
                (x0, y0, x1, y1) = mode.board.getCellBounds(row, col)
                stringLetter = mode.board.textBoard[row][col]
                pointVal = mode.b1.letterValuesDict[stringLetter]
                while (row, col, stringLetter, pointVal) in mode.board.finalizedTilesToDraw:
                    mode.board.finalizedTilesToDraw.remove((row, col, stringLetter, pointVal))

            for (row, col) in mode.board.rowscolsToRemoveIfPlayerMessesUp:
                mode.board.textBoard[row][col] = "-"
            mode.board.rowscolsToRemoveIfPlayerMessesUp = []

            mode.board.okayToDrawTiles = True
            mode.myWordButton.isClickedOn = False
            mode.myWordButton.updateFill()
        # both are true, call next player
        else:
            mode.calculatePlayerScore()
            for tile in mode.currentPlayer.rack.rackList:
                    tile.isClickedOn = False
                    tile.updateFill()
            for tile in mode.currentPlayer.selectedTiles:
                mode.currentPlayer.rack.takeFromRack(tile)
            mode.currentPlayer.rack.replenishRack()
            mode.currentPlayer.selectedTiles = []
            mode.currentPlayer.possibleWord = ""
            mode.currentPlayer.wordList = []
            mode.currentPlayer.clickList = []
            mode.board.rowscolsToRemoveIfPlayerMessesUp = []
            mode.board.okayToDrawTiles = True
            mode.myWordButton.isClickedOn = False
            mode.myWordButton.updateFill() 
            mode.currentPlayer.selectedPositionIsValid = None
            mode.currentPlayer.selectedWordDictIsValid = None
            if(mode.b1.currentAmtOfTiles > 0):
                if (type(mode.playerList[0]) == Computer) or (type(mode.playerList[1]) == Computer):
                    mode.getNextPlayer()
                else:
                    mode.getNextPlayer()
                    mode.app.setActiveMode(mode.app.waitForNextPlayerMode)
            else:
                mode.gameOver = True
                self.app.hasSkippedTurn = False
    
    # Calculate human score
    def calculatePlayerScore(mode):
        listOfLetters = []
        special = []
        seen = [] 
        for possibleWord in mode.currentPlayer.wordList:
            score = 0
            if possibleWord in seen:
                continue
            seen.append(possibleWord)
            for (row, col) in mode.currentPlayer.clickList:
                letter = mode.board.textBoard[row][col]
                listOfLetters.append(letter)
                if (row, col) in mode.board.doubleLetterLocations:
                    score += 2*mode.b1.letterValuesDict[letter]
                elif (row, col) in mode.board.tripleLetterLocations:
                    score += 3*mode.b1.letterValuesDict[letter]
                else:
                    score += mode.b1.letterValuesDict[letter]
                if (row, col) in mode.board.doubleWordLocations:
                    special.append("dw")
                elif(row, col) in mode.board.tripleWordLocations:
                    special.append("tw")
            #find missing letters
            for c in possibleWord:
                if c not in listOfLetters:
                    score = score + mode.b1.letterValuesDict[c]
            #do dw and tw calcs
            for thing in special:
                if thing == "dw":
                    score = score*2
                elif thing == "tw":
                    score = score*3
            mode.currentPlayer.score += score
        
    # Create board clickList by detecting where the user clicks and 
    # don't add if Place Word has already been clicked
    def createBoardClickList(mode, mouseX, mouseY):
        # Don't want to add to clickList if ur click is occupied in textBoard
        (row, col) = mode.board.getCell(mouseX, mouseY)
        if mode.board.textBoard[row][col] != "-":
            mode.board.okayToDrawTiles = False

        if len(mode.currentPlayer.clickList) == len(mode.currentPlayer.selectedTiles) \
            and len(mode.currentPlayer.clickList) != 0 and len(mode.currentPlayer.selectedTiles) != 0:
            mode.board.okayToDrawTiles = False
        elif((row != -1 and col != -1) and ((row,col) not in mode.currentPlayer.clickList) \
            and len(mode.currentPlayer.selectedTiles) > 0):
            mode.currentPlayer.clickList.append( (row, col) )
            mode.board.rowscolsToRemoveIfPlayerMessesUp.append((row, col)) 
        mode.board.drawSelectedTilesOnBoard() 
        ###TESTS###
        print(mode.currentPlayer.clickList) #@@printcheck
        #mode.board.updateSelectedPositionIsValid()
        print(mode.currentPlayer.selectedPositionIsValid) #@printum
        #print(mode.board.textBoard)
        
        
    # create selected tiles list
    def createSelectedTilesList(mode, tile):           
        if((tile.isClickedOn) == True) and (tile in mode.currentPlayer.selectedTiles)\
            and (len(mode.currentPlayer.selectedTiles) == len(mode.currentPlayer.clickList)):
            tile.currentFill = "#948f8b"
            pass
        elif(tile.isClickedOn == True):
            mode.currentPlayer.selectedTiles.append(tile)
        elif((tile.isClickedOn) == False) and (tile in mode.currentPlayer.selectedTiles)\
            and (len(mode.currentPlayer.selectedTiles) == len(mode.currentPlayer.clickList)):
            tile.currentFill = "#948f8b"
            pass
        elif((tile.isClickedOn == False) and (tile in mode.currentPlayer.selectedTiles)):
            mode.currentPlayer.selectedTiles.remove(tile)

    def getNextPlayer(mode):
        if mode.playerList.index(mode.currentPlayer) != (len(mode.playerList)-1):
            mode.currentPlayer = mode.playerList[mode.playerList.index(mode.currentPlayer)+1]
        else:
            mode.currentPlayer = mode.playerList[0]
        if mode.currentPlayer.name == "Computer":
            print("in getNextPl yo")
            mode.currentPlayer.theComputerCheckGame()

        mode.thingsThatChangeOnNextPlayer()
    
    def thingsThatChangeOnNextPlayer(mode):
        mode.myWordButton.fillColor = "#DEB887"
        #mode.help = False

    def redrawAll(mode, canvas):
        mode.drawBackground(canvas)
        mode.drawWhoseTurn(canvas)
        mode.drawPlayerRack(canvas)
        if(len(mode.currentPlayer.rack.rackList) == 7):
            mode.drawTilesOnRack(canvas)
        mode.drawSelectedTiles(canvas)
        mode.drawButtons(canvas)
        mode.drawDictionaryCheckMsg(canvas)
        mode.drawBoard(canvas)
        mode.board.drawFinalTilesToStay(canvas)
        mode.drawPlayerScore(canvas)
        mode.drawBagAmount(canvas)
        mode.drawSkippedTurnMsg(canvas)
        mode.drawMultiplierInfo(canvas)
        mode.drawHelp(canvas)
        mode.drawGameOver(canvas)
    
    def drawHelp(mode, canvas):
        height=0
        if mode.currentPlayer.name != "Computer" and mode.help == True:
            canvas.create_rectangle(0, 0, mode.width, mode.height, fill="white")
            for word in mode.currentPlayer.sortedListOfPossibleWords:
                hm = mode.currentPlayer.findPossibleRowColToPlace(word)
                if hm == "nope" or hm == "pick a word":
                    continue
                else:
                    canvas.create_text(100, height, text=word)
                height = height + 25
    
    # Draw multiplier information
    def drawMultiplierInfo(mode, canvas):
        rectX = mode.backButton.x
        rectY = mode.shuffleButton.y - mode.height/20
        width = mode.width/10
        height = mode.width/10
        canvas.create_rectangle(rectX, rectY, rectX+width, rectY+height, fill="#DEB887", width=3)
        canvas.create_text((rectX+rectX+width)/2, rectY - mode.height/60, text="Multipliers", 
                            fill="black", font="Helvetica 13 bold") 
        #doubleletter
        dlX = rectX + mode.width/80
        dlY = rectY + mode.width/80
        size = 10
        canvas.create_rectangle(dlX, dlY, dlX+size, dlY+size, fill="#90f3f1")
        canvas.create_text(dlX+40, dlY+5, text="2x Letter", font="Helvetica 10")

        #triple letter
        tlY = dlY + mode.width/50
        canvas.create_rectangle(dlX, tlY, dlX+size, tlY+size, fill="blue")
        canvas.create_text(dlX+40, tlY+5, text="3x Letter", font="Helvetica 10")

        #double word
        dwY = tlY + mode.width/50
        canvas.create_rectangle(dlX, dwY, dlX+size, dwY+size, fill="#ff8c69")
        canvas.create_text(dlX+40, dwY+5, text="2x Word", font="Helvetica 10")

        #triple word
        twY = dwY + mode.width/50
        canvas.create_rectangle(dlX, twY, dlX+size, twY+size, fill="red")
        canvas.create_text(dlX+40, twY+5, text="3x Word", font="Helvetica 10")
    
    def drawGameOver(mode, canvas):
        if mode.gameOver == True:
            canvas.create_rectangle(0, 0, mode.width, mode.height, fill='brown')
            canvas.create_text(mode.width/2, mode.height/2, text="GAME OVER", font="Helvetica 25 bold")
            if mode.p1.score > mode.p2.score:
                winnerMsg = mode.p1.name + " wins with " + str(mode.p1.score) + " points!"  
                canvas.create_text(mode.width/2, mode.height/2 + 100, text=winnerMsg, font="Helvetica 25 bold")
            else:
                winnerMsg2 = mode.p2.name + " wins with " + str(mode.p2.score) + " points!"  
                canvas.create_text(mode.width/2, mode.height/2 + 100, text=winnerMsg2, font="Helvetica 25 bold")
            canvas.create_text(mode.width/2, mode.height/2 + 35, text="Press 'r' to restart", font="Helvetica 25 bold")
    
    def drawBagAmount(mode, canvas):
        bagAmtX = (mode.myWordButton.x + mode.myWordButton.endX)//2
        bagAmtY = mode.myWordButton.endY + mode.height/15
        bagText = "Current Bag Amt: " + str(mode.b1.currentAmtOfTiles)
        canvas.create_text(bagAmtX, bagAmtY, text=bagText)
    
    def drawPlayerScore(mode, canvas):
        scoreX = (mode.myWordButton.x + mode.myWordButton.endX)//2
        scoreY = mode.myWordButton.endY + mode.height/40
        otherScoreY = mode.myWordButton.endY + mode.height/22
        currentPlName = mode.currentPlayer.name
        canvas.create_text(scoreX, scoreY, 
                        text= str(currentPlName) + "'s Score: " + str(mode.currentPlayer.score))
        if mode.playerList.index(mode.currentPlayer) == 0: #so other player is 1
            displayOtherScore = mode.playerList[1].score
            otherName = mode.playerList[1].name
            canvas.create_text(scoreX, otherScoreY, 
                        text=str(otherName) + "'s Score: " + str(displayOtherScore))
        elif mode.playerList.index(mode.currentPlayer) == 1:
            displayOtherScore = mode.playerList[0].score
            otherName = mode.playerList[0].name
            canvas.create_text(scoreX, otherScoreY, 
                        text=str(otherName) + "'s Score: " + str(displayOtherScore))
        
        
    def drawBoard(mode, canvas):
        mode.board.drawBoard(canvas)
        #if(len(mode.currentPlayer.clickList) > 0):
        if mode.board.okayToDrawTiles == True:
            mode.board.drawSelectedTilesOnBoard()
    
    def drawSkippedTurnMsg(mode, canvas):
        if mode.hasSkippedTurn == True:
            print("ACTUALLY EVER IN HERE?")
            wordX = mode.width/2
            wordY = mode.myWordButton.endY + mode.height/15
            canvas.create_text(wordX, wordY, 
                text="The computer has skipped its turn.", 
                fill="black",font="Helvetica 15 bold")

    # draws location validity/word validity error messages when assoc
    # variables are False
    def drawDictionaryCheckMsg(mode, canvas):
        msgX = mode.width/2
        msgY = mode.myWordButton.endY + mode.height/50
        msgY2 = mode.myWordButton.endY + mode.height/20

        if(mode.currentPlayer.selectedPositionIsValid == False):
            canvas.create_text(msgX, msgY, 
                text="This location isn't valid. Pick a new one.", 
                fill="black",font="Helvetica 15 bold")
            canvas.create_text(msgX, msgY2, 
                text= "This message will disappear once you pick a valid position!", 
                fill="black",font="Helvetica 10 bold")
        elif (mode.currentPlayer.selectedWordDictIsValid == False):
            canvas.create_text(msgX, msgY, 
                text="Location fine. Word invalid. Pick a new one.", 
                fill="black",font="Helvetica 15 bold")
            canvas.create_text(msgX, msgY2, 
                text= "This message will disappear once you pick a valid word!", 
                fill="black",font="Helvetica 10 bold")
        else: #both true
            pass
        
    
    def drawButtons(mode, canvas):
        mode.myWordButton.drawButton(canvas)
        mode.backButton.drawButton(canvas)
        mode.instructionsButton.drawButton(canvas)
        mode.shuffleButton.drawButton(canvas)
        mode.skipButton.drawButton(canvas)
        
    def drawSelectedTiles(mode, canvas):
        textX = mode.width/4.625
        textY = mode.height/25 + (8.5*(mode.height/10))
        canvas.create_text(textX, textY, text="Selected Tiles: ", 
                            fill="black",font="Helvetica 20 bold")
        startTileX = mode.width/3.25
        startTileY = mode.height/25 + (8.25*(mode.height/10))
        size = mode.width/20
        for tile in mode.currentPlayer.selectedTiles:
            if mode.currentPlayer.selectedTiles.index(tile) == 0:
                letter = tile.letter
            elif mode.currentPlayer.selectedTiles.index(tile) == 1:
                letter = tile.letter
                startTileX = startTileX + size
            elif mode.currentPlayer.selectedTiles.index(tile) == 2:
                letter = tile.letter
                startTileX = startTileX + size
            elif mode.currentPlayer.selectedTiles.index(tile) == 3:
                letter = tile.letter
                startTileX = startTileX + size
            elif mode.currentPlayer.selectedTiles.index(tile) == 4:
                letter = tile.letter
                startTileX = startTileX + size
            elif mode.currentPlayer.selectedTiles.index(tile) == 5:
                letter = tile.letter
                startTileX = startTileX + size
            elif mode.currentPlayer.selectedTiles.index(tile) == 6:
                letter = tile.letter
                startTileX = startTileX + size

            canvas.create_rectangle(startTileX, startTileY, startTileX+size,
                        startTileY+size, fill="white", width=2)
            canvas.create_text(startTileX+(size/2), startTileY+(size/2),
                        text=letter,fill="black",font="Helvetica 15 bold")
            
            

    def drawTilesOnRack(mode, canvas):
        for tile in mode.currentPlayer.rack.rackList:
            mode.drawSpecificTileOnRack(canvas, tile)
    
    def drawSpecificTileOnRack(mode, canvas, tile):
        if mode.gameOver == False:
            separationBtwnEachTile = mode.width/60
            startTileX = mode.width/4.625
            startTileY = mode.height/25 + (6.75*mode.height/10) 
            size = mode.tileSize
            if mode.currentPlayer.rack.rackList.index(tile) == 0:   #1st tile in rack
                letter = tile.letter
                tile.x = startTileX
                tile.y = startTileY 
            elif mode.currentPlayer.rack.rackList.index(tile) == 1: 
                letter = tile.letter
                tile.x = startTileX + size + separationBtwnEachTile
                tile.y = startTileY 
            elif mode.currentPlayer.rack.rackList.index(tile) == 2:
                letter = tile.letter
                tile.x = startTileX + 2*size + 2*separationBtwnEachTile
                tile.y = startTileY 
            elif mode.currentPlayer.rack.rackList.index(tile) == 3:
                letter = tile.letter
                tile.x = startTileX + 3*size + 3*separationBtwnEachTile
                tile.y = startTileY
            elif mode.currentPlayer.rack.rackList.index(tile) == 4:
                letter = tile.letter
                tile.x = startTileX + 4*size + 4*separationBtwnEachTile
                tile.y = startTileY
            elif mode.currentPlayer.rack.rackList.index(tile) == 5:
                letter = tile.letter
                tile.x = startTileX + 5*size + 5*separationBtwnEachTile
                tile.y = startTileY
            elif mode.currentPlayer.rack.rackList.index(tile) == 6:
                letter = tile.letter
                tile.x = startTileX + 6*size + 6*separationBtwnEachTile
                tile.y = startTileY
            canvas.create_rectangle(tile.x, tile.y, tile.x+size, tile.y+size, 
                            fill=tile.currentFill,width=3)
            canvas.create_text(tile.x+(size/2), tile.y+(size/2), text=letter,
                            fill="black",font="Helvetica 25 bold")
            canvas.create_text(tile.x+(4*size/5), tile.y+(2*size/3), 
                            text=str(tile.pointVal), font="Helvetica 15 bold")
            #print(mode.currentPlayer.rack.rackList)
        
    
    def drawPlayerRack(mode, canvas):
        rackX = mode.width/4.5
        rackY = mode.height/25 + (7*mode.height/10)
        width = mode.width/1.8
        height = mode.height/10
        canvas.create_rectangle(rackX, rackY, rackX+width, rackY+height,
                                fill="#6f4e37",width=5)
        
    def drawWhoseTurn(mode, canvas):
        rectX = mode.width/3
        rectY = mode.height/25
        width = mode.width/3
        height = mode.height/10
        canvas.create_rectangle(rectX, rectY, rectX+width, rectY+height,
                                fill="#DEB887",width=5)

        text = str(mode.currentPlayer.name) + "'s Turn"
        canvas.create_text(rectX+(width/2), rectY+(height/2), 
                            text=text, fill="brown",font="Helvetica 35 bold")

    def drawBackground(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill="brown")



# the intermediary screen in Two-Player Mode between the two players
class WaitForNextPlayerMode(Mode):
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill="brown")
        text = "Pass the computer, it's the next player's turn!"
        canvas.create_text(mode.width/2, mode.height/2, text=text, fill="white", font="Helvetica 30 bold")
        text2 = "Press enter when you're ready."
        text2y = mode.height - mode.width/3
        canvas.create_text(mode.width/2, text2y, text=text2, fill="white", font="Helvetica 30 bold")
    
    def keyPressed(mode, event):
        if event.key == "Enter":
            mode.app.setActiveMode(mode.app.gameComputerMode)



# General ModalApp construction (such as class MyModalApp) taken from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.instructionsMode = InstructionsMode()
        app.middleMode = MiddleMode()
        #app.gameMode = GameMode()
        app.gameComputerMode = GameComputerMode()
        app.waitForNextPlayerMode = WaitForNextPlayerMode()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay = 25


# Scrabble is a trademark of Hasbro Gaming company. I just coded a version of it here.
def runScrabble():
    MyModalApp(width=800, height=800)

runScrabble()

