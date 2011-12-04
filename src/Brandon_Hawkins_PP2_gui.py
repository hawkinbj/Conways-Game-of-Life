#------------------------------------------------------------------------------
# Brandon_Hawkins_PP2_gui.py 
# Student Name: Brandon Hawkins 
# Assignment: Project #2
# Submission Date: 11/22/2011 
#------------------------------------------------------------------------------
# Honor Code Statement: I received no assistance on this assignment that 
#                       violates the ethical guidelines as set forth by the 
#                       instructor and the class syllabus. 
#------------------------------------------------------------------------------

from Tkinter import *  
from tkFileDialog import * 
from Brandon_Hawkins_PP2_cell import Cell
from Brandon_Hawkins_PP2_board import Board
from Brandon_Hawkins_PP2_validation import*

# Constant for square dimensions of grid.
BOARDSIZE = 20

class GameFrame (Frame):
    """GUI representation of Game of Life."""
    def __init__(self, parent):
        """Initialize frame."""
        # Initialize parent Frame.
        Frame.__init__(self, parent)
        self.cell_btns = {}
        self.grid()   
        self.create_widgets()
            
    def create_widgets(self):
        """Fills the frame with various buttons."""
        # Fill grid (dictionary) with cell buttons.
        grid = {}
        for i in range(BOARDSIZE):
            for j in range(BOARDSIZE):
                grid[(i, j)] = Cell(False)
                cell_btn = Button(self, text="", relief=GROOVE, width=2)
                cell_btn.bind("<Button-1>", self.click_cell_btn)
                cell_btn.grid(row=i, column=j)
                # Store buttons and their coordinates in a dictionary.
                self.cell_btns[i, j] = cell_btn
           
        # Initialize Board with dead cells.    
        self.board = Board(grid, BOARDSIZE)
        
        # Place error label.
        self.error_lbl = Label(self, text="", foreground="red")
        self.error_lbl.grid(columnspan=15, column=2, row=(BOARDSIZE + 1))
          
        # Place reset button.
        reset_btn = Button(self, text="Reset", command=self.click_reset_btn)
        reset_btn.grid(columnspan=2, pady=10, column=5, row=(BOARDSIZE + 2))
        
        # Place load file button.
        loadfile_btn = Button(self, text="Load File...", command=self.click_loadfile_btn)
        loadfile_btn.grid(columnspan=4, column=4, row=(BOARDSIZE + 3))
        
        # Place generation step button.
        step_btn = Button(self, text="Step for one Generation", command=self.click_step_btn)
        step_btn.grid(columnspan=6, column=10, row=(BOARDSIZE + 2))
        
        # Place save file button.
        savefile_btn = Button(self, text="Save to File...", command=self.click_savefile_btn)
        savefile_btn.grid(columnspan=4, column=10, row=(BOARDSIZE + 3))
        
        # Place number of generations label.
        num_of_gens_lbl = Label(self, text="# of Generations:")
        num_of_gens_lbl.grid(columnspan=4, column=4, row=(BOARDSIZE + 4))
                
        # Place number of generations entry box.
        self.counter = StringVar(value="<#>")
        self.num_of_gens_box = Entry(self, width=4, textvariable=self.counter)
        self.num_of_gens_box.grid(columnspan=4, column=7, row=(BOARDSIZE + 4)) 
        
        # Place go button for multiple generation advancement.
        go_btn = Button(self, text="Go!", command=self.click_go_btn)
        go_btn.grid(columnspan=2, pady=10, column=10, row=(BOARDSIZE + 4))
        
    def click_cell_btn(self, event):
        """Registers a right-mouse click on a particular cell button
        
        Registers a right-mouse click on a particular cell button and
        alternates the cell's internal and displayed states.
        
        """
        # Clear any previous error messages on action.
        self.clear_error_lbl()
        
        cell = event.widget
        # Store grid coordinates (dictionary)
        info = cell.grid_info()
        # If cell is alive, kill it and update display...
        if cell["text"] == "X":
            self.board.set_cell(Cell(False), int(info["row"]), int(info["column"]))
            cell.configure(text="", background="SystemButtonFace")
        # ...otherwise set cell to alive and update display.
        else:
            self.board.set_cell(Cell(True), int(info["row"]), int(info["column"]))
            cell.configure(text="X", background="medium sea green")
        
    def click_reset_btn(self):
        """Registers reset_btn clicks
        
        Resets the board to all False (dead) cells.
        
        """
        # Clear any previous error messages on action.
        self.clear_error_lbl()
        
        for i in range(BOARDSIZE):
            for j in range(BOARDSIZE):
                self.board.set_cell(Cell(False), i, j)
                self.cell_btns[(i, j)].configure(text="", background="SystemButtonFace")
    
    def click_loadfile_btn(self):
        """Registers loadfile_btn clicks
        
        Prompts user for file and displays reads contents into internal
        board and displays cell states.
           
        """
        # Clear any previous error messages on action.
        self.clear_error_lbl()
        
        f = askopenfile(filetypes=[("TXT Files", "*.txt")], mode="rU")
        read = f.readlines()     
        # Pass list to Validation object. Returns True if valid, False otherwise.   
        if not Validation(read).validate_lines():
            self.error_lbl.config(text="Invalid file.")
            return
        # File is valid. Sore in 2-dim list representing board.
        grid = [] 
        for i in range (len(read)):    
            lines = read[i].rstrip()
            grid.append(list(lines))
        f.close()
        
        # This block determines what type of Cell to place based on file text
        for i in range(BOARDSIZE):
            for j in range(BOARDSIZE):
            # Swap "X" with living Cell object and update display.
                if grid[i][j] == 'X':
                    self.board.set_cell(Cell(True), i, j)
                    self.cell_btns[(i, j)].configure(text="X", background="medium sea green")
                # Swap "." with dead Cell object and update display.
                else:
                    self.board.set_cell(Cell(False), i, j)
                    self.cell_btns[(i, j)].configure(text="", background="SystemButtonFace")
        
    def click_savefile_btn(self):
        """Registers savefile_btn clicks
        
        Prompts user for filename and writes internal Board to said file.
           
        """
        f = open(asksaveasfilename(filetypes=[("TXT Files", "*.txt")], defaultextension=".txt"), "w")
        build_string = ""
        for i in range(BOARDSIZE):
            if i > 0:
                build_string += "\n"
            for j in range(BOARDSIZE):
                build_string += (str(self.board.get_cell(i, j)))
        # Last character of last line must be "\n".
        build_string += "\n"
        f.writelines(build_string)
        f.close()
    
    def click_step_btn(self):
        """Registers step_btn clicks
        
        Checks whether each cell on the Board will live in the "next
        generation" based on Board.would_cell_live(). Creates new Board
        filled with next generation Cells and displays the new Board.
           
        """
        # Clear any previous error messages on action.
        self.clear_error_lbl()
        # Need to store future cell states in new dictionary so as not to base
        # would_cell_live on updated values during iterations.
        new_board = {}   
        for i in range(BOARDSIZE):
            for j in range(BOARDSIZE):
                if self.board.would_cell_live(i, j):
                    new_board[(i, j)] = Cell(True)
                    self.cell_btns[(i, j)].configure(text="X", background="medium sea green")
                else:
                    new_board[(i, j)] = Cell(False)
                    self.cell_btns[(i, j)].configure(text="", background="SystemButtonFace")
        # Construct new board reflecting new generation of cells.
        self.board = Board(new_board, BOARDSIZE) 
    
    def click_go_btn(self):
        """Registers go_btn clicks
        
        Executes the click_step_btn method a number of times equal to
        self.counter value entered in self.num_of_gens_box. This means
        the cells/board iterate through the number of next generations
        provided by the user.
        
        """
        # Clear any previous error messages on action.
        self.clear_error_lbl()
        
        try:
            # Get the number of iterations to execute.
            count = int(self.counter.get())
        except ValueError as error:
            self.error_lbl.config(text=error)
        # Input is valid.
        else:
            self.clear_error_lbl()
            while count > 0:
                count -= 1
                self.click_step_btn()
                # Decrement displayed counter in self.num_of_gens_box.
                self.counter.set(str(count))
                # Flush buffer to show countdown.
                self.master._root().update_idletasks()
                
    def clear_error_lbl(self):
        self.error_lbl.config(text="")
