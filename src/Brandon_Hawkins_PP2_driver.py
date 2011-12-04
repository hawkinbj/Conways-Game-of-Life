#------------------------------------------------------------------------------
# Brandon_Hawkins_PP2_driver.py 
# Student Name: Brandon Hawkins 
# Assignment: Project #2
# Submission Date: 11/22/2011 
#------------------------------------------------------------------------------
# Honor Code Statement: I received no assistance on this assignment that 
#                       violates the ethical guidelines as set forth by the 
#                       instructor and the class syllabus. 
#------------------------------------------------------------------------------

from Brandon_Hawkins_PP2_gui import GameFrame
from Tkinter import Tk

def main():
    parent = Tk()
    parent.title("Game of Life Simulator")
    parent.geometry("480x660")
    GameFrame(parent)
    parent.mainloop()
    
main()
