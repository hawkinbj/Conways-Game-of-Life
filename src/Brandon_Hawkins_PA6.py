#-------------------------------------------------------------------------------
# Student Name: Brandon Hawkins / Assignment: PA #6 / Date: 11/02/2011
#-------------------------------------------------------------------------------
# Honor Code Statement: I received no assistance on this assignment that 
# violates the ethical guidelines set forth by professor and class syllabus.
#-------------------------------------------------------------------------------
#Assumptions: If file is < 20 lines, lines of dead Cells are added. If individual
# lines are < 20 characters, dead Cells are added. If supplied board/.txt file
# is larger than 20x20, lines are removed from bottom.
#-------------------------------------------------------------------------------
# NOTE: width of source code should be < 80 characters to facilitate printing 
#-------------------------------------------------------------------------------

import os
from Brandon_Hawkins_PA7_Cell import Cell
from Brandon_Hawkins_PA7_Board import Board

BOARDSIZE = 20

def main():
    global BOARDSIZE
    """Configure the initial board from a .txt file."""
    print_dir()
    print "\nPlease select a file containing an initial cell state board: " 
    fileName = str(raw_input())
    # Make sure the file actually exists.
    if not os.path.exists(fileName):
        print "That is not a valid entry."
        main()
    grid = []  
    f = open(fileName, "r+")
    read = f.readlines()        
    for i in range (len(read)):    
        temp = read[i].rstrip()
        grid.append(list(temp))
    # If Board in .txt file is larger than default BOARDSIZE, update BOARDSIZE
    tempSize = file_len(fileName)
    if tempSize > BOARDSIZE:
        BOARDSIZE = tempSize
    f.close()
    # If total num of lines is < size, append lines of dead cells. 
    while len(grid) < BOARDSIZE:
        newlines = []
        for i in range(BOARDSIZE):
            newlines.append('.')
        grid.append(newlines)
    for i in range(len(grid)):
        for j in range(len(grid)):
            # If a line is < 20 in length, add dead cells. 
            while (len(grid[i]) < BOARDSIZE):
                grid[i].append('.')
            # Swap "X" with living Cell object.
            if grid[i][j] == 'X':
                grid[i][j] = Cell(True)
            # Swap "." with dead Cell object.
            elif grid[i][j] == '.':
                grid[i][j] = Cell(False)
        # Construct board            
    board = Board(grid)     
    main_menu(board)

def file_len(fileName):
    """Determines num of lines in file."""
    with open(fileName) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def main_menu(board, invalid=False):
    """Main Menu."""
    if invalid:
        print "Please enter a valid selection./n"
    clear_screen()
    print "\n1. Print the board."
    print "2. Is the cell at point (x,y) currently alive?"
    print "3. Would the cell at point (x,y) be alive in the next generation?"
    print "4. Quit."
    choice = raw_input("Please make a selection: ")
    if choice in ("One", "one", "1", 1):
        print board
        main_menu(board)
    elif choice in ("Two", "two", "2", 2):
        (i, j) = input("What point? (Answer with #,#) : ") 
        if board.get_cell(i, j).alive:
            print "Yes"
        else:
            print "No"
        main_menu(board)
    elif choice in ("Three", "three", "3", 3):
        (i, j) = input("What point? (Answer with #,#) : ") 
        if board.would_cell_live(i, j):
            print "Yes"
        else:
            print "No"
        main_menu(board)
    elif choice in ("Four", "four", "4", 4):
        exit
    else:
        main_menu(board, True)
        
def print_dir():
    """Presents the current directory in a readable format"""
    print ("Current directory:\n")
    for dirname, dirnames, filenames in os.walk('.'):
        for subdirname in dirnames:
            print "\t" + os.path.join(dirname, subdirname)
        for filename in filenames:
            print "\t" + os.path.join(dirname, filename) 
        
def clear_screen():
    """Clear the terminal."""
    if (os.name == "posix"):
        clear_cmd = "clear"
    elif (os.name == "nt"):
        clear_cmd = "cls"
    else:
        print "*** Unsupported System ***\nApplication Terminating !!!"
    os.system(clear_cmd)
    
main()
