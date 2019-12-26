#Author: ISHIKA SAXENA

import math, copy, string
import random
# cmu_112_graphics_final taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics_final import *
from tkinter import *
from PIL import Image

# Board class manages the board (e.g. draws the tiles, forms possible words)
class Board(object):
    def __init__(self, app):
        self.app = app
        self.rows = 15
        self.cols = 15
        self.marginX = self.app.width/5.5 #mode.width/4.625 #7.5
        self.topMarginY = .14*self.app.height
        self.bottomMarginY = .30*self.app.height
        self.textBoard = [ (["-"]*self.cols) for row in range(self.rows) ]
        self.initializeSpecialSpotsLocations()
        self.okayToDrawTiles = True
        self.finalizedTilesToDraw = []
        self.rowscolsToRemoveIfPlayerMessesUp = []
    
    # initialize multipliers' board locations and colors
    def initializeSpecialSpotsLocations(self):
        self.tripleWordLocations = [(0,0), (0,7), (0,14), (7,0), (7,14), (14,0), (14,7), (14,14)]
        self.doubleWordLocations = [(1,1), (1,13), (2,2), (2,12), (3,3), (3,11), (4,4), (4,10),
                                    (7,7), (10,4), (10,10), (11,3),(11,11), (12,2), (12,12),
                                    (13,1), (13,13)]
        self.doubleLetterLocations = [(0,3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14),
                                    (6,2), (6,6), (6,8), (6,12), (7,3), (7,11), (8,2), (8,6),
                                    (8,8), (8,12), (11,0), (11,7), (11,14), (12,6), (12,8),
                                    (14,3), (14,11)]
        self.tripleLetterLocations = [(1,5), (1,9), (5,1), (5,5), (5,9), (5,13), (9,1), (9,5),
                                    (9,9), (9,13), (13,5), (13,9)]
        self.tripleWordColor = "red"
        self.doubleWordColor = "#ff8c69" #tannish pink
        self.doubleLetterColor = "#90f3f1" #light blue 
        self.tripleLetterColor = "blue"
        self.regularColor = "#DEB887" #tan
    

    def drawBoard(self, canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                fill = self.decideFillOnBoard(row, col)
                (x0, y0, x1, y1) = self.getCellBounds(row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill=fill, width=2)
    
    def decideFillOnBoard(self, row, col):
        if (row, col) in self.tripleWordLocations:
            return self.tripleWordColor
        elif (row, col) in self.doubleWordLocations:
            return self.doubleWordColor
        elif (row, col) in self.doubleLetterLocations:
            return self.doubleLetterColor
        elif (row, col) in self.tripleLetterLocations:
            return self.tripleLetterColor
        else:
            return self.regularColor
    
    # sets up drawing process, filtering through selected tiles  & clicked positions
    def drawSelectedTilesOnBoard(self):
        for position in self.app.currentPlayer.clickList:   #position is (row, col)
            if self.app.currentPlayer.clickList.index(position) == 0:
                tile = self.app.currentPlayer.selectedTiles[0]
            elif self.app.currentPlayer.clickList.index(position) == 1:
                tile = self.app.currentPlayer.selectedTiles[1]
            elif self.app.currentPlayer.clickList.index(position) == 2:
                tile = self.app.currentPlayer.selectedTiles[2] 
            elif self.app.currentPlayer.clickList.index(position) == 3:
                tile = self.app.currentPlayer.selectedTiles[3] 
            elif self.app.currentPlayer.clickList.index(position) == 4:
                tile = self.app.currentPlayer.selectedTiles[4] 
            elif self.app.currentPlayer.clickList.index(position) == 5:
                tile = self.app.currentPlayer.selectedTiles[5] 
            elif self.app.currentPlayer.clickList.index(position) == 6:
                tile = self.app.currentPlayer.selectedTiles[6] 
            self.finalizedTilesToDraw.append( (position[0], position[1], tile.letter, tile.pointVal) )
            self.updateTextBoard(position[0], position[1], tile)
            
    # actually draws the tiles on the board
    def drawFinalTilesToStay(self, canvas):
        for (row, col, letter, points) in self.finalizedTilesToDraw:
            (x0, y0, x1, y1) = self.getCellBounds(row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill="white", width=2)
            startX = x0
            startY = y0
            sizeX = (self.app.width - 2*self.marginX) / self.cols
            sizeY = (self.app.height - (self.topMarginY + self.bottomMarginY)) / self.rows
            canvas.create_text(startX + (sizeX/2), startY+(sizeY/2), 
                    text=letter, fill="black",font="Helvetica 15 bold")
            canvas.create_text(startX + (4*sizeX/5), startY+(2*sizeY/3), 
                    text=points, fill="black",font="Helvetica 10 bold")
    
    # textBoard houses string values (i.e. letters) currently on the board
    def updateTextBoard(self, row, col, tile):
        self.textBoard[row][col] = tile.letter
        
    # forms possible word via iterating through possible directions of placed letters
    def formPossibleWord(self):
        # If center tile in clickList, call function to form "first word on board"
        if((7,7) in self.app.currentPlayer.clickList):
            self.formFirstWordOnBoard()
            return
        
        for position in self.app.currentPlayer.clickList:
            # Check for dashes in each position in clickList
            if(len(self.app.currentPlayer.clickList) > 1):
                self.checkIfDashInWord()
            # Look both up/down and left/right for a possible word
            self.findUpDown(position)   
            self.findLeftRight(position)
    
    # A dash in the word means location is invalid (i.e. there are spaces between placed letters)
    def checkIfDashInWord(self):
        val = self.decideIfRowsOrColsAreChanging() # decides whether rows or columns are changing
        word = ""
        tempList = []
        unchangingVal = -1
        if(val == "cols"): #cols are changing so will append towards upwards/downwards
            for position in self.app.currentPlayer.clickList:
                tempList.append(position[1])
                unchangingVal = position[0]
        elif(val == "rows"):    #rows are changing so will append towards left/right
            for position in self.app.currentPlayer.clickList:
                tempList.append(position[0])
                unchangingVal = position[1]
        # sort tempList now to sort the indexes so we can iterate through them more easily
        tempList.sort()
        minVal = tempList[0]
        maxVal = tempList[len(tempList)-1]
        if val == "cols":       
            for i in range(minVal, maxVal+1): 
                word = word + self.textBoard[unchangingVal][i]
            for c in word:
                if c == "-":
                    self.app.currentPlayer.wordList.append(word)
                    return
        elif val == "rows":
            for i in range(minVal, maxVal+1): 
                word = word + self.textBoard[i][unchangingVal]
            for c in word:
                if c == "-":
                    self.app.currentPlayer.wordList.append(word)
                    return

    # Looks through left/right for possible words and appends them to Player's possibleWord
    def findLeftRight(self, position):
        (row, col) = position
        # Empty or wall on left so go right until no more letters
        if (col-1 == -1 or self.textBoard[row][col-1] == "-") and \
             (col+1 == 15 or self.textBoard[row][col+1] != "-"):
            while(col < 15) and self.textBoard[row][col] != "-":
                self.app.currentPlayer.possibleWord =  self.app.currentPlayer.possibleWord + self.textBoard[row][col]
                col = col + 1
            self.app.currentPlayer.wordList.append(self.app.currentPlayer.possibleWord)
            self.app.currentPlayer.possibleWord = "" 
        # Empty or wall on right so go left until no more letters
        elif (col+1 == 15 or self.textBoard[row][col+1] == "-") and \
            (col-1==-1 or self.textBoard[row][col-1] != "-"):
            while (col > -1) and self.textBoard[row][col] != "-":
                self.app.currentPlayer.possibleWord = self.textBoard[row][col] + self.app.currentPlayer.possibleWord
                col = col - 1
            self.app.currentPlayer.wordList.append(self.app.currentPlayer.possibleWord)
            self.app.currentPlayer.possibleWord = ""
            return
        # Non-empty on left and right, so form word from min to max index of text
        else:
            tempList = []
            for position in self.app.currentPlayer.clickList:
                tempList.append(position[1])        #bc assuming cols are changing
                row = position[0]
            tempList.sort()
            minVal = tempList[0]
            maxVal = tempList[len(tempList)-1]
            if (minVal-1 == -1 and maxVal+1==15) or ((minVal-1==-1 or self.textBoard[row][minVal-1] != "-")\
                and (maxVal+1==15 or self.textBoard[row][maxVal+1] != "-")): 
                while( minVal > -1 and self.textBoard[row][minVal] != "-" ):
                    minVal = minVal - 1
                while ( maxVal < 15 and self.textBoard[row][maxVal] != "-" ):
                    maxVal = maxVal + 1
                for i in range(minVal+1, maxVal):       #play around w this?minVal, maxVal+1
                    self.app.currentPlayer.possibleWord = self.app.currentPlayer.possibleWord + self.textBoard[row][i]
                self.app.currentPlayer.wordList.append(self.app.currentPlayer.possibleWord)
                self.app.currentPlayer.possibleWord = ""
                return
    
    # Looks through up/down for possible words and appends them to Player's possibleWord
    def findUpDown(self, position):
        (row, col) = position
        # Empty or wall on above so go down until no more letters
        if (row-1 == -1 or self.textBoard[row-1][col] == "-") \
            and (row+1 == 15 or self.textBoard[row+1][col] != "-"):
            while (row < 15) and self.textBoard[row][col] != "-":
                self.app.currentPlayer.possibleWord =  self.app.currentPlayer.possibleWord + self.textBoard[row][col]
                row = row + 1
            self.app.currentPlayer.wordList.append(self.app.currentPlayer.possibleWord)
            self.app.currentPlayer.possibleWord = "" 
        # Empty or wall on below so go up until no more letters
        elif (row+1 == 15 or self.textBoard[row+1][col] == "-")\
            and (row-1 == -1 or self.textBoard[row-1][col] != "-"): 
            while (row > -1) and self.textBoard[row][col] != "-":
                self.app.currentPlayer.possibleWord = self.textBoard[row][col] + self.app.currentPlayer.possibleWord
                row = row - 1
            self.app.currentPlayer.wordList.append(self.app.currentPlayer.possibleWord)
            self.app.currentPlayer.possibleWord = ""
            return
        # Non-empty above and below, so same algoirthm as findLeftRight
        else:
            tempList = []
            for position in self.app.currentPlayer.clickList:
                tempList.append(position[0]) 
                col = position[1]
            tempList.sort()
            minVal = tempList[0]
            maxVal = tempList[len(tempList)-1]
            print(minVal, maxVal)
            if (minVal-1 == -1 and maxVal+1==15) or ((minVal-1 == -1 or self.textBoard[minVal-1][col] != "-") \
                and (maxVal+1 == 15 or self.textBoard[maxVal+1][col] != "-")):
                while( minVal > -1 and self.textBoard[minVal][col] != "-" ):
                    minVal = minVal - 1
                while ( maxVal < 15 and self.textBoard[maxVal][col] != "-" ):
                    maxVal = maxVal + 1
                for i in range(minVal+1, maxVal):
                    self.app.currentPlayer.possibleWord = self.app.currentPlayer.possibleWord + self.textBoard[i][col]
                self.app.currentPlayer.wordList.append(self.app.currentPlayer.possibleWord)
                self.app.currentPlayer.possibleWord = ""
                return

    # Forms first word on board
    def formFirstWordOnBoard(self):
        val = self.decideIfRowsOrColsAreChanging()
        tempList = []
        unchangingVal = -1
        if(val == "cols"): #cols are changing
            for position in self.app.currentPlayer.clickList:
                tempList.append(position[1])
                unchangingVal = position[0]
        elif(val == "rows"):    #rows are changing
            for position in self.app.currentPlayer.clickList:
                tempList.append(position[0])
                unchangingVal = position[1]
        self.case23(unchangingVal, tempList, val)
    
    
    # Case that finds a word that intersects another word (i.e. there's a gap in clickList)
    def case23(self, unchangingVal, tempList, val): 
        tempList.sort()
        minVal = tempList[0]
        maxVal = tempList[len(tempList)-1]
        if val == "cols":       
            for i in range(minVal, maxVal+1): 
                self.app.currentPlayer.possibleWord = self.app.currentPlayer.possibleWord + self.textBoard[unchangingVal][i]
            self.app.currentPlayer.wordList.append(self.app.currentPlayer.possibleWord)
            self.app.currentPlayer.possibleWord = ""
        elif val == "rows":
            for i in range(minVal, maxVal+1): 
                self.app.currentPlayer.possibleWord = self.app.currentPlayer.possibleWord + self.textBoard[i][unchangingVal]
            self.app.currentPlayer.wordList.append(self.app.currentPlayer.possibleWord)
            self.app.currentPlayer.possibleWord = ""

    # Find whether tempList, a version of clickList, is missing any numbers i.e. has gaps
    def isTempListMissingNums(self, tempList):
        tempList.sort()             
        minVal = tempList[0]
        maxVal = tempList[len(tempList)-1]
        for i in range(minVal, maxVal):
            if i not in tempList:
                return True     
        return False            
    
    # Find whether the rows/cols are changing in the user's clickList
    def decideIfRowsOrColsAreChanging(self):
        tuple1 = self.app.currentPlayer.clickList[0]
        tuple2 = self.app.currentPlayer.clickList[1]
        if(tuple1[0] == tuple2[0]):
            return "cols"
        else:
            return "rows"        

    # Update location validity
    def updateSelectedPositionIsValid(self): 
        # Leave spaces --> invalid
        for letter in self.app.currentPlayer.possibleWord:
            if letter == "-":
                self.app.currentPlayer.selectedPositionIsValid = False
                return    

        # row doesn't stay consistent while the cols change --> invalid location
        # col doesn't stay consistent while the rows change --> invalid location
        seenCols = []
        seenRows = []
        if len(self.app.currentPlayer.clickList) > 1:
            val = self.decideIfRowsOrColsAreChanging()
            if val == "rows":
                for (row, col) in self.app.currentPlayer.clickList:
                    if col not in seenCols and len(seenCols) > 0:
                        self.app.currentPlayer.selectedPositionIsValid = False
                        return
                    seenCols.append(col)
            elif val == "cols":
                for (row, col) in self.app.currentPlayer.clickList:
                    if row not in seenRows and len(seenRows) > 0:
                        self.app.currentPlayer.selectedPositionIsValid = False
                        return
                    seenRows.append(row)
            
            # Edge cases for position: four corners
            for (row, col) in self.app.currentPlayer.clickList:
                #top left
                if row-1==-1 and col-1==-1:
                    self.app.currentPlayer.selectedPositionIsValid = False
                    return
                #top right
                elif row-1==-1 and col+1==15:
                    self.app.currentPlayer.selectedPositionIsValid = False
                    return
                #bottom left
                elif row+1==15 and col-1==-1:
                    self.app.currentPlayer.selectedPositionIsValid = False
                    return
                #bottom right
                elif row+1==15 and col+1==15:
                    self.app.currentPlayer.selectedPositionIsValid = False
                    return

            
            # Edge cases for position: the border
            # Letters on the border are only valid if they're connected to words already on the board
            for (row, col) in self.app.currentPlayer.clickList:
                if val == "rows":
                    if col+1 == 15:
                        if (self.textBoard[row][col-1] != "-" and (row, col-1) not in self.app.currentPlayer.clickList) \
                            or (self.textBoard[row+1][col] != "-" and (row+1, col) not in self.app.currentPlayer.clickList) \
                            or (self.textBoard[row-1][col] != "-" and (row-1, col) not in self.app.currentPlayer.clickList):
                            self.app.currentPlayer.selectedPositionIsValid = True
                            return
                    elif col-1 == -1:
                        if (self.textBoard[row][col+1] != "-" and (row, col+1) not in self.app.currentPlayer.clickList) \
                            or (self.textBoard[row+1][col] != "-" and (row+1, col) not in self.app.currentPlayer.clickList) \
                            or (self.textBoard[row-1][col] != "-" and (row-1, col) not in self.app.currentPlayer.clickList):
                            self.app.currentPlayer.selectedPositionIsValid = True
                            return
                elif val == "cols":
                    if row+1 == 15:
                        if (self.textBoard[row-1][col] != "-" and (row-1, col) not in self.app.currentPlayer.clickList) \
                            or (self.textBoard[row][col-1] != "-" and (row, col-1) not in self.app.currentPlayer.clickList) \
                            or (self.textBoard[row][col+1] != "-" and (row, col+1) not in self.app.currentPlayer.clickList):
                            self.app.currentPlayer.selectedPositionIsValid = True
                            return
                    elif row-1 == -1:
                        if (self.textBoard[row+1][col] != "-" and (row+1, col) not in self.app.currentPlayer.clickList) \
                            or (self.textBoard[row][col-1] != "-" and (row, col-1) not in self.app.currentPlayer.clickList) \
                            or (self.textBoard[row][col+1] != "-" and (row, col+1) not in self.app.currentPlayer.clickList):
                            self.app.currentPlayer.selectedPositionIsValid = True
                            return
        else:
            # Case of only 1 tile being placed down (partioned into cases on the edge/border)
            for (row, col) in self.app.currentPlayer.clickList:
                if col+1==15:
                    if row-1 != -1 and row+1 != 15:
                        if self.textBoard[row-1][col] != "-" or self.textBoard[row+1][col] != "-" or self.textBoard[row][col-1] != "-":
                            self.app.currentPlayer.selectedPositionIsValid = True
                            return
                elif col-1 == -1:
                    if row-1 != -1 and row+1 != 15:
                        if self.textBoard[row-1][col] != "-" or self.textBoard[row+1][col] != "-" or self.textBoard[row][col+1] != "-":
                            self.app.currentPlayer.selectedPositionIsValid = True
                            return
                elif row+1 == 15:
                    if col-1 != -1 and col+1 != 15:
                        if self.textBoard[row][col-1] != "-" or self.textBoard[row][col+1] != "-" or self.textBoard[row-1][col] != "-":
                            self.app.currentPlayer.selectedPositionIsValid = True
                            return
                elif row-1 == -1:
                    if col-1 != -1 and col+1 != 15:
                        if self.textBoard[row][col-1] != "-" or self.textBoard[row][col+1] != "-" or self.textBoard[row+1][col] != "-":
                            self.app.currentPlayer.selectedPositionIsValid = True
                            return
        
        # General checks for adjacency, for tiles not on the border
        for position in self.app.currentPlayer.clickList:
            if position == (7, 7):
                self.app.currentPlayer.selectedPositionIsValid = True
                return
            (row, col) = position
            if (row-1 != -1) and (row+1 != 15) and (col-1 != -1) and (col+1 != 15):
                if (self.textBoard[row-1][col] != "-") and ((row-1, col) not in self.app.currentPlayer.clickList):
                    self.app.currentPlayer.selectedPositionIsValid = True
                    return
                elif self.textBoard[row][col+1] != "-" and ((row, col+1) not in self.app.currentPlayer.clickList):
                    self.app.currentPlayer.selectedPositionIsValid = True
                    return
                elif self.textBoard[row+1][col] != "-" and ((row+1, col) not in self.app.currentPlayer.clickList):
                    self.app.currentPlayer.selectedPositionIsValid = True
                    return
                elif self.textBoard[row][col-1] != "-" and ((row, col-1) not in self.app.currentPlayer.clickList):
                    self.app.currentPlayer.selectedPositionIsValid = True
                    return
                else:
                    self.app.currentPlayer.selectedPositionIsValid = False
        
        self.app.currentPlayer.selectedPositionIsValid = False
        


    # getCellBounds(self, row, col) taken from http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
    # returns cell bounds given (row, col)
    def getCellBounds(self, row, col):
        gridWidth  = self.app.width - 2*self.marginX
        gridHeight = self.app.height - (self.topMarginY + self.bottomMarginY)
        #gridHeight = self.app.height - (2*self.topMarginY)
        columnWidth = gridWidth / self.cols
        rowHeight = gridHeight / self.rows
        x0 = self.marginX + (col * columnWidth)
        x1 = self.marginX + (col+1) * columnWidth
        y0 = self.topMarginY + row * rowHeight
        y1 = self.topMarginY + (row+1) * rowHeight
        return (x0, y0, x1, y1)
    
    # pointInGrid(self, x, y) taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def pointInGrid(self, x, y):
    # return True if (x, y) is inside the board that we've defined
        return ((self.marginX <= x <= self.app.width-self.marginX) and
                (self.topMarginY <= y <= self.app.height-self.bottomMarginY))

    # getCell(self, x, y) taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    # returns (row, col) location of (x, y) position
    def getCell(self, x, y):
        if (self.pointInGrid(x, y) == False):
            return (-1, -1)
        gridWidth  = self.app.width - 2*self.marginX
        gridHeight = self.app.height - (self.topMarginY + self.bottomMarginY)
        cellWidth  = gridWidth / self.cols
        cellHeight = gridHeight / self.rows

        row = int((y - self.topMarginY) / cellHeight)
        col = int((x - self.marginX) / cellWidth)

        return (row, col)
