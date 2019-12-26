import math, copy, string
import random
# cmu_112_graphics_final from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics_final import *
from tkinter import *
from PIL import Image

# Rack class contains list of tiles on players' racks) & methods to replenish/initialize player's rack
class Rack(object):
    def __init__(self, app, bag): 
        self.app = app
        self.bag = bag

        # the rack
        self.rackList = []
        self.initializeStartingRack()
        self.fullTileRack = 7       
        self.currentTileRack = 7 
    
    def initializeStartingRack(self):
        for i in range(7):
            aTile = self.bag.takeFromBag()
            self.rackList.append(aTile)
    
    # called every time player plays a tile from their rack
    def takeFromRack(self, tile):
        if(len(self.rackList) > 0):
            self.rackList.remove(tile)
    
    # replenishes rack so it has 7 letters
    def replenishRack(self):
        if self.app.gameOver == False:
            currentLen = len(self.rackList)
            if(currentLen < self.fullTileRack):
                for i in range(self.fullTileRack - currentLen):
                    tileToAdd = self.bag.takeFromBag()
                    self.rackList.append(tileToAdd)

    def putTilesRemovedBackOnRack(self, tilesToPutBack): 
        for tile in tilesToPutBack:
            self.rackList.append(tile)
