#!/usr/bin/python
import os
import sys
import curses

from optparse import OptionParser

"""
This is a python, curses implimentation of Conway's game of life
v1.0 (2010-05-15)
by Daniel Thau
Licensed under the GPLv2
"""

def load_board(filename, board):
    """
    loads the file argument into the board
    """
    with open(filename,'r') as f:
        loaded_file = f.readlines()

    # finding row/col offset to center file on board
    rows = cols = 0
    for line in loaded_file:
        rows+=1
        if len(line)>cols:
            cols=len(line)
        row_offset=(len(board)-rows)/2
        col_offset=(len(board[0])-cols)/2

    row = 0
    for line in loaded_file:
        col = 0
        for char in line:
            if char in ['0', '1']:
                board[row+row_offset][col+col_offset] = int(char)
            col += 1
        row += 1

    return board

def new_board(screen_width, screen_height):
    """
    creat empty board
    """
    return [[0 for i in range(screen_width)] for j in range(screen_height)]



def draw_board(screen, board):
    """
    draw board onto screen
    """
    global options

    chars = {0:' ', 1:'#'}

    color_to_use = 0
    if options.color:
        color_to_use = curses.color_pair(1)

    for row in range(len(board)):
        for col in range(len(board[0])):
            screen.addstr(row, col*2, chars[board[row][col]], color_to_use)


def check_life(screen, board):
    """
    follows Conway's Game of Life rules to determine which cells
    are alive in the next frame
    """
    nextboard=new_board(len(board[0]),len(board))
    for row in range(len(board)):
        for col in range(len(board[0])):
            live_neighbors = 0

            # checking neighbors
            for row_offset in [-1,0,1]:
                for col_offset in [-1,0,1]:

                    check_row = row+row_offset

                    if check_row < 0:
                        check_row = len(board)-1

                    if check_row == len(board):
                        check_row = 0

                    check_col = col+col_offset

                    if check_col < 0:
                        check_col = len(board[0])-1

                    if check_col == len(board[0]):
                        check_col = 0

                    if board[check_row][check_col] == 1:
                        live_neighbors += 1

            if board[row][col]==0:
                if live_neighbors==3:
                    nextboard[row][col] = 1
            else:
                # checking for 3 or 4 since actual cell was counted as a neighbor
                if  3 <= live_neighbors <= 4:
                    nextboard[row][col] = 1

    return nextboard

def main(screen, pause_between_frames, filename):
    """
    main loop
    """
    screen_height=screen.getmaxyx()[0]
    screen_width=screen.getmaxyx()[1]/2-1
    curses.curs_set(0) # makes cursor invisible
    
    if options.color:
        #Get some color settings in the works
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)


    board = load_board(filename,new_board(screen_width,screen_height))

    if pause_between_frames:
        while screen.getch()!=ord('q'):
            draw_board(screen, board)
            board = check_life(screen,board)
    else:
        while True:
            draw_board(screen, board)
            board = check_life(screen, board)
            screen.refresh()



if __name__ == '__main__':

    global options 

    parser = OptionParser()

    parser.add_option("-p", "--pause", dest="pause_between_frames",
            default=False, action="store_true")

    parser.add_option("-c", "--color", dest="color",
            default=False, action="store_true")

    (options, args) = parser.parse_args()

    files = []
    for arg in args:
        if not os.path.exists(arg):
            print "File not found, quitting"
            sys.exit()

        else:
            files.append(arg)

    curses.wrapper(main, options.pause_between_frames, files[0])

