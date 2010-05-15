#!/usr/bin/python
import curses, sys, os

"""
This is a python, curses implimentation of Conway's game of life
v1.0 (2010-05-15)
by Daniel Thau
Licensed under the GPLv2
"""

def load_board(filename,board):
	"""
	loads the file argument into the board
	"""
	f = open(filename,'r')
	# finding row/col offset to center file on board
	rows=0
	cols=0
	for line in f:
		rows+=1
		if len(line)>cols:
			cols=len(line)
	row_offset=(len(board)-rows)/2
	col_offset=(len(board[0])-cols)/2
	# actually loading file into board
	f = open(filename,'r')
	row=0
	for line in f:
		col=0
		for char in line:
			print col,row,'!'+char+'!'
			if char=='0':
				board[row+row_offset][col+col_offset]=0
			if char=='1':
				board[row+row_offset][col+col_offset]=1
			col+=1
		row+=1
	return board

def new_board(screen_width,screen_height):
	"""
	creat empty board
	"""
	board = []
	for h in range(screen_height):
		row = []
		for w in range(screen_width):
			row.append(0)
		board.append(row)
	return board

def draw_board(screen,board):
	"""
	draw board onto screen
	"""
	for row in range(len(board)):
		for col in range(len(board[0])):
			if board[row][col]==0:
				screen.addstr(row,col*2,". ")
			else:
				screen.addstr(row,col*2,"o ")
def check_life(screen,board):
	"""
	follows Conway's Game of Life rules to determine which cells
	are alive in the next frame
	"""
	nextboard=new_board(len(board[0]),len(board))
	for row in range(len(board)):
		for col in range(len(board[0])):
			live_neighbors=0
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
					if board[check_row][check_col]==1:
						live_neighbors+=1
			if board[row][col]==0:
				if live_neighbors==3:
					nextboard[row][col]=1
			else:
				# checking for 3 or 4 since actual cell was counted as a neighbor
				if live_neighbors==3 or live_neighbors==4:
					nextboard[row][col]=1
	return nextboard

def main(screen,pause_between_frames,filename):
	"""
	main loop
	"""
	screen_height=screen.getmaxyx()[0]
	screen_width=screen.getmaxyx()[1]/2-1
	curses.curs_set(0) # makes cursor invisible
	board = load_board(filename,new_board(screen_width,screen_height))
	if pause_between_frames:
		while screen.getch()!=ord('q'):
			draw_board(screen,board)
			board = check_life(screen,board)
	else:
		while True:
			draw_board(screen,board)
			board = check_life(screen,board)
			screen.refresh()


"""
program execution starts here
"""
pause_between_frames=False
filename=""
first_arg=True
for arg in sys.argv:
	if first_arg:
		first_arg=False
	else:
		if arg=='-p':
			pause_between_frames=True
		if arg=="--help" or arg=="-h":
			print "Conway's Game of Life v1.0 (2010-05-15) by Daniel Thau"
			print ""
			print "usage: gol [arguments] FILE"
			print ""
			print "Arguments:"
			print "   -h or --help     Show this help"
			print "   -p               Pause between frames"
			sys.exit()
		if arg[0]!='-':
			if os.path.isfile(arg)==False:
				print "Can not load file, quitting"
				sys.exit()
			else:
				filename=arg
if filename=="":
	print "No file given, quitting"
	sys.exit()
curses.wrapper(main,pause_between_frames,filename)
