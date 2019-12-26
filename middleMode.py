#Author: ISHIKA SAXENA
import math, copy, string
import random
# cmu_112_graphics_final taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics_final import *
from tkinter import *
from PIL import Image

# interface before GameMode, where user decides which mode to play
class MiddleMode(Mode):
    def appStarted(mode):
        mode.player1 = ""
        mode.player2 = ""

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height,fill="brown")
        canvas.create_text(mode.width/2, mode.height/3, text='CHOOSE WHICH MODE', fill="#DEB887", font='Arial 26 bold')
        mode.drawButtons(canvas)
    
    def drawButtons(mode, canvas):
        twoPlX = mode.width/5
        twoPlY = mode.height/2
        width = mode.width/4
        height = mode.height/7
        canvas.create_rectangle(twoPlX, twoPlY, twoPlX+width, twoPlY+height, fill="#DEB887",width=5)
        canvas.create_text(twoPlX+(width/2), twoPlY+(height/2), 
                            text="TWO-PLAYER", fill="brown", font="Helvetica 15 bold")
        
        compPlX = mode.width/2
        compPlY = mode.height/2
        canvas.create_rectangle(compPlX, compPlY, compPlX+width, compPlY+height, fill="#DEB887",width=5)
        canvas.create_text(compPlX+(width/2), compPlY+(height/2), 
                            text="    SINGLE-PLAYER \nAGAINST COMPUTER", fill="brown", font="Helvetica 15 bold")
    
    def mousePressed(mode, event):
        twoPlX = mode.width/5
        twoPlY = mode.height/2
        width = mode.width/4
        height = mode.height/7
        compPlX = mode.width/2
        compPlY = mode.height/2

        # detect click on buttons and set players' names
        if( (twoPlX <= event.x <= twoPlX+width) and (twoPlY <= event.y <= twoPlY+height) ):
            mode.player1 = "Player 1"
            mode.player2 = "Player 2"
            mode.app.setActiveMode(mode.app.gameComputerMode)
            mode.app.gameComputerMode.createPlayers()
        elif( (compPlX <= event.x <= compPlX+width) and (compPlY <= event.y <= compPlY+height) ):
            mode.player1 = "Human"
            mode.player2 = "Computer"
            mode.app.setActiveMode(mode.app.gameComputerMode)
            mode.app.gameComputerMode.createPlayers()

    def getPlayer1Name(mode):
        return mode.player1
    
    def getPlayer2Name(mode):
        return mode.player2
