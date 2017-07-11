import numpy as np
import random
import copy
import os
import Tkinter as tk

class Board(tk.Frame):
    
    def __init__(self, parent, dims):
        self.x = dims[0]
        self.y = dims[1]
        
        self.width = self.x - 1
        self.height = self.y - 1
        
        self.GAME_SPEED = 1000
        
        self.board = self.createBoard()
        self.tempBoard = []
        self.size = 8
        
        self.canvas_width = self.x * self.size
        self.canvas_height = self.y * self.size 
                
        tk.Frame.__init__(self, parent)
        
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=self.canvas_width, height=self.canvas_height, background="white")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        
    def createBoard(self):
        """
            Create a board with all zero entries.
        """
        board = []
        
        for x in range(self.x):
            board.append([])
            for y in range(self.y):
                board[x].append(0)
                
        return board
    
    def printBoard(self):
        """
            Print the cells of the board
        """
        for row in self.board:
            print row
            
        print ""    
        
    def randomSeed(self, prob):
        """
            Generate live cells on the board as a random seed, with a probability of being alive of prob.
        """
        
        for x in range(self.x):
            for y in range(self.y):
                if not(x == 0 or x == self.x-1 or y == 0 or y == self.y-1):
                    if random.random() < prob:
                        self.board[x][y] = 1

    def inputBoard(self, positions):
        """
            Allow the user to specify a board by supplying a list of positions to be alive.
        """
        for (x,y) in positions:
            self.board[x][y] = 1
            

    def neighbours(self, x, y):
        """
            Gets the value of the neighbours of the point (x,y) and returns them as a list.
            
            Note: Functions on the tempBoard
            
            Goes across neighbouring values left to right, top to bottom.
            
            e.g. 
            e is input point value,
            
            a b c
            d e f
            g h i 
            
            Returns [a, b, c, d, f, g, h, i]
        """
        nbs = []
        dirs = [-1, 0, 1]
        for dirx in dirs:
            if (x == 0) and (dirx == -1):
                dirx = self.width
                
            if (x == self.width) and (dirx == 1):
                dirx = -self.width 
                
            for diry in dirs:
                if (y == 0) and (diry == -1):
                    diry = self.height
                
                if (y == self.height) and (diry == 1):
                    diry = -self.height 
                
                if not((diry == 0) and (dirx == 0)):

                    nbs.append(self.tempBoard[x + dirx][y + diry])
                    
        return nbs        
            
    def update(self):
        """
            Iterate over the cells of the board and update them according to
            the rules of Conway's Game of Life.
        """
        self.tempBoard = copy.deepcopy(self.board)
        for x in range(self.x):
            for y in range(self.y):
                # Get value of neighbours
                nbs = sum(self.neighbours(x, y))
                cell = self.tempBoard[x][y] 
                
                # If the cell is dead and has 3 live neighbours, they reporoduce.
                if (cell == 0 and nbs == 3):
                    self.board[x][y] = 1
                    
                if cell == 1:
                    # Implicit if equal to two or three, lives
                    # Less than two neighbours, dies
                    if nbs < 2:
                        self.board[x][y] = 0
                                                
                    # More than 3 neighbours, dies
                    if nbs > 3:
                        self.board[x][y] = 0
    
    def redraw(self):
        """
            Redraw the board
        """
        xsize = int((self.canvas_width-1) / self.x)
        ysize = int((self.canvas_height-1) / self.y)
        self.size = min(xsize, ysize)
        
        self.canvas.delete("square")
        
        for x in range(self.x):
            for y in range(self.y):
                x1 = x * self.size
                y1 = y * self.size
                x2 = x1 + self.size
                y2 = y1 + self.size
                if self.board[x][y] == 1:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="black", tags="square")

        self.update()        
        self.after(self.GAME_SPEED, self.redraw)
    
if __name__ == '__main__':
    root = tk.Tk()
    
    dims = (100,50)
    
    board = Board(root, dims)
    board.pack(side="top", fill="both", expand=True, padx=2, pady=2)
    board.randomSeed(0.2)
    # glider board.inputBoard([(10,10), (11,10), (12,10), (12,9), (11,8)])
    board.redraw()
    
    root.mainloop()   