#NAME: ISHIKA SAXENA

import math, copy, string
import random
# cmu_112_graphics_final taken from 15-112 CMU Fundamentals in Programming & Computer Science Course: 
# Taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics_final import *
from tkinter import *
from PIL import Image

# The home screen
class SplashScreenMode(Mode):
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill="brown")
        mode.drawTiles(canvas)
        mode.drawButtons(canvas)
    
    def drawTiles(mode, canvas):
        heightOfEachTile = (mode.height - (2*(mode.height//8))) // 7
        # drawing S
        nextHeight = mode.height/8 + heightOfEachTile
        canvas.create_rectangle(mode.width/8, mode.height/8, mode.width/4, 
            nextHeight, fill="#DEB887",width=5)
        canvas.create_text(mode.width/8+((mode.width/8)/2), 
            mode.height/8+((mode.height/8)/2), text="S",fill="brown",font="Helvetica 50 bold")
        

        # drawing C
        nextHeight2 = nextHeight + heightOfEachTile   
        goesIn1 = mode.height/8 + heightOfEachTile
        canvas.create_rectangle(mode.width/8, goesIn1, mode.width/4, nextHeight2, 
                                fill="#DEB887",width=5)
        canvas.create_text(mode.width/8+((mode.width/8)/2), goesIn1+(goesIn1/4), 
                                text="C",fill="brown",font="Helvetica 50 bold")
        
        # drawing R
        nextHeight3 = nextHeight2 + heightOfEachTile
        goesIn2 = mode.height/8 + 2*heightOfEachTile
        canvas.create_rectangle(mode.width/8, goesIn2, mode.width/4, nextHeight3, 
                                fill="#DEB887",width=5)
        canvas.create_text(mode.width/8+((mode.width/8)/2), goesIn2 + (heightOfEachTile/2), 
                                text="R",fill="brown",font="Helvetica 50 bold")
        
        # drawing A
        nextHeight4 = nextHeight3 + heightOfEachTile
        goesIn3 = mode.height/8 + 3*heightOfEachTile
        canvas.create_rectangle(mode.width/8, goesIn3, mode.width/4, nextHeight4, 
                                fill="#DEB887",width=5)
        canvas.create_text(mode.width/8+((mode.width/8)/2), goesIn3 + (heightOfEachTile/2), 
                                text="A",fill="brown",font="Helvetica 50 bold")
        
        # drawing I
        canvas.create_rectangle(mode.width/4, goesIn3, mode.width/4+heightOfEachTile+10, nextHeight4, 
                                fill="#DEB887",width=5)
        canvas.create_text((mode.width/4 + (mode.width/4)+heightOfEachTile+10)/2, goesIn3 + 45, 
                            text="I", fill="brown", font="Helvetica 50 bold")
        
        # drawing B
        nextHeight5 = nextHeight4 + heightOfEachTile
        goesIn4 = mode.height/8 + 4*heightOfEachTile
        canvas.create_rectangle(mode.width/8, goesIn4, mode.width/4, nextHeight5, 
                                fill="#DEB887",width=5)
        canvas.create_text(mode.width/8+((mode.width/8)/2), goesIn4 + (heightOfEachTile/2), 
                                text="B",fill="brown",font="Helvetica 50 bold")
        
        # drawing B
        nextHeight6 = nextHeight5 + heightOfEachTile
        goesIn5 = mode.height/8 + 5*heightOfEachTile
        canvas.create_rectangle(mode.width/8, goesIn5, mode.width/4, nextHeight6, 
                                fill="#DEB887",width=5)
        canvas.create_text(mode.width/8+((mode.width/8)/2), goesIn5 + (heightOfEachTile/2), 
                                text="B",fill="brown",font="Helvetica 50 bold")
        
        # drawing L
        nextHeight7 = nextHeight6 + heightOfEachTile
        goesIn6 = mode.height/8 + 6*heightOfEachTile
        canvas.create_rectangle(mode.width/8, goesIn6, mode.width/4, nextHeight7, 
                                fill="#DEB887",width=5)
        canvas.create_text(mode.width/8+((mode.width/8)/2), goesIn6 + (heightOfEachTile/2), 
                                text="L",fill="brown",font="Helvetica 50 bold")
        
        # drawing E
        nextHeight8 = nextHeight7 + heightOfEachTile
        goesIn7 = mode.height/8 + 7*heightOfEachTile
        canvas.create_rectangle(mode.width/8, goesIn7, mode.width/4, nextHeight8, 
                                fill="#DEB887",width=5)
        canvas.create_text(mode.width/8+((mode.width/8)/2), goesIn7 + (heightOfEachTile/2), 
                                text="E",fill="brown",font="Helvetica 50 bold")


    def drawButtons(mode, canvas):
        # play button
        playX = mode.width - (mode.width/3)
        playY = mode.height / 2
        width = mode.width/4
        height = mode.height/7
        canvas.create_rectangle(playX, playY, playX+width, playY+height,fill="#DEB887",width=5)
        canvas.create_text(playX+(width/2), playY+(height/2), 
                            text="PLAY", fill="brown", font="Helvetica 50 bold")
        
        # instructions button
        instrucX = playX
        instrucY = mode.height - (mode.height/3)
        canvas.create_rectangle(instrucX, instrucY, instrucX+width, instrucY+height,
                                fill="#DEB887",width=5)
        canvas.create_text(instrucX+(width/2), instrucY+(height/2), 
                            text="INSTRUCTIONS", fill="brown", font="Helvetica 25 bold")
        

    def mousePressed(mode, event):
        playX = mode.width - (mode.width/3)
        playY = mode.height / 2
        width = mode.width/4
        height = mode.height/7
        instrucX = playX
        instrucY = mode.height - (mode.height/3)

        # if they click on Play / Instruction button, switch mode
        if( (playX <= event.x <= playX+width) and (playY <= event.y <= playY+height) ):
            mode.app.setActiveMode(mode.app.middleMode)
        elif( (instrucX <= event.x <= instrucX+width) and (instrucY <= event.y <= instrucY+height) ):
            mode.app.setActiveMode(mode.app.instructionsMode)
